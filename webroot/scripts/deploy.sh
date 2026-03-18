#!/bin/bash
# SuperPig Complete Deployment Script
# Run this whenever you need to deploy updates
# Copy this file this path /root/projects/jsys/deploy.sh:

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 🔑 SSH setup for Git (no passphrase prompts)
export GIT_SSH_COMMAND="ssh -i /root/.ssh/deploy_key -o IdentitiesOnly=yes"

echo -e "${BLUE}================================${NC}"
echo -e "${GREEN}🐷 SuperPig Deployment Script${NC}"
echo -e "${BLUE}================================${NC}"
echo "Started at: $(date)"
echo ""

# Function to print section headers
section() {
    echo ""
    echo -e "${YELLOW}▶ $1${NC}"
    echo "----------------------------------------"
}

# Function to check if last command succeeded
check_success() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}  ✅ $1${NC}"
    else
        echo -e "${RED}  ❌ $1${NC}"
        exit 1
    fi
}

# 1️⃣ STOP THE PYTHON APP
section "STEP 1: Stopping Python app"
echo "Looking for running pig_ops_web.py processes..."

# Find and kill the Python process (if exists)
PIDS=$(pgrep -f "python.*pig_ops_web.py" || true)
if [ -n "$PIDS" ]; then
    echo "Found PIDs: $PIDS"
    kill $PIDS 2>/dev/null || true
fi

# 2️⃣ CHANGE TO PROJECT ROOT
section "STEP 2: Changing to project root"
cd /root/projects/jsys
echo "Current directory: $(pwd)"
check_success "Changed to project root"

# 3️⃣ GIT PULL IN PIG_OPS_UI_MOB (Frontend)
section "STEP 3: Updating frontend (pig_ops_ui_mob)"
if [ -d "pig_ops_ui_mob" ]; then
    cd pig_ops_ui_mob
    echo "Frontend directory: $(pwd)"
    
    # Stash any local changes (optional)
    git stash > /dev/null 2>&1 || true
    
    echo "Pulling latest changes from Bitbucket..."
    git pull origin main
    check_success "Frontend git pull completed"
    
    # Go back to project root
    cd /root/projects/jsys
else
    echo -e "${RED}❌ pig_ops_ui_mob directory not found!${NC}"
    exit 1
fi

# 4️⃣ RESTORE TEMPLATES BEFORE PIG_OPS PULL
section "STEP 4: Restoring templates from backup (if exists)"
if [ -d "pig_ops/webroot/templates_backup" ]; then
    echo "Found templates backup, restoring..."
    
    # Clear current templates
    rm -f pig_ops/webroot/templates/*.html
    
    # Copy back from backup
    cp pig_ops/webroot/templates_backup/*.html pig_ops/webroot/templates/ 2>/dev/null || true
    check_success "Templates restored from backup"
else
    echo -e "${YELLOW}⚠️  No templates backup found - skipping restore${NC}"
fi

# 5️⃣ GIT PULL IN PIG_OPS (Backend)
section "STEP 5: Updating backend (pig_ops)"
if [ -d "pig_ops" ]; then
    cd pig_ops
    echo "Backend directory: $(pwd)"
    
    # Stash any local changes (optional)
    git stash > /dev/null 2>&1 || true
    
    echo "Pulling latest changes from Bitbucket..."
    git pull origin main
    check_success "Backend git pull completed"
    
    # Go back to project root
    cd /root/projects/jsys
else
    echo -e "${RED}❌ pig_ops directory not found!${NC}"
    exit 1
fi

# 6️⃣ MINIFY TEMPLATES
section "STEP 6: Minifying HTML templates"
if [ -f "pig_ops/webroot/scripts/minify_templates.py" ]; then
    cd pig_ops/webroot/scripts
    python3 minify_templates.py
    check_success "Templates minified"
    cd /root/projects/jsys
else
    echo -e "${YELLOW}⚠️  Minify script not found - skipping minification${NC}"
    echo "Expected at: pig_ops/webroot/scripts/minify_templates.py"
fi

# 7️⃣ START PYTHON APP (Detached)
section "STEP 7: Starting Python app in background"
cd pig_ops/webroot

# Activate virtual environment and start app
VENV_PATH="/root/projects/jsys/.venv"

if [ -f "$VENV_PATH/bin/activate" ]; then
    echo "Activating virtual environment..."
    source "$VENV_PATH/bin/activate"
    
    # Create logs directory if it doesn't exist
    mkdir -p logs
    
    # Get current date for log file
    LOG_FILE="logs/app_$(date +%Y%m%d_%H%M%S).log"
    
    echo "Starting app with nohup..."
    echo "Log file: $LOG_FILE"
    
    # Use nohup to run in background with venv python
    nohup "$VENV_PATH/bin/python" pig_ops_web.py > "$LOG_FILE" 2>&1 &
    APP_PID=$!
    
    # Deactivate venv (doesn't affect running process)
    deactivate 2>/dev/null || true
    
    # Give it a moment to start
    sleep 3
    
    # Check if process is still running
    if kill -0 $APP_PID 2>/dev/null; then
        echo -e "${GREEN}  ✅ App started with PID: $APP_PID${NC}"
        echo "  📝 Logs: /root/projects/jsys/pig_ops/webroot/$LOG_FILE"
        
        # Save PID to file
        echo $APP_PID > /root/projects/jsys/app.pid
        echo "  💾 PID saved to /root/projects/jsys/app.pid"
        
        # Quick health check
        echo "  🔍 Performing health check..."
        sleep 2
        if curl -s http://localhost:8000 > /dev/null 2>&1; then
            echo -e "${GREEN}  ✅ App is responding${NC}"
        else
            echo -e "${YELLOW}  ⚠️  App started but not responding - check logs:${NC}"
            echo "     tail -f $LOG_FILE"
        fi
        
        # Disown the process so it survives terminal close
        disown $APP_PID
    else
        echo -e "${RED}  ❌ App failed to start - check logs${NC}"
        tail -20 "$LOG_FILE"
        exit 1
    fi
else
    echo -e "${RED}  ❌ Virtual environment not found at $VENV_PATH${NC}"
    exit 1
fi


# Save PID to file
echo $APP_PID > /root/projects/jsys/app.pid
echo "  💾 PID saved to /root/projects/jsys/app.pid"

# Quick health check
echo "  🔍 Performing health check..."
sleep 5
if curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo -e "${GREEN}  ✅ App is responding${NC}"
else
    echo -e "${YELLOW}  ⚠️  App started but not responding - check logs:${NC}"
    echo "     tail -f /root/projects/jsys/pig_ops/webroot/$LOG_FILE"
fi

# After app starts, go back to project root
cd /root/projects/jsys


# 8️⃣ After starting the app, add:
if [ -f "pig_ops/webroot/scripts/manage_logs.py" ]; then
    cd pig_ops/webroot/scripts
    python3 manage_logs.py
    check_success "Logs managed"
    cd /root/projects/jsys
else
    echo -e "${YELLOW}⚠️  manage_logs.py not found - skipping log management${NC}"
fi


# 9️⃣ SUMMARY
section "✅ DEPLOYMENT COMPLETE"
echo -e "${GREEN}Started at: $(date)${NC}"
echo -e "${GREEN}Completed at: $(date)${NC}"
echo ""
echo "📊 Summary:"
echo "  • Frontend: Updated from Bitbucket"
echo "  • Backend: Updated from Bitbucket"
echo "  • Templates: Minified"
echo "  • App: Running in background (PID: $APP_PID)"
echo ""
echo "📝 Useful commands:"
echo "  • Check app status:     ps aux | grep python"
echo "  • View logs:            tail -f ~/projects/jsys/pig_ops/webroot/$LOG_FILE"
echo "  • Stop app manually:    pkill -f pig_ops_web.py"
echo "  • Run this script:      ./deploy.sh"
echo ""
echo -e "${GREEN}🐷 SuperPig is now live!${NC}"
