#!/bin/bash
# SuperPig Complete Deployment Script
# Run this whenever you need to deploy updates

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

# ============= LOG ROTATION: KEEP ONLY LAST 3 =============
# Delete old deployment logs, keep only the 3 most recent
if [ -d "$DEPLOY_LOG_DIR" ]; then
    # Count number of log files (excluding latest symlink)
    LOG_COUNT=$(ls -1 "$DEPLOY_LOG_DIR"/deploy_*.log 2>/dev/null | wc -l)
    
    if [ "$LOG_COUNT" -gt 3 ]; then
        echo "🧹 Cleaning up old deployment logs (keeping last 3)..."
        # List files by modification time, skip the newest 3, delete the rest
        ls -1t "$DEPLOY_LOG_DIR"/deploy_*.log 2>/dev/null | tail -n +4 | while read old_log; do
            echo "   Removing: $(basename "$old_log")"
            rm -f "$old_log"
        done
        echo ""
    fi
fi
# =======================================================

TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")
DEPLOY_LOG_FILE="$DEPLOY_LOG_DIR/deploy_$TIMESTAMP.log"
LATEST_LOG_LINK="$DEPLOY_LOG_DIR/latest.log"

# Function to log messages
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

ln -sf "$DEPLOY_LOG_FILE" "$LATEST_LOG_LINK"
exec > >(tee -a "$DEPLOY_LOG_FILE") 2>&1
# ===================================================

echo -e "${BLUE}================================${NC}"
echo -e "${GREEN}🐷 SuperPig Deployment Script${NC}"
echo -e "${BLUE}================================${NC}"
echo "Started at: $(date)"
echo "Deployment log: $DEPLOY_LOG_FILE"
echo "Keeping last 3 deployment logs only"
echo ""

# Override functions for logging
section() { log_section "$1"; }
check_success() { if [ $? -eq 0 ]; then log_success "$1"; else log_error "$1"; exit 1; fi; }

# Initialize flags and store commit hashes
FRONTEND_CHANGED=false
BACKEND_CHANGED=false
BUILD_NEEDED=false
RESTART_NEEDED=false
FRONTEND_COMMIT=""
BACKEND_COMMIT=""

# Store app log file path for summary
APP_LOG_FILE=""

# 1️⃣ CHANGE TO PROJECT ROOT
section "STEP 1: Changing to project root"
cd /root/projects/jsys
echo "Current directory: $(pwd)"
check_success "Changed to project root"

# 2️⃣ FRONTEND: Git pull and build if changes
section "STEP 2: Updating frontend (pig_ops_ui_mob)"
if [ -d "pig_ops_ui_mob" ]; then
    cd pig_ops_ui_mob
    
    # Get current commit hash before pull
    BEFORE_HASH=$(git rev-parse HEAD)
    echo "Current frontend commit: ${BEFORE_HASH:0:7}"
    
    # Stash any local changes (optional)
    git stash > /dev/null 2>&1 || true
    
    echo "Pulling latest changes from Bitbucket..."
    git pull origin main
    
    # Get new commit hash after pull
    AFTER_HASH=$(git rev-parse HEAD)
    FRONTEND_COMMIT="$AFTER_HASH"
    echo "New frontend commit: ${AFTER_HASH:0:7}"
    
    # Check if changes were pulled
    if [ "$BEFORE_HASH" != "$AFTER_HASH" ]; then
        FRONTEND_CHANGED=true
        BUILD_NEEDED=true
        RESTART_NEEDED=true  # Frontend changes affect templates, so restart needed
        log_success "Frontend changes detected (${BEFORE_HASH:0:7} → ${AFTER_HASH:0:7})"
        
        # Show summary of changes
        echo ""
        echo "📋 Frontend changes:"
        git log --oneline --decorate --stat HEAD@{1}..HEAD | head -10
    else
        log_success "No frontend changes detected (already up to date)"
        FRONTEND_COMMIT="$BEFORE_HASH"
    fi
    
    # Go back to project root
    cd /root/projects/jsys
else
    log_error "pig_ops_ui_mob directory not found!"
    exit 1
fi

# 3️⃣ BUILD FRONTEND (only if changes detected)
section "STEP 3: Building frontend JS bundles"
if [ "$BUILD_NEEDED" = true ]; then
    cd pig_ops_ui_mob
    
    # Activate virtual environment
    source /root/projects/jsys/.venv/bin/activate 2>/dev/null || true
    
    if [ -f "build.py" ]; then
        echo "Building JavaScript bundles (changes detected)..."
        
        # Build with versioning
        echo "Running: python build.py --version"
        python build.py --version
        
        if [ $? -eq 0 ]; then
            log_success "Frontend JS bundles built successfully"
            
            # Show generated files
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
        log_warning "build.py not found - skipping JS build"
    fi
    
    # Deactivate virtual environment
    deactivate 2>/dev/null || true
    
    # Go back to project root
    cd /root/projects/jsys
else
    log_success "No frontend changes - skipping build"
fi

# 4️⃣ RESTORE TEMPLATES (only if frontend changed)
if [ "$FRONTEND_CHANGED" = true ]; then
    section "STEP 4: Restoring templates from backup"
    if [ -d "pig_ops/webroot/templates_backup" ]; then
        echo "Frontend changed, restoring templates backup..."
        rm -f pig_ops/webroot/templates/*.html
        cp pig_ops/webroot/templates_backup/*.html pig_ops/webroot/templates/ 2>/dev/null || true
        check_success "Templates restored from backup"
    else
        log_warning "No templates backup found - skipping restore"
    fi
fi

# 5️⃣ BACKEND: Git pull and check for changes
section "STEP 5: Updating backend (pig_ops)"
if [ -d "pig_ops" ]; then
    cd pig_ops
    
    # Get current commit hash before pull
    BEFORE_HASH=$(git rev-parse HEAD)
    echo "Current backend commit: ${BEFORE_HASH:0:7}"
    
    # Stash any local changes (optional)
    git stash > /dev/null 2>&1 || true
    
    echo "Pulling latest changes from Bitbucket..."
    git pull origin main
    
    # Get new commit hash after pull
    AFTER_HASH=$(git rev-parse HEAD)
    BACKEND_COMMIT="$AFTER_HASH"
    echo "New backend commit: ${AFTER_HASH:0:7}"
    
    # Check if changes were pulled
    if [ "$BEFORE_HASH" != "$AFTER_HASH" ]; then
        BACKEND_CHANGED=true
        RESTART_NEEDED=true
        log_success "Backend changes detected (${BEFORE_HASH:0:7} → ${AFTER_HASH:0:7})"
        
        # Show summary of changes
        echo ""
        echo "📋 Backend changes:"
        git log --oneline --decorate --stat HEAD@{1}..HEAD | head -10
    else
        log_success "No backend changes detected (already up to date)"
        BACKEND_COMMIT="$BEFORE_HASH"
    fi
    
    # Go back to project root
    cd /root/projects/jsys
else
    log_error "pig_ops directory not found!"
    exit 1
fi

# ============= NEW: INSTALL/UPDATE PYTHON PACKAGES =============
section "STEP 5.5: Installing/updating Python packages"
cd pig_ops

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    # Activate virtual environment
    source /root/projects/jsys/.venv/bin/activate
    
    echo "Checking for Python package changes..."
    
    # Check if requirements.txt has changed since last deploy
    REQ_HASH_FILE="/root/projects/jsys/.requirements_hash"
    CURRENT_HASH=$(md5sum requirements.txt | cut -d' ' -f1)
    
    if [ -f "$REQ_HASH_FILE" ] && [ "$(cat $REQ_HASH_FILE)" = "$CURRENT_HASH" ]; then
        echo "✅ requirements.txt unchanged - skipping package installation"
    else
        echo "📦 requirements.txt changed - installing/updating packages..."
        echo "   This may take a moment..."
        
        # Install/update packages from requirements.txt
        pip install --upgrade -r requirements.txt
        
        # Show what was installed (optional)
        echo "   Latest packages installed:"
        pip list | grep -E "$(cat requirements.txt | grep -v '^#' | cut -d'=' -f1 | tr '\n' '|' | sed 's/|$//')" 2>/dev/null || true
        
        # Save hash for next run
        echo "$CURRENT_HASH" > "$REQ_HASH_FILE"
        log_success "Python packages updated"
    fi
    
    # Deactivate virtual environment
    deactivate
else
    log_warning "requirements.txt not found - skipping package installation"
fi

cd /root/projects/jsys
# =============================================================


# Find the pig_ops_db repo
DB_REPO_DIR="/root/projects/jsys/pig_ops_db"
# ============= NEW: RUN DATABASE MIGRATIONS =============
section "STEP 5.6: Running database migrations"

# Find the pig_ops_db repo
DB_REPO_DIR="/root/projects/jsys/pig_ops_db"
if [ -d "$DB_REPO_DIR" ]; then
    cd "$DB_REPO_DIR"
    
    # Pull latest database changes
    echo "Pulling latest database changes from Bitbucket..."
    git pull origin main
    check_success "Database git pull completed"
    
    # Run migrations for production
    if [ -f "migrate.sh" ]; then
        echo "Running database migrations..."
        
        # Temporarily disable exit-on-error to prevent migration from killing script
        set +e
        ./migrate.sh prod
        MIGRATION_EXIT=$?
        set -e
        
        if [ $MIGRATION_EXIT -eq 0 ]; then
            log_success "Database migrations applied"
        else
            log_error "Database migrations failed (exit code: $MIGRATION_EXIT)"
            exit 1
        fi
    else
        log_warning "migrate.sh not found in $DB_REPO_DIR"
    fi
    
    cd /root/projects/jsys
else
    log_warning "pig_ops_db directory not found at $DB_REPO_DIR"
fi
# =========================================================

# 6️⃣ MINIFY TEMPLATES (only if backend changed OR frontend changed)
if [ "$RESTART_NEEDED" = true ]; then
    section "STEP 6: Minifying HTML templates"
    if [ -f "pig_ops/webroot/scripts/minify_templates.py" ]; then
        cd pig_ops/webroot/scripts
        python3 minify_templates.py
        check_success "Templates minified"
        cd /root/projects/jsys
    else
        log_warning "Minify script not found - skipping minification"
    fi
fi

# 7️⃣ STOP PYTHON APP (only if restart needed)
if [ "$RESTART_NEEDED" = true ]; then
    section "STEP 7: Stopping Python app"
    echo "Looking for running pig_ops_web.py processes..."
    
    PIDS=$(pgrep -f "python.*pig_ops_web.py" || true)
    if [ -n "$PIDS" ]; then
        echo "Found PIDs: $PIDS"
        kill $PIDS 2>/dev/null || true
        sleep 2
        if pgrep -f "python.*pig_ops_web.py" > /dev/null; then
            echo "Process still running, force killing..."
            pkill -9 -f "python.*pig_ops_web.py" || true
        fi
        log_success "Python app stopped"
    else
        log_warning "No running Python app found"
    fi
else
    log_success "No changes requiring restart - app remains running"
fi

# 8️⃣ START PYTHON APP (only if restart needed)
if [ "$RESTART_NEEDED" = true ]; then
    section "STEP 8: Starting Python app in background"
    cd pig_ops/webroot
    
    VENV_PATH="/root/projects/jsys/.venv"
    
    if [ -f "$VENV_PATH/bin/activate" ]; then
        echo "Activating virtual environment..."
        source "$VENV_PATH/bin/activate"
        
        mkdir -p logs
        APP_LOG_FILE="logs/app_$(date +%Y%m%d_%H%M%S).log"
        
        echo "Starting app with nohup..."
        echo "App log file: $APP_LOG_FILE"
        
        nohup "$VENV_PATH/bin/python" pig_ops_web.py > "$APP_LOG_FILE" 2>&1 &
        APP_PID=$!
        
        deactivate 2>/dev/null || true
        sleep 3
        
        if kill -0 $APP_PID 2>/dev/null; then
            log_success "App started with PID: $APP_PID"
            echo "  📝 App logs: /root/projects/jsys/pig_ops/webroot/$APP_LOG_FILE"
            echo $APP_PID > /root/projects/jsys/app.pid
            echo "  💾 PID saved"
            
            # 🔗 CREATE SYMLINK TO CURRENT APP LOG (FIX)
            cd logs
            ln -sf "$(basename "$APP_LOG_FILE")" current.log
            cd ..
            echo "  🔗 Created symlink: logs/current.log -> $APP_LOG_FILE"
            
            echo "  🔍 Health check (waiting 10 seconds)..."
            sleep 10
            if curl -s http://localhost:8000 > /dev/null 2>&1; then
                log_success "App is responding"
            else
                log_warning "App started but not responding - check logs"
            fi
            
            disown $APP_PID
        else
            log_error "App failed to start"
            tail -20 "$APP_LOG_FILE"
            exit 1
        fi
    else
        log_error "Virtual environment not found"
        exit 1
    fi
    
    cd /root/projects/jsys
else
    log_success "No restart needed - app continues running"
fi

# 9️⃣ MANAGE LOGS (always run)
section "STEP 9: Managing logs"
if [ -f "pig_ops/webroot/scripts/manage_logs.py" ]; then
    cd pig_ops/webroot/scripts
    python3 manage_logs.py
    check_success "Logs managed"
    cd /root/projects/jsys
else
    log_warning "manage_logs.py not found - skipping log management"
fi

# 🔟 SHOW APP LOG PREVIEW (always show if app is running)
section "STEP 10: App Log Preview"
if [ -n "$APP_LOG_FILE" ] && [ -f "pig_ops/webroot/$APP_LOG_FILE" ]; then
    echo "📋 Last 20 lines of app log ($APP_LOG_FILE):"
    echo "----------------------------------------"
    tail -20 "pig_ops/webroot/$APP_LOG_FILE" | sed 's/^/   /'
    echo "----------------------------------------"
    echo ""
    echo "🔍 To follow logs in real-time:"
    echo "   tail -f /root/projects/jsys/pig_ops/webroot/logs/current.log"
elif [ -f "pig_ops/webroot/logs/current.log" ]; then
    # Fallback to current.log symlink if exists
    echo "📋 Last 20 lines of current app log:"
    echo "----------------------------------------"
    tail -20 "pig_ops/webroot/logs/current.log" 2>/dev/null | sed 's/^/   /' || echo "   No logs available"
    echo "----------------------------------------"
    echo ""
    echo "🔍 To follow logs in real-time:"
    echo "   tail -f /root/projects/jsys/pig_ops/webroot/logs/current.log"
else
    # Try to find the most recent log file
    LATEST_LOG=$(ls -t /root/projects/jsys/pig_ops/webroot/logs/app_*.log 2>/dev/null | head -1)
    if [ -n "$LATEST_LOG" ]; then
        echo "📋 Last 20 lines of most recent log ($(basename "$LATEST_LOG")):"
        echo "----------------------------------------"
        tail -20 "$LATEST_LOG" | sed 's/^/   /'
        echo "----------------------------------------"
        echo ""
        echo "🔍 To follow logs in real-time:"
        echo "   tail -f $LATEST_LOG"
    else
        echo "   No app logs found"
    fi
fi

# 1️⃣1️⃣ SUMMARY
section "✅ DEPLOYMENT COMPLETE"
echo -e "${GREEN}Started at: $(date)${NC}"
echo -e "${GREEN}Completed at: $(date)${NC}"
echo ""
echo "📊 Summary:"
echo "  • Frontend changes: $FRONTEND_CHANGED"
echo "  • Frontend build: $BUILD_NEEDED"
echo "  • Backend changes: $BACKEND_CHANGED"
echo "  • Database migrations: applied"
echo "  • Restart performed: $RESTART_NEEDED"
if [ "$RESTART_NEEDED" = true ]; then
    echo "  • App PID: $APP_PID"
    echo "  • App log: /root/projects/jsys/pig_ops/webroot/$APP_LOG_FILE"
    echo "  • App log symlink: logs/current.log"
else
    echo "  • App: Already running (no changes)"
    # Find current app PID
    CURRENT_PID=$(pgrep -f "python.*pig_ops_web.py" | head -1)
    if [ -n "$CURRENT_PID" ]; then
        echo "  • App PID: $CURRENT_PID"
    fi
fi
echo ""
echo "📝 Git Commit Hashes:"
echo "  • Frontend: ${FRONTEND_COMMIT:0:8}"
echo "  • Backend:  ${BACKEND_COMMIT:0:8}"
echo ""
echo "📝 Deployment Logs:"
echo "  • This log: $DEPLOY_LOG_FILE"
echo "  • Latest: $LATEST_LOG_LINK"
echo "  • Only last 3 logs are kept automatically"
echo ""
echo "📝 Quick Commands:"
echo "  • Follow app log:    tail -f /root/projects/jsys/pig_ops/webroot/logs/current.log"
echo "  • Check app status:  ps aux | grep python"
echo "  • Stop app:          pkill -f pig_ops_web.py"
echo "  • Deploy again:      ./deploy.sh"
echo ""

# Record final status in log
echo "" >> "$DEPLOY_LOG_FILE"
echo "========================================" >> "$DEPLOY_LOG_FILE"
echo "✅ Deployment completed at $(date)" >> "$DEPLOY_LOG_FILE"
echo "   Frontend changed: $FRONTEND_CHANGED" >> "$DEPLOY_LOG_FILE"
echo "   Backend changed: $BACKEND_CHANGED" >> "$DEPLOY_LOG_FILE"
echo "   Frontend commit: ${FRONTEND_COMMIT:0:8}" >> "$DEPLOY_LOG_FILE"
echo "   Backend commit: ${BACKEND_COMMIT:0:8}" >> "$DEPLOY_LOG_FILE"
echo "   Restart needed: $RESTART_NEEDED" >> "$DEPLOY_LOG_FILE"
echo "========================================" >> "$DEPLOY_LOG_FILE"

# Force log rotation by removing any remaining old logs that might have been missed
# This runs again to ensure only 3 remain
cd "$DEPLOY_LOG_DIR"
ls -1t deploy_*.log 2>/dev/null | tail -n +4 | while read old_log; do
    rm -f "$old_log"
done
cd /root/projects/jsys
