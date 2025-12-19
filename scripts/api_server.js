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
