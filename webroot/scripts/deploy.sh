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

# ============= DEPLOYMENT LOGGING SETUP =============
DEPLOY_LOG_DIR="/root/projects/jsys/deploy_logs"
mkdir -p "$DEPLOY_LOG_DIR"

# Create log filename with timestamp (YYYY-MM-DD_HHMMSS)
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")
DEPLOY_LOG_FILE="$DEPLOY_LOG_DIR/deploy_$TIMESTAMP.log"

# Also create a symlink to latest log for easy access
LATEST_LOG_LINK="$DEPLOY_LOG_DIR/latest.log"

# Function to log messages to both console and log file
log_message() {
    echo -e "$1" | tee -a "$DEPLOY_LOG_FILE"
}

# Function to log section headers
log_section() {
    log_message ""
    log_message "${YELLOW}▶ $1${NC}"
    log_message "----------------------------------------"
}

# Function to log success/failure
log_success() {
    log_message "${GREEN}  ✅ $1${NC}"
}

log_error() {
    log_message "${RED}  ❌ $1${NC}"
}

log_warning() {
    log_message "${YELLOW}  ⚠️  $1${NC}"
}

# Start logging
{
    echo "========================================"
    echo "🐷 SuperPig Deployment Log - $TIMESTAMP"
    echo "========================================"
    echo ""
} >> "$DEPLOY_LOG_FILE"

# Create symlink to this deployment as latest
ln -sf "$DEPLOY_LOG_FILE" "$LATEST_LOG_LINK"

# Redirect all output to both console and log file
# This ensures EVERYTHING gets logged
exec > >(tee -a "$DEPLOY_LOG_FILE") 2>&1
# ===================================================

echo -e "${BLUE}================================${NC}"
echo -e "${GREEN}🐷 SuperPig Deployment Script${NC}"
echo -e "${BLUE}================================${NC}"
echo "Started at: $(date)"
echo "Deployment log: $DEPLOY_LOG_FILE"
echo ""

# Override section function to use logging
section() {
    log_section "$1"
}

# Override check_success function to use logging
check_success() {
    if [ $? -eq 0 ]; then
        log_success "$1"
    else
        log_error "$1"
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
    sleep 2
    # Check if still running and force kill if needed
    if pgrep -f "python.*pig_ops_web.py" > /dev/null; then
        echo "Process still running, force killing..."
        pkill -9 -f "python.*pig_ops_web.py" || true
    fi
    log_success "Python app stopped"
else
    log_warning "No running Python app found"
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
    log_error "pig_ops_ui_mob directory not found!"
    exit 1
fi

# ===== NEW: BUILD FRONTEND JS BUNDLES =====
section "STEP 3.5: Building frontend JS bundles"
if [ -d "pig_ops_ui_mob" ]; then
    cd pig_ops_ui_mob
    
    # Activate virtual environment for Python dependencies (csscompressor)
    source /root/projects/jsys/.venv/bin/activate 2>/dev/null || true
    
    # Check if build.py exists
    if [ -f "build.py" ]; then
        echo "Found build.py, building JavaScript bundles..."
        
        # Install CSS compressor if needed (quietly)
        pip install csscompressor > /dev/null 2>&1 || true
        
        # Build with versioning (production mode)
        echo "Running: python build.py --version"
        python build.py --version
        
        # Check if build was successful
        if [ $? -eq 0 ]; then
            log_success "Frontend JS bundles built successfully"
            
            # Show the generated files
            echo ""
            echo "📦 Generated files in static/js/:"
            ls -la static/js/ | grep -E "bundle.*\.min\.js|manifest\.json" | sed 's/^/   /'
            
            echo ""
            echo "📦 Generated files in static/css/:"
            ls -la static/css/ 2>/dev/null | grep -E "main.*\.min\.css|manifest\.json" | sed 's/^/   /' || echo "   No CSS files found"
        else
            log_error "Frontend build failed!"
            exit 1
        fi
    else
        log_warning "build.py not found in pig_ops_ui_mob - skipping JS build"
    fi
    
    # Deactivate virtual environment
    deactivate 2>/dev/null || true
    
    # Go back to project root
    cd /root/projects/jsys
else
    log_warning "pig_ops_ui_mob directory not found - skipping JS build"
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
    log_warning "No templates backup found - skipping restore"
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
    log_error "pig_ops directory not found!"
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
    log_warning "Minify script not found - skipping minification"
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
    
    # Get current date for app log file (separate from deploy log)
    APP_LOG_FILE="logs/app_$(date +%Y%m%d_%H%M%S).log"
    
    echo "Starting app with nohup..."
    echo "App log file: $APP_LOG_FILE"
    
    # Use nohup to run in background with venv python
    nohup "$VENV_PATH/bin/python" pig_ops_web.py > "$APP_LOG_FILE" 2>&1 &
    APP_PID=$!
    
    # Deactivate venv (doesn't affect running process)
    deactivate 2>/dev/null || true
    
    # Give it a moment to start
    sleep 3
    
    # Check if process is still running
    if kill -0 $APP_PID 2>/dev/null; then
        log_success "App started with PID: $APP_PID"
        echo "  📝 App logs: /root/projects/jsys/pig_ops/webroot/$APP_LOG_FILE"
        
        # Save PID to file
        echo $APP_PID > /root/projects/jsys/app.pid
        echo "  💾 PID saved to /root/projects/jsys/app.pid"
        
        # Quick health check - wait longer for app to initialize
        echo "  🔍 Performing health check (waiting 10 seconds)..."
        sleep 10
        if curl -s http://localhost:8000 > /dev/null 2>&1; then
            log_success "App is responding"
        else
            log_warning "App started but not responding - check app logs:"
            echo "     tail -f $APP_LOG_FILE"
            echo "     Last 20 lines of app log:"
            tail -20 "$APP_LOG_FILE" | sed 's/^/       /'
        fi
        
        # Disown the process so it survives terminal close
        disown $APP_PID
    else
        log_error "App failed to start - check app logs"
        tail -20 "$APP_LOG_FILE"
        exit 1
    fi
else
    log_error "Virtual environment not found at $VENV_PATH"
    exit 1
fi

# After app starts, go back to project root
cd /root/projects/jsys

# 8️⃣ MANAGE LOGS
section "STEP 8: Managing logs"
if [ -f "pig_ops/webroot/scripts/manage_logs.py" ]; then
    cd pig_ops/webroot/scripts
    python3 manage_logs.py
    check_success "Logs managed"
    cd /root/projects/jsys
else
    log_warning "manage_logs.py not found - skipping log management"
fi

# 9️⃣ SUMMARY
section "✅ DEPLOYMENT COMPLETE"
echo -e "${GREEN}Started at: $(date)${NC}"
echo -e "${GREEN}Completed at: $(date)${NC}"
echo ""
echo "📊 Summary:"
echo "  • Frontend: Updated from Bitbucket"
echo "  • Frontend JS: Built with versioning"
echo "  • Backend: Updated from Bitbucket"
echo "  • Templates: Minified"
echo "  • App: Running in background (PID: $APP_PID)"
echo ""
echo "📝 Deployment Logs:"
echo "  • This deployment log: $DEPLOY_LOG_FILE"
echo "  • Latest log symlink: $LATEST_LOG_LINK"
echo "  • View with: cat $LATEST_LOG_LINK"
echo ""
echo "📝 App Logs:"
echo "  • Current app log: /root/projects/jsys/pig_ops/webroot/$APP_LOG_FILE"
echo "  • View with: tail -f /root/projects/jsys/pig_ops/webroot/$APP_LOG_FILE"
echo ""
echo "📝 Useful commands:"
echo "  • Check app status:     ps aux | grep python"
echo "  • View deployment history: ls -la $DEPLOY_LOG_DIR"
echo "  • Stop app manually:    pkill -f pig_ops_web.py"
echo "  • Run this script:      ./deploy.sh"
echo ""
echo -e "${GREEN}🐷 SuperPig is now live!${NC}"

# Record final status in log
echo ""
echo "========================================" >> "$DEPLOY_LOG_FILE"
echo "✅ Deployment completed at $(date)" >> "$DEPLOY_LOG_FILE"
echo "========================================" >> "$DEPLOY_LOG_FILE"
