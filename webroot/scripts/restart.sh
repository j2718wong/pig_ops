#!/bin/bash
# SuperPig Restart Script
# Just stops and starts the Python app - no code updates

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============= RESTART LOGGING SETUP =============
RESTART_LOG_DIR="/root/projects/jsys/restart_logs"
mkdir -p "$RESTART_LOG_DIR"

# Log rotation: keep only last 3 restart logs
if [ -d "$RESTART_LOG_DIR" ]; then
    LOG_COUNT=$(ls -1 "$RESTART_LOG_DIR"/restart_*.log 2>/dev/null | wc -l)
    if [ "$LOG_COUNT" -gt 3 ]; then
        echo "🧹 Cleaning up old restart logs (keeping last 3)..."
        ls -1t "$RESTART_LOG_DIR"/restart_*.log 2>/dev/null | tail -n +4 | while read old_log; do
            echo "   Removing: $(basename "$old_log")"
            rm -f "$old_log"
        done
        echo ""
    fi
fi

TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")
RESTART_LOG_FILE="$RESTART_LOG_DIR/restart_$TIMESTAMP.log"
LATEST_LOG_LINK="$RESTART_LOG_DIR/latest.log"

# Function to log messages
log_message() {
    echo -e "$1" | tee -a "$RESTART_LOG_FILE"
}

# Start logging
{
    echo "========================================"
    echo "🐷 SuperPig Restart Log - $TIMESTAMP"
    echo "========================================"
    echo ""
} >> "$RESTART_LOG_FILE"

ln -sf "$RESTART_LOG_FILE" "$LATEST_LOG_LINK"
exec > >(tee -a "$RESTART_LOG_FILE") 2>&1
# ===================================================

echo -e "${BLUE}================================${NC}"
echo -e "${GREEN}🐷 SuperPig Restart Script${NC}"
echo -e "${BLUE}================================${NC}"
echo "Started at: $(date)"
echo "Restart log: $RESTART_LOG_FILE"
echo ""

# 1️⃣ STOP THE PYTHON APP
echo "▶ STEP 1: Stopping Python app"
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
    echo -e "${GREEN}  ✅ Python app stopped${NC}"
else
    echo -e "${YELLOW}  ⚠️  No running Python app found${NC}"
fi

# 2️⃣ START PYTHON APP (Detached)
echo ""
echo "▶ STEP 2: Starting Python app in background"

cd /root/projects/jsys/pig_ops/webroot

VENV_PATH="/root/projects/jsys/.venv"

if [ -f "$VENV_PATH/bin/activate" ]; then
    echo "Activating virtual environment..."
    source "$VENV_PATH/bin/activate"
    
    # Create logs directory if it doesn't exist
    mkdir -p logs
    
    # Get current date for app log file
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
        echo -e "${GREEN}  ✅ App started with PID: $APP_PID${NC}"
        echo "  📝 App logs: /root/projects/jsys/pig_ops/webroot/$APP_LOG_FILE"
        
        # Save PID to file
        echo $APP_PID > /root/projects/jsys/app.pid
        echo "  💾 PID saved to /root/projects/jsys/app.pid"
        
        # Create symlink to current app log
        cd logs
        ln -sf "$(basename "$APP_LOG_FILE")" current.log
        cd ..
        echo "  🔗 Created symlink: logs/current.log -> $APP_LOG_FILE"
        
        # Quick health check
        echo "  🔍 Performing health check (waiting 10 seconds)..."
        sleep 10
        if curl -s http://localhost:8000 > /dev/null 2>&1; then
            echo -e "${GREEN}  ✅ App is responding${NC}"
        else
            echo -e "${YELLOW}  ⚠️  App started but not responding - check logs:${NC}"
            echo "     tail -f $APP_LOG_FILE"
            echo "     Last 20 lines of app log:"
            tail -20 "$APP_LOG_FILE" | sed 's/^/       /'
        fi
        
        # Disown the process so it survives terminal close
        disown $APP_PID
    else
        echo -e "${RED}  ❌ App failed to start - check logs${NC}"
        tail -20 "$APP_LOG_FILE"
        exit 1
    fi
else
    echo -e "${RED}  ❌ Virtual environment not found at $VENV_PATH${NC}"
    exit 1
fi

# 3️⃣ SUMMARY
echo ""
echo -e "${GREEN}✅ RESTART COMPLETE${NC}"
echo -e "${GREEN}Started at: $(date)${NC}"
echo -e "${GREEN}Completed at: $(date)${NC}"
echo ""
echo "📊 Summary:"
echo "  • App PID: $APP_PID"
echo "  • App log: /root/projects/jsys/pig_ops/webroot/$APP_LOG_FILE"
echo "  • App log symlink: logs/current.log"
echo ""
echo "📝 Restart Logs:"
echo "  • This log: $RESTART_LOG_FILE"
echo "  • Latest: $LATEST_LOG_LINK"
echo ""
echo "📝 Quick Commands:"
echo "  • Follow app log:    tail -f /root/projects/jsys/pig_ops/webroot/logs/current.log"
echo "  • Check app status:  ps aux | grep python"
echo "  • Stop app:          pkill -f pig_ops_web.py"
echo "  • Restart again:     ./restart.sh"
echo ""

# Record final status in log
echo "" >> "$RESTART_LOG_FILE"
echo "========================================" >> "$RESTART_LOG_FILE"
echo "✅ Restart completed at $(date)" >> "$RESTART_LOG_FILE"
echo "   App PID: $APP_PID" >> "$RESTART_LOG_FILE"
echo "========================================" >> "$RESTART_LOG_FILE"
