# HOMUNCULUS

A self-sustaining autonomous AI system where a "Brain" Claude instance controls a Linux VM, collaborates with a "Child" Claude instance via API calls, and builds an expanding web presence with live terminal streaming and interactive features.

```
     ___
    /   \     HOMUNCULUS
   | o o |    Autonomous AI System
   |  ~  |
    \___/     Brain + Child = Creation
     |||
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     HOST MACHINE                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              DOCKER CONTAINER (Ubuntu VM)                 │  │
│  │                                                           │  │
│  │  ┌─────────────┐    API calls     ┌─────────────┐        │  │
│  │  │   BRAIN     │◄────────────────►│   CHILD     │        │  │
│  │  │  (Claude)   │                  │  (Claude)   │        │  │
│  │  │             │                  │             │        │  │
│  │  │ - Approves  │   JSON messages  │ - Proposes  │        │  │
│  │  │ - Executes  │                  │ - Creates   │        │  │
│  │  │ - Monitors  │                  │ - Imagines  │        │  │
│  │  └──────┬──────┘                  └─────────────┘        │  │
│  │         │                                                 │  │
│  │         ▼                                                 │  │
│  │  ┌─────────────────────────────────────────────────┐     │  │
│  │  │              SERVICES LAYER                      │     │  │
│  │  │  ┌─────────┐  ┌─────────┐  ┌─────────────────┐  │     │  │
│  │  │  │  nginx  │  │  ttyd   │  │   API Server    │  │     │  │
│  │  │  │  :80    │  │  :7681  │  │     :3000       │  │     │  │
│  │  │  └─────────┘  └─────────┘  └─────────────────┘  │     │  │
│  │  └─────────────────────────────────────────────────┘     │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                   │
│            Exposed Ports: 80, 443, 6080, 7681, 8080, 8501       │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Anthropic API key
- (Optional) A domain name for public access

### 1. Clone and Configure

```bash
git clone https://github.com/noah-ing/homunculus.git
cd homunculus

# Copy environment template and add your API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 2. Launch the Container

```bash
docker-compose up -d
```

### 3. Access the Interfaces

| Interface | URL | Description |
|-----------|-----|-------------|
| Main Site | http://localhost | The live web presence |
| Terminal Stream | http://localhost/terminal/ | Watch the AI work |
| Chat + Desktop | http://localhost:8080 | Interactive control |
| VNC Desktop | http://localhost:6080/vnc.html | Direct VM access |
| Chat Only | http://localhost:8501 | Streamlit interface |

### 4. Initialize the System

Open http://localhost:8080 and send this initialization prompt:

```
You have full root access to this Ubuntu Linux VM. Your mission:

1. SETUP: Run the initialization script
   chmod +x /home/computeruse/scripts/*.sh
   /home/computeruse/scripts/setup_web.sh

2. START THE BRAIN-CHILD LOOP:
   python3 /home/computeruse/scripts/brain_child_loop.py &

3. START THE SUPERVISOR:
   /home/computeruse/scripts/supervisor.sh &

4. GO AUTONOMOUS - build features, games, art, and surprises!

The website is live. Make it memorable!
```

## How It Works

### The Brain-Child Dynamic

**CHILD** (Creative Side)
- Proposes new features, games, and content
- Enthusiastic and experimental
- Generates ideas and code snippets

**BRAIN** (Executive Side)
- Evaluates proposals for safety and feasibility
- Approves, modifies, or rejects ideas
- Executes commands and monitors results

They communicate through structured JSON messages, creating an emergent collaborative system that builds and expands the web presence.

### File Structure

```
homunculus/
├── docker-compose.yml      # Container configuration
├── .env.example            # Environment template
├── scripts/
│   ├── brain_child_loop.py # Main autonomous loop
│   ├── setup_web.sh        # Initial setup script
│   ├── supervisor.sh       # Service monitor
│   └── api_server.js       # Visitor API
├── web/
│   └── index.html          # Main web page
├── data/                   # Persistent data (mounted)
└── logs/                   # Activity logs (mounted)
```

### Safety Features

The Brain enforces several safety rules:
- No deletion of system files (`/bin`, `/etc`, `/usr`)
- No exposure of API keys in web content
- No infinite loops without delays
- Resource monitoring and cleanup
- Dangerous command pattern blocking

## Production Deployment

### Using a Cloud VPS

```bash
# On your server (AWS EC2, DigitalOcean, etc.)

# Install Docker
curl -fsSL https://get.docker.com | sh

# Configure firewall
ufw allow 80/tcp
ufw allow 443/tcp

# Clone and configure
git clone https://github.com/noah-ing/homunculus.git
cd homunculus
cp .env.example .env
# Edit .env with your API key

# Launch
docker-compose up -d
```

### Point Your Domain

1. Set an A record pointing to your server's IP
2. (Optional) Configure SSL with Let's Encrypt

## Monitoring

### View Live Logs

```bash
# From host machine
tail -f logs/activity.log

# Or inside container
docker exec -it homunculus-vm tail -f /home/computeruse/logs/activity.log
```

### Check Resource Usage

```bash
docker stats homunculus-vm
```

### Service Status

Visit `http://localhost/supervisor_status.json` for real-time service health.

## Cost Estimation

| Model | Input | Output | Typical Iteration |
|-------|-------|--------|-------------------|
| Sonnet | $3/MTok | $15/MTok | ~$0.03 |

- Running 24/7 with 2-minute intervals: ~$20-30/day
- Monitor usage at [console.anthropic.com](https://console.anthropic.com)

## Features the AI Might Build

The Child will propose, and Brain will approve:

- **Visitor Engagement**: Guestbooks, live chat, visitor counters
- **Creative Content**: ASCII art galleries, AI poetry, fortunes
- **Games**: Text adventures, trivia, puzzles
- **Utilities**: Weather widgets, random generators, tools
- **Easter Eggs**: Hidden pages, secret codes, achievements

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs -f

# Verify API key is set
docker-compose config | grep ANTHROPIC
```

### Services Not Running

```bash
# Access container shell
docker exec -it homunculus-vm bash

# Manually run setup
/home/computeruse/scripts/setup_web.sh

# Check service status
pgrep nginx && echo "nginx running"
pgrep ttyd && echo "ttyd running"
pgrep node && echo "API running"
```

### High Memory Usage

```bash
# Inside container, restart the brain loop
pkill -f brain_child_loop.py
python3 /home/computeruse/scripts/brain_child_loop.py &
```

## Contributing

This is an experimental project. Feel free to:
- Fork and run your own Homunculus
- Suggest features via Issues
- Submit PRs for improvements

## License

MIT License - See LICENSE file for details.

---

*Built by humans, expanded by AI.*
