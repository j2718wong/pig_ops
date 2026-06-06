#!/bin/bash
# deploy.sh
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
if [ -d "$DEPLOY_LOG_DIR" ]; then
    LOG_COUNT=$(ls -1 "$DEPLOY_LOG_DIR"/deploy_*.log 2>/dev/null | wc -l)
    
    if [ "$LOG_COUNT" -gt 3 ]; then
        echo "🧹 Cleaning up old deployment logs (keeping last 3)..."
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

# ============= VERSION MANAGEMENT =============
VERSION_FILE="/root/projects/jsys/version.txt"
VERSION_ADMIN_FILE="/root/projects/jsys/version_admin.txt"

# Read current version (SPA)
read_version() {
    if [ -f "$VERSION_FILE" ]; then
        IFS='.' read -r MAJOR DB_VER BACKEND_VER FRONTEND_VER < "$VERSION_FILE"
    else
        MAJOR=1
        DB_VER=0
        BACKEND_VER=0
        FRONTEND_VER=0
        echo "$MAJOR.$DB_VER.$BACKEND_VER.$FRONTEND_VER" > "$VERSION_FILE"
    fi
}

# Write version back (SPA)
write_version() {
    echo "$MAJOR.$DB_VER.$BACKEND_VER.$FRONTEND_VER" > "$VERSION_FILE"
    log_message "📦 SPA version updated to: $MAJOR.$DB_VER.$BACKEND_VER.$FRONTEND_VER"
}

# Read admin version
read_admin_version() {
    if [ -f "$VERSION_ADMIN_FILE" ]; then
        IFS='.' read -r MAJOR DB_VER BACKEND_VER ADMIN_VER < "$VERSION_ADMIN_FILE"
    else
        MAJOR=1
        DB_VER=0
        BACKEND_VER=0
        ADMIN_VER=0
        echo "$MAJOR.$DB_VER.$BACKEND_VER.$ADMIN_VER" > "$VERSION_ADMIN_FILE"
    fi
}

# Write admin version back
write_admin_version() {
    echo "$MAJOR.$DB_VER.$BACKEND_VER.$ADMIN_VER" > "$VERSION_ADMIN_FILE"
    log_message "📦 Admin version updated to: $MAJOR.$DB_VER.$BACKEND_VER.$ADMIN_VER"
}

# Increment database version (shared between SPA and Admin)
inc_db_version() {
    read_version
    DB_VER=$((DB_VER + 1))
    write_version
    
    # Also update admin version with same DB_VER
    read_admin_version
    # Keep MAJOR, BACKEND_VER, ADMIN_VER same, update DB_VER
    echo "$MAJOR.$DB_VER.$BACKEND_VER.$ADMIN_VER" > "$VERSION_ADMIN_FILE"
    log_success "Database version incremented to $DB_VER (SPA & Admin)"
}

# Increment backend version (shared)
inc_backend_version() {
    read_version
    BACKEND_VER=$((BACKEND_VER + 1))
    write_version
    
    # Also update admin version with same BACKEND_VER
    read_admin_version
    echo "$MAJOR.$DB_VER.$BACKEND_VER.$ADMIN_VER" > "$VERSION_ADMIN_FILE"
    log_success "Backend version incremented to $BACKEND_VER (SPA & Admin)"
}

# Increment frontend version (SPA only)
inc_frontend_version() {
    read_version
    FRONTEND_VER=$((FRONTEND_VER + 1))
    write_version
    log_success "Frontend (SPA) version incremented to $FRONTEND_VER"
}

# Increment admin version (Admin only)
inc_admin_version() {
    read_admin_version
    ADMIN_VER=$((ADMIN_VER + 1))
    write_admin_version
    log_success "Admin version incremented to $ADMIN_VER"
}
# ================================================

# Initialize flags and store commit hashes
FRONTEND_CHANGED=false
BACKEND_CHANGED=false
ADMIN_CHANGED=false
BUILD_NEEDED=false
RESTART_NEEDED=false
FRONTEND_COMMIT=""
BACKEND_COMMIT=""
ADMIN_COMMIT=""
BKOPS_COMMIT=""

# Store app log file path for summary
APP_LOG_FILE=""

# 1️⃣ CHANGE TO PROJECT ROOT
section "STEP 1: Changing to project root"
cd /root/projects/jsys
echo "Current directory: $(pwd)"
check_success "Changed to project root"

# 2️⃣ FRONTEND: Git pull and build if changes
section "STEP 2: Updating frontend SPA (pig_ops_ui_mob)"
if [ -d "pig_ops_ui_mob" ]; then
    cd pig_ops_ui_mob
    
    BEFORE_HASH=$(git rev-parse HEAD)
    echo "Current frontend commit: ${BEFORE_HASH:0:7}"
    
    git stash > /dev/null 2>&1 || true
    
    echo "Pulling latest changes from Bitbucket..."
    git pull origin main
    
    AFTER_HASH=$(git rev-parse HEAD)
    FRONTEND_COMMIT="$AFTER_HASH"
    echo "New frontend commit: ${AFTER_HASH:0:7}"
    
    if [ "$BEFORE_HASH" != "$AFTER_HASH" ]; then
        FRONTEND_CHANGED=true
        BUILD_NEEDED=true
        RESTART_NEEDED=true
        log_success "Frontend changes detected (${BEFORE_HASH:0:7} → ${AFTER_HASH:0:7})"
        
        echo ""
        echo "📋 Frontend changes:"
        git log --oneline --decorate --stat HEAD@{1}..HEAD | head -10
    else
        log_success "No frontend changes detected (already up to date)"
        FRONTEND_COMMIT="$BEFORE_HASH"
    fi
    
    cd /root/projects/jsys
else
    log_error "pig_ops_ui_mob directory not found!"
    exit 1
fi

# 3️⃣ BUILD FRONTEND SPA (only if changes detected)
section "STEP 3: Building frontend SPA bundles"
if [ "$BUILD_NEEDED" = true ]; then
    cd pig_ops_ui_mob
    
    source /root/projects/jsys/.venv/bin/activate 2>/dev/null || true
    
    if [ -f "build.py" ]; then
        echo "Building JavaScript bundles (changes detected)..."
        
        echo "Running: python build.py --version"
        python build.py --version
        
        if [ $? -eq 0 ]; then
            log_success "Frontend SPA bundles built successfully"
            
            echo ""
            echo "📦 Generated files in static/js/:"
            ls -la static/js/ | grep -E "bundle.*\.min\.js|manifest\.json" | sed 's/^/   /'
            
            echo ""
            echo "📦 Generated files in static/css/:"
            ls -la static/css/ 2>/dev/null | grep -E "main.*\.min\.css|manifest\.json" | sed 's/^/   /' || echo "   No CSS files found"
            
            inc_frontend_version
        else
            log_error "Frontend SPA build failed!"
            exit 1
        fi
    else
        log_warning "build.py not found - skipping JS build"
    fi
    
    deactivate 2>/dev/null || true
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
    
    BEFORE_HASH=$(git rev-parse HEAD)
    echo "Current backend commit: ${BEFORE_HASH:0:7}"
    
    git stash > /dev/null 2>&1 || true
    
    echo "Pulling latest changes from Bitbucket..."
    git pull origin main
    
    AFTER_HASH=$(git rev-parse HEAD)
    BACKEND_COMMIT="$AFTER_HASH"
    echo "New backend commit: ${AFTER_HASH:0:7}"
    
    if [ "$BEFORE_HASH" != "$AFTER_HASH" ]; then
        BACKEND_CHANGED=true
        RESTART_NEEDED=true
        log_success "Backend changes detected (${BEFORE_HASH:0:7} → ${AFTER_HASH:0:7})"
        
        echo ""
        echo "📋 Backend changes:"
        git log --oneline --decorate --stat HEAD@{1}..HEAD | head -10
        
        inc_backend_version
    else
        log_success "No backend changes detected (already up to date)"
        BACKEND_COMMIT="$BEFORE_HASH"
    fi
    
    cd /root/projects/jsys
else
    log_error "pig_ops directory not found!"
    exit 1
fi

# ============= ADMIN APP: Git pull and build =============
section "STEP 5.1: Updating admin app (pig_ops_admin)"
ADMIN_DIR="/root/projects/jsys/pig_ops_admin"
if [ -d "$ADMIN_DIR" ]; then
    cd "$ADMIN_DIR"
    
    # Check if it's a git repo
    if [ -d ".git" ]; then
        BEFORE_HASH=$(git rev-parse HEAD 2>/dev/null || echo "no_commits")
        echo "Current admin commit: ${BEFORE_HASH:0:7}"
        
        echo "Pulling latest changes from Bitbucket..."
        git pull origin main 2>/dev/null || echo "   No changes or not a git repo"
        
        AFTER_HASH=$(git rev-parse HEAD 2>/dev/null || echo "no_commits")
        ADMIN_COMMIT="$AFTER_HASH"
        echo "New admin commit: ${AFTER_HASH:0:7}"
        
        if [ "$BEFORE_HASH" != "no_commits" ] && [ "$BEFORE_HASH" != "$AFTER_HASH" ]; then
            ADMIN_CHANGED=true
            RESTART_NEEDED=true  # Admin is separate, but templates may need refresh
            log_success "Admin changes detected (${BEFORE_HASH:0:7} → ${AFTER_HASH:0:7})"
        else
            log_success "No admin changes detected"
            ADMIN_COMMIT="$BEFORE_HASH"
        fi
    else
        log_warning "pig_ops_admin is not a git repository"
        ADMIN_COMMIT="no_git"
    fi
    
    # Build admin if changes detected OR build_admin.py exists and we want fresh build
    if [ "$ADMIN_CHANGED" = true ]; then
        echo "Building admin bundles..."
        
        source /root/projects/jsys/.venv/bin/activate 2>/dev/null || true
        
        if [ -f "build_admin.py" ]; then
            python build_admin.py --version
            if [ $? -eq 0 ]; then
                log_success "Admin JS bundles built successfully"
                inc_admin_version
            else
                log_error "Admin build failed!"
                exit 1
            fi
        else
            log_warning "build_admin.py not found - copying source directly"
            # Fallback: copy source file directly
            mkdir -p static/js
            cp src/static/js/admin_receipt_data_entry.js static/js/ 2>/dev/null || true
        fi
        
        deactivate 2>/dev/null || true
    else
        log_success "No admin changes - skipping admin build"
    fi
    
    cd /root/projects/jsys
else
    log_warning "pig_ops_admin directory not found at $ADMIN_DIR - skipping"
fi
# =========================================================

# ============= BACKGROUND OPS (pig_ops_bkops) =============
section "STEP 5.2: Updating background ops (pig_ops_bkops)"
BKOPs_DIR="/root/projects/jsys/pig_ops_bkops"
if [ -d "$BKOPs_DIR" ]; then
    cd "$BKOPs_DIR"
    
    BEFORE_HASH=$(git rev-parse HEAD 2>/dev/null || echo "no_commits")
    echo "Current bkops commit: ${BEFORE_HASH:0:7}"
    
    echo "Pulling latest changes from Bitbucket..."
    git pull origin main 2>/dev/null || echo "   No changes or not a git repo"
    
    AFTER_HASH=$(git rev-parse HEAD 2>/dev/null || echo "no_commits")
    BKOPS_COMMIT="$AFTER_HASH"
    echo "New bkops commit: ${AFTER_HASH:0:7}"
    
    if [ "$BEFORE_HASH" != "no_commits" ] && [ "$BEFORE_HASH" != "$AFTER_HASH" ]; then
        log_success "Background ops changes detected (${BEFORE_HASH:0:7} → ${AFTER_HASH:0:7})"
    else
        log_success "No background ops changes detected"
        BKOPS_COMMIT="$BEFORE_HASH"
    fi
    
    cd /root/projects/jsys
else
    log_warning "pig_ops_bkops directory not found at $BKOPs_DIR - skipping"
fi
# =========================================================

# 5.3️⃣ INSTALL/UPDATE PYTHON PACKAGES
section "STEP 5.3: Installing/updating Python packages"
cd pig_ops

if [ -f "requirements.txt" ]; then
    source /root/projects/jsys/.venv/bin/activate
    
    echo "Checking for Python package changes..."
    
    REQ_HASH_FILE="/root/projects/jsys/.requirements_hash"
    CURRENT_HASH=$(md5sum requirements.txt | cut -d' ' -f1)
    
    if [ -f "$REQ_HASH_FILE" ] && [ "$(cat $REQ_HASH_FILE)" = "$CURRENT_HASH" ]; then
        echo "✅ requirements.txt unchanged - skipping package installation"
    else
        echo "📦 requirements.txt changed - installing/updating packages..."
        
        pip install --upgrade -r requirements.txt
        
        echo "$CURRENT_HASH" > "$REQ_HASH_FILE"
        log_success "Python packages updated"
    fi
    
    deactivate
else
    log_warning "requirements.txt not found - skipping package installation"
fi

cd /root/projects/jsys
# =========================================================

# ============= RUN DATABASE MIGRATIONS =============
section "STEP 5.4: Running database migrations"

DB_REPO_DIR="/root/projects/jsys/pig_ops_db"
MIGRATION_APPLIED_FILE="/root/.db_migrations_prod_last_run"
OLD_TIMESTAMP=""

if [ -f "$MIGRATION_APPLIED_FILE" ]; then
    OLD_TIMESTAMP=$(cat "$MIGRATION_APPLIED_FILE")
fi

if [ -d "$DB_REPO_DIR" ]; then
    cd "$DB_REPO_DIR"
    
    echo "Pulling latest database changes from Bitbucket..."
    git pull origin main
    check_success "Database git pull completed"
    
    if [ -f "migrate.sh" ]; then
        echo "Running database migrations..."
        
        set +e
        ./migrate.sh prod
        MIGRATION_EXIT=$?
        set -e
        
        NEW_TIMESTAMP=""
        if [ -f "$MIGRATION_APPLIED_FILE" ]; then
            NEW_TIMESTAMP=$(cat "$MIGRATION_APPLIED_FILE")
        fi
        
        if [ $MIGRATION_EXIT -eq 0 ]; then
            if [ "$OLD_TIMESTAMP" != "$NEW_TIMESTAMP" ]; then
                log_success "Database migrations applied"
                inc_db_version
            else
                log_success "No new migrations to apply"
            fi
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

# 🔟 SHOW APP LOG PREVIEW
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
    echo "📋 Last 20 lines of current app log:"
    echo "----------------------------------------"
    tail -20 "pig_ops/webroot/logs/current.log" 2>/dev/null | sed 's/^/   /' || echo "   No logs available"
    echo "----------------------------------------"
    echo ""
    echo "🔍 To follow logs in real-time:"
    echo "   tail -f /root/projects/jsys/pig_ops/webroot/logs/current.log"
else
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

# Read final versions
FINAL_SPA_VERSION=$(cat "$VERSION_FILE" 2>/dev/null || echo "1.0.0.0")
FINAL_ADMIN_VERSION=$(cat "$VERSION_ADMIN_FILE" 2>/dev/null || echo "1.0.0.0")

echo -e "${GREEN}Started at: $(date)${NC}"
echo -e "${GREEN}Completed at: $(date)${NC}"
echo ""

# Read final versions for summary
read_version
read_admin_version

echo "📊 Summary:"
echo "  • Frontend changes (SPA): $FRONTEND_CHANGED"
echo "  • Frontend build (SPA): $BUILD_NEEDED"
echo "  • Backend changes: $BACKEND_CHANGED"
echo "  • Admin changes: $ADMIN_CHANGED"
echo "  • Background ops pull: performed"
echo "  • Database migrations: applied"
echo "  • Restart performed: $RESTART_NEEDED"
echo ""
echo "📦 Version Numbers:"
echo "  • SPA Version:   $FINAL_SPA_VERSION"
echo "  • Admin Version: $FINAL_ADMIN_VERSION"

if [ "$RESTART_NEEDED" = true ]; then
    echo ""
    echo "  • App PID: $APP_PID"
    echo "  • App log: /root/projects/jsys/pig_ops/webroot/$APP_LOG_FILE"
    echo "  • App log symlink: logs/current.log"
else
    echo ""
    CURRENT_PID=$(pgrep -f "python.*pig_ops_web.py" | head -1)
    if [ -n "$CURRENT_PID" ]; then
        echo "  • App PID: $CURRENT_PID"
    fi
fi

echo ""
echo "📝 Git Commit Hashes:"
echo "  • Frontend (SPA):   ${FRONTEND_COMMIT:0:8}"
echo "  • Backend:          ${BACKEND_COMMIT:0:8}"
echo "  • Admin:            ${ADMIN_COMMIT:0:8}"
echo "  • Background Ops:   ${BKOPS_COMMIT:0:8}"
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
echo "   Frontend changed (SPA): $FRONTEND_CHANGED" >> "$DEPLOY_LOG_FILE"
echo "   Backend changed: $BACKEND_CHANGED" >> "$DEPLOY_LOG_FILE"
echo "   Admin changed: $ADMIN_CHANGED" >> "$DEPLOY_LOG_FILE"
echo "   Frontend commit: ${FRONTEND_COMMIT:0:8}" >> "$DEPLOY_LOG_FILE"
echo "   Backend commit: ${BACKEND_COMMIT:0:8}" >> "$DEPLOY_LOG_FILE"
echo "   Admin commit: ${ADMIN_COMMIT:0:8}" >> "$DEPLOY_LOG_FILE"
echo "   Background ops commit: ${BKOPS_COMMIT:0:8}" >> "$DEPLOY_LOG_FILE"
echo "   SPA Version: $MAJOR.$DB_VER.$BACKEND_VER.$FRONTEND_VER" >> "$DEPLOY_LOG_FILE"
echo "   Admin Version: $MAJOR.$DB_VER.$BACKEND_VER.$ADMIN_VER" >> "$DEPLOY_LOG_FILE"
echo "   Restart needed: $RESTART_NEEDED" >> "$DEPLOY_LOG_FILE"
echo "========================================" >> "$DEPLOY_LOG_FILE"

# Force log rotation
cd "$DEPLOY_LOG_DIR"
ls -1t deploy_*.log 2>/dev/null | tail -n +4 | while read old_log; do
    rm -f "$old_log"
done
cd /root/projects/jsys
