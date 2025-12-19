#!/bin/bash
#
# Homunculus Supervisor Script
# =============================
# Keeps all services running and monitors system health.
# Automatically restarts failed services.
#

LOG_FILE="/home/computeruse/logs/supervisor.log"
BRAIN_SCRIPT="/home/computeruse/scripts/brain_child_loop.py"
API_SCRIPT="/home/computeruse/scripts/api_server.js"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "[${timestamp}] [${level}] ${message}" | tee -a "$LOG_FILE"
}

log_info() { log "INFO" "$1"; }
log_warn() { log "WARN" "$1"; }
log_error() { log "ERROR" "$1"; }
log_success() { log "SUCCESS" "$1"; }

# Check and start nginx
check_nginx() {
    if ! pgrep -x nginx > /dev/null; then
        log_warn "nginx is down, attempting restart..."
        if systemctl restart nginx 2>/dev/null || service nginx restart 2>/dev/null || nginx 2>/dev/null; then
            log_success "nginx restarted successfully"
            return 0
        else
            log_error "Failed to restart nginx"
            return 1
        fi
    fi
    return 0
}

# Check and start ttyd
check_ttyd() {
    if ! pgrep -x ttyd > /dev/null; then
        log_warn "ttyd is down, attempting restart..."
        ttyd -p 7681 -R -t fontSize=14 bash -c 'cd /home/computeruse && tail -f logs/activity.log 2>/dev/null || echo "Waiting for activity..."' &
        sleep 2
        if pgrep -x ttyd > /dev/null; then
            log_success "ttyd restarted successfully (PID: $!)"
            return 0
        else
            log_error "Failed to restart ttyd"
            return 1
        fi
    fi
    return 0
}

# Check and start API server
check_api() {
    if ! pgrep -f "node.*api_server.js" > /dev/null; then
        log_warn "API server is down, attempting restart..."
        if [ -f "$API_SCRIPT" ]; then
            node "$API_SCRIPT" &
            sleep 2
            if pgrep -f "node.*api_server.js" > /dev/null; then
                log_success "API server restarted successfully (PID: $!)"
                return 0
            else
                log_error "Failed to restart API server"
                return 1
            fi
        else
            log_error "API script not found at $API_SCRIPT"
            return 1
        fi
    fi
    return 0
}

# Check and start Brain-Child loop
check_brain() {
    if ! pgrep -f "python.*brain_child_loop.py" > /dev/null; then
        log_warn "Brain-Child loop is down, attempting restart..."
        if [ -f "$BRAIN_SCRIPT" ]; then
            python3 "$BRAIN_SCRIPT" &
            BRAIN_PID=$!
            sleep 3
            if ps -p $BRAIN_PID > /dev/null 2>&1; then
                log_success "Brain-Child loop restarted (PID: $BRAIN_PID)"
                return 0
            else
                log_error "Brain-Child loop failed to start"
                return 1
            fi
        else
            log_error "Brain script not found at $BRAIN_SCRIPT"
            return 1
        fi
    fi
    return 0
}

# Monitor system resources
check_resources() {
    # Check memory usage
    MEM_USED=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
    if [ "$MEM_USED" -gt 90 ]; then
        log_warn "High memory usage: ${MEM_USED}%"

        # Try to free some memory by clearing caches
        sync
        echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || true

        # If still high, log error
        MEM_AFTER=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
        if [ "$MEM_AFTER" -gt 90 ]; then
            log_error "Memory still critical: ${MEM_AFTER}%"
        else
            log_info "Memory freed: now at ${MEM_AFTER}%"
        fi
    fi

    # Check disk usage
    DISK_USED=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ "$DISK_USED" -gt 90 ]; then
        log_warn "High disk usage: ${DISK_USED}%"

        # Clean up log files if too large
        find /home/computeruse/logs -name "*.log" -size +100M -exec truncate -s 10M {} \; 2>/dev/null || true
        log_info "Truncated large log files"
    fi
}

# Create a status file for the web interface
update_status_file() {
    local status_file="/var/www/html/supervisor_status.json"
    local nginx_status="unknown"
    local ttyd_status="unknown"
    local api_status="unknown"
    local brain_status="unknown"

    pgrep -x nginx > /dev/null && nginx_status="running" || nginx_status="stopped"
    pgrep -x ttyd > /dev/null && ttyd_status="running" || ttyd_status="stopped"
    pgrep -f "node.*api_server.js" > /dev/null && api_status="running" || api_status="stopped"
    pgrep -f "python.*brain_child_loop.py" > /dev/null && brain_status="running" || brain_status="stopped"

    cat > "$status_file" << EOF
{
    "timestamp": "$(date -Iseconds)",
    "services": {
        "nginx": "$nginx_status",
        "ttyd": "$ttyd_status",
        "api": "$api_status",
        "brain": "$brain_status"
    },
    "resources": {
        "memory_percent": $(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100}'),
        "disk_percent": $(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    }
}
EOF
}

# Handle signals
trap 'log_info "Supervisor received shutdown signal"; exit 0' SIGTERM SIGINT

# Main supervisor loop
main() {
    log_info "========================================"
    log_info "  HOMUNCULUS SUPERVISOR STARTING"
    log_info "========================================"

    local check_interval=30  # seconds between checks
    local iteration=0

    while true; do
        iteration=$((iteration + 1))

        if [ $((iteration % 10)) -eq 1 ]; then
            log_info "Supervisor check #${iteration}"
        fi

        # Check all services
        check_nginx
        check_ttyd
        check_api
        check_brain

        # Monitor resources every 5th iteration
        if [ $((iteration % 5)) -eq 0 ]; then
            check_resources
        fi

        # Update status file
        update_status_file

        sleep $check_interval
    done
}

# Run main function
main "$@"
