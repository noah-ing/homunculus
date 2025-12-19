#!/bin/bash
#
# Homunculus Web Presence Setup Script
# =====================================
# This script initializes the web server, terminal streaming,
# and all services needed for the autonomous system.
#

set -e

echo "========================================"
echo "  HOMUNCULUS WEB PRESENCE SETUP"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    log_warn "Not running as root, some operations may fail"
fi

# Update package lists
log_info "Updating package lists..."
apt-get update -qq

# Install essential packages
log_info "Installing essential packages..."
apt-get install -y -qq \
    nginx \
    ttyd \
    python3-pip \
    nodejs \
    npm \
    curl \
    jq \
    git \
    htop \
    tree \
    figlet \
    cowsay \
    fortune-mod \
    2>/dev/null || log_warn "Some packages may have failed to install"

# Install Python packages
log_info "Installing Python packages..."
pip3 install -q anthropic requests flask 2>/dev/null || log_warn "Python packages may have failed"

# Create directory structure
log_info "Creating directory structure..."
mkdir -p /var/www/html/{games,gallery,api,assets}
mkdir -p /home/computeruse/{logs,comms,persistent}
chown -R www-data:www-data /var/www/html 2>/dev/null || true
chmod -R 755 /var/www/html

# Configure nginx
log_info "Configuring nginx..."
cat > /etc/nginx/sites-available/default << 'NGINX_CONF'
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html;

    server_name _;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    # Main site
    location / {
        try_files $uri $uri/ =404;
    }

    # Live terminal stream (ttyd)
    location /terminal/ {
        proxy_pass http://127.0.0.1:7681/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }

    # API endpoints
    location /api/ {
        proxy_pass http://127.0.0.1:3000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Activity feed (JSON file)
    location /activity.json {
        add_header Cache-Control "no-cache";
        try_files $uri =404;
    }

    # Stats feed (JSON file)
    location /stats.json {
        add_header Cache-Control "no-cache";
        try_files $uri =404;
    }

    # Enable gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript;
}
NGINX_CONF

# Test and restart nginx
log_info "Testing nginx configuration..."
nginx -t 2>/dev/null && log_success "Nginx configuration valid"
systemctl restart nginx 2>/dev/null || service nginx restart 2>/dev/null || nginx -s reload 2>/dev/null

# Create initial activity.json
log_info "Creating initial data files..."
echo '[]' > /var/www/html/activity.json
echo '{"iterations":0,"commands_executed":0,"features_built":0,"uptime_start":"'$(date -Iseconds)'","last_update":"'$(date -Iseconds)'"}' > /var/www/html/stats.json

# Copy main web files
log_info "Setting up web content..."
if [ -f "/home/computeruse/scripts/index.html" ]; then
    cp /home/computeruse/scripts/index.html /var/www/html/index.html
fi

# Start ttyd for terminal streaming
log_info "Starting terminal streaming service (ttyd)..."
pkill ttyd 2>/dev/null || true
sleep 1

# Start ttyd with read-only mode for security
ttyd -p 7681 -R -t fontSize=14 -t fontFamily="'Fira Code', monospace" bash -c 'cd /home/computeruse && tail -f logs/activity.log 2>/dev/null || echo "Waiting for activity..."' &
TTYD_PID=$!

if ps -p $TTYD_PID > /dev/null 2>&1; then
    log_success "ttyd started on port 7681 (PID: $TTYD_PID)"
else
    log_warn "ttyd may not have started correctly"
fi

# Create startup script for API server
log_info "Setting up API server..."
cat > /home/computeruse/scripts/api_server.js << 'APISERVER'
const http = require('http');
const fs = require('fs');
const path = require('path');

// State
let visitorCount = 0;
const startTime = Date.now();

// Load persisted visitor count
const visitorFile = '/home/computeruse/persistent/visitors.json';
try {
    if (fs.existsSync(visitorFile)) {
        const data = JSON.parse(fs.readFileSync(visitorFile, 'utf8'));
        visitorCount = data.count || 0;
    }
} catch (e) {
    console.log('Starting fresh visitor count');
}

function saveVisitors() {
    try {
        fs.writeFileSync(visitorFile, JSON.stringify({ count: visitorCount }));
    } catch (e) {
        console.error('Failed to save visitor count:', e);
    }
}

const server = http.createServer((req, res) => {
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');

    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    const url = req.url.split('?')[0];

    switch (url) {
        case '/visit':
            visitorCount++;
            saveVisitors();
            res.end(JSON.stringify({
                count: visitorCount,
                message: getVisitorMessage(visitorCount)
            }));
            break;

        case '/stats':
            const statsFile = '/var/www/html/stats.json';
            try {
                const stats = JSON.parse(fs.readFileSync(statsFile, 'utf8'));
                stats.visitors = visitorCount;
                stats.uptime_seconds = Math.floor((Date.now() - startTime) / 1000);
                res.end(JSON.stringify(stats));
            } catch (e) {
                res.end(JSON.stringify({
                    visitors: visitorCount,
                    uptime_seconds: Math.floor((Date.now() - startTime) / 1000),
                    error: 'Stats file not available'
                }));
            }
            break;

        case '/activity':
            const activityFile = '/var/www/html/activity.json';
            try {
                const activity = fs.readFileSync(activityFile, 'utf8');
                res.end(activity);
            } catch (e) {
                res.end(JSON.stringify([]));
            }
            break;

        case '/health':
            res.end(JSON.stringify({
                status: 'healthy',
                uptime: Math.floor((Date.now() - startTime) / 1000)
            }));
            break;

        default:
            res.statusCode = 404;
            res.end(JSON.stringify({ error: 'Not found' }));
    }
});

function getVisitorMessage(count) {
    if (count === 1) return "You're the FIRST visitor! Welcome, pioneer!";
    if (count === 10) return "DOUBLE DIGITS! You're visitor #10!";
    if (count === 42) return "The answer to everything! Visitor #42!";
    if (count === 100) return "TRIPLE DIGITS! Visitor #100!";
    if (count === 1000) return "ONE THOUSAND visitors! This is amazing!";
    if (count % 100 === 0) return `Milestone! Visitor #${count}!`;
    return `Welcome, visitor #${count}!`;
}

const PORT = 3000;
server.listen(PORT, '0.0.0.0', () => {
    console.log(`API server running on port ${PORT}`);
    console.log(`Current visitor count: ${visitorCount}`);
});
APISERVER

# Start API server
pkill -f "node.*api_server.js" 2>/dev/null || true
sleep 1
node /home/computeruse/scripts/api_server.js &
API_PID=$!

if ps -p $API_PID > /dev/null 2>&1; then
    log_success "API server started on port 3000 (PID: $API_PID)"
else
    log_warn "API server may not have started correctly"
fi

# Create a welcome banner
log_info "Creating welcome banner..."
figlet -f small "HOMUNCULUS" 2>/dev/null || echo "=== HOMUNCULUS ===" > /var/www/html/banner.txt

# Final status
echo ""
echo "========================================"
echo -e "${GREEN}  SETUP COMPLETE!${NC}"
echo "========================================"
echo ""
echo "Services running:"
echo "  - nginx (port 80)     : Web server"
echo "  - ttyd (port 7681)    : Terminal streaming"
echo "  - API (port 3000)     : Visitor API"
echo ""
echo "Access points:"
echo "  - Main site    : http://localhost/"
echo "  - Terminal     : http://localhost/terminal/"
echo "  - API Status   : http://localhost/api/health"
echo ""
echo "To start the Brain-Child loop:"
echo "  python3 /home/computeruse/scripts/brain_child_loop.py"
echo ""
log_success "Homunculus is ready to awaken!"
