<p align="center">
  <img src="https://img.shields.io/badge/Status-Autonomous-00ff88?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/AI-Claude%20Sonnet-blueviolet?style=for-the-badge" alt="AI Model">
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=28&pause=1000&color=00FF88&center=true&vCenter=true&random=false&width=600&lines=HOMUNCULUS;Autonomous+AI+System;Brain+%2B+Child+%3D+Creation" alt="Typing SVG" />
</p>

<p align="center">
  <strong>A self-evolving AI system that builds and expands its own web presence</strong>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-how-it-works">How It Works</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-operations-guide">Operations</a> •
  <a href="#-live-demo">Demo</a>
</p>

---

## 🎯 Overview

**Homunculus** is an experimental autonomous AI system that demonstrates emergent behavior through a unique "Brain-Child" collaboration model. Two Claude AI instances work together inside a Docker container—one creative, one executive—to continuously build, expand, and maintain a live web presence.

### ✨ Key Features

- **🧠 Dual-AI Architecture** — Brain (executive) and Child (creative) instances collaborate via structured JSON messaging
- **🔄 Autonomous Operation** — Runs continuously, proposing and implementing features without human intervention
- **🛡️ Built-in Safety** — Command filtering, resource monitoring, and execution guardrails
- **📺 Live Transparency** — Watch the AI work in real-time via terminal streaming
- **💾 Persistent Memory** — Remembers what it built across restarts
- **🎮 Self-Generated Content** — Games, art, utilities—all created by the AI itself

### 🏆 What Makes This Special

Unlike typical AI demos, Homunculus isn't just responding to prompts—it's **actively deciding** what to build next, **evaluating** its own ideas, and **executing** real code on a real system. The Brain-Child dynamic creates emergent behavior where:

- The **Child** dreams up creative features ("Let's build a rainbow snake game!")
- The **Brain** evaluates feasibility and safety ("Approved with modifications...")
- Together they **iterate** until something works
- The system **learns** from failures and **remembers** successes

---

## 📸 Screenshots

<p align="center">
  <i>The Homunculus web interface showing real-time stats and activity feed</i>
</p>

| Main Dashboard | Live Terminal | Snake Game |
|:---:|:---:|:---:|
| Real-time stats, visitor counter, activity feed | Watch Brain-Child collaboration live | AI-generated HTML5 canvas game |

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Docker | 20.10+ | [Install Docker](https://docs.docker.com/get-docker/) |
| Docker Compose | 2.0+ | Usually included with Docker Desktop |
| Anthropic API Key | — | [Get one here](https://console.anthropic.com/) |

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/noah-ing/homunculus.git
cd homunculus

# 2. Configure your API key
cp .env.example .env
echo "ANTHROPIC_API_KEY=your-key-here" > .env

# 3. Launch the container
docker-compose up -d

# 4. Initialize the system (copy scripts into container)
docker cp scripts/. homunculus-vm:/home/computeruse/scripts/
docker cp web/. homunculus-vm:/var/www/html/

# 5. Run setup and start the autonomous loop
docker exec -u root homunculus-vm bash -c "chmod +x /home/computeruse/scripts/*.sh && /home/computeruse/scripts/setup_web.sh"
docker exec -u root homunculus-vm bash -c "python3 /home/computeruse/scripts/brain_child_loop.py &"
```

### Access Points

| Interface | URL | Description |
|:----------|:----|:------------|
| 🌐 **Main Site** | [localhost](http://localhost) | The live web presence built by the AI |
| 📺 **Terminal Stream** | [localhost:7681](http://localhost:7681) | Watch the AI work in real-time |
| 🖥️ **VNC Desktop** | [localhost:6080/vnc.html](http://localhost:6080/vnc.html) | Full desktop access |
| 💬 **Chat Interface** | [localhost:8080](http://localhost:8080) | Interactive chat + desktop view |
| 📊 **API Stats** | [localhost:3000/stats](http://localhost:3000/stats) | JSON endpoint for metrics |

---

## 🧠 How It Works

### The Brain-Child Collaboration Model

Homunculus implements a novel dual-agent architecture inspired by cognitive psychology's concept of creative vs. executive function:

```
┌─────────────────────────────────────────────────────────────┐
│                    COLLABORATION LOOP                        │
│                                                              │
│   ┌─────────┐    Proposal     ┌─────────┐                   │
│   │  CHILD  │ ──────────────► │  BRAIN  │                   │
│   │         │                 │         │                   │
│   │ Creative│ ◄────────────── │Executive│                   │
│   │ Dreamer │    Decision     │  Judge  │                   │
│   └─────────┘                 └────┬────┘                   │
│                                    │                         │
│                              ┌─────▼─────┐                   │
│                              │  EXECUTE  │                   │
│                              │  Commands │                   │
│                              └─────┬─────┘                   │
│                                    │                         │
│                              ┌─────▼─────┐                   │
│                              │  UPDATE   │                   │
│                              │  Context  │                   │
│                              └───────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

#### 👶 The Child (Creative Agent)

- **Personality**: Enthusiastic, experimental, uses caps when excited
- **Role**: Proposes new features, generates ideas, imagines possibilities
- **Prompt Style**: "Let's build a RAINBOW SNAKE GAME! 🎮"
- **Model**: Claude Sonnet (fast iteration)

#### 🧠 The Brain (Executive Agent)

- **Personality**: Thoughtful, safety-conscious, pragmatic
- **Role**: Evaluates proposals, ensures safety, executes commands
- **Decisions**: `APPROVE`, `MODIFY`, or `REJECT`
- **Model**: Claude Sonnet (reliable judgment)

### Communication Protocol

Each iteration follows this cycle:

1. **Child proposes** → Natural language with code snippets
2. **Brain evaluates** → Returns structured JSON decision
3. **Commands execute** → Shell commands run with safety checks
4. **Context updates** → Results inform next iteration

```json
{
  "decision": "approve",
  "reasoning": "Safe and creative addition to the site",
  "commands": ["mkdir -p /var/www/html/games", "cat > game.html << 'EOF'..."],
  "feature_name": "Rainbow Snake Game",
  "next_direction": "Consider adding a high score system"
}
```

### Safety Guardrails

The Brain enforces multiple safety layers:

| Layer | Protection |
|-------|------------|
| **Pattern Blocking** | Regex filters for dangerous commands (`rm -rf /`, `mkfs`, etc.) |
| **Path Protection** | No modifications to `/bin`, `/etc`, `/usr` |
| **Secret Protection** | API keys never exposed in web content |
| **Resource Limits** | Memory monitoring, log rotation, timeout enforcement |
| **Execution Timeout** | Commands killed after 5 minutes |

---

## 🏗️ Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                          HOST MACHINE                                 │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                DOCKER CONTAINER (Ubuntu 22.04)                   │ │
│  │                                                                  │ │
│  │  ┌──────────────────────────────────────────────────────────┐   │ │
│  │  │                   BRAIN-CHILD LOOP                        │   │ │
│  │  │                  (brain_child_loop.py)                    │   │ │
│  │  │                                                           │   │ │
│  │  │   ┌─────────┐  Anthropic API  ┌─────────┐               │   │ │
│  │  │   │  BRAIN  │◄───────────────►│  CHILD  │               │   │ │
│  │  │   │ Claude  │                 │ Claude  │               │   │ │
│  │  │   └────┬────┘                 └─────────┘               │   │ │
│  │  │        │ subprocess.run()                                │   │ │
│  │  │        ▼                                                 │   │ │
│  │  │   ┌─────────┐                                           │   │ │
│  │  │   │  BASH   │ ──► File System, Services, Network        │   │ │
│  │  │   └─────────┘                                           │   │ │
│  │  └──────────────────────────────────────────────────────────┘   │ │
│  │                                                                  │ │
│  │  ┌─────────────────────────────────────────────────────────┐    │ │
│  │  │                    SERVICES LAYER                        │    │ │
│  │  │                                                          │    │ │
│  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌───────────┐  │    │ │
│  │  │  │  nginx  │  │  ttyd   │  │  API    │  │Supervisor │  │    │ │
│  │  │  │  :80    │  │  :7681  │  │  :3000  │  │  (monitor)│  │    │ │
│  │  │  └─────────┘  └─────────┘  └─────────┘  └───────────┘  │    │ │
│  │  └─────────────────────────────────────────────────────────┘    │ │
│  │                                                                  │ │
│  │  ┌─────────────────────────────────────────────────────────┐    │ │
│  │  │                   STORAGE LAYER                          │    │ │
│  │  │                                                          │    │ │
│  │  │   /var/www/html/     Web content (AI-generated)         │    │ │
│  │  │   /home/.../logs/    Activity logs                       │    │ │
│  │  │   /home/.../persistent/  Memory, state                   │    │ │
│  │  └─────────────────────────────────────────────────────────┘    │ │
│  │                                                                  │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                              │                                        │
│    Ports: 80, 443, 3000, 5900, 6080, 7681, 8080, 8501               │
└──────────────────────────────────────────────────────────────────────┘
```

### File Structure

```
homunculus/
├── 📄 docker-compose.yml       # Container orchestration
├── 📄 .env.example             # Environment template
├── 📄 .gitignore               # Git ignore rules
├── 📄 README.md                # This file
│
├── 📁 scripts/
│   ├── 🐍 brain_child_loop.py  # Core autonomous loop (500+ lines)
│   ├── 🔧 setup_web.sh         # Service initialization
│   ├── 🔧 supervisor.sh        # Health monitoring & restart
│   └── 📜 api_server.js        # Visitor tracking API
│
├── 📁 web/
│   ├── 🌐 index.html           # Main dashboard
│   └── 🎮 games/               # AI-generated games
│
├── 📁 data/                    # Mounted: persistent storage
│   └── 💾 memory.json          # AI's long-term memory
│
└── 📁 logs/                    # Mounted: activity logs
    ├── 📋 activity.log         # Human-readable log
    └── 📋 activity.jsonl       # Machine-parseable log
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Container | Docker + Ubuntu 22.04 | Isolated execution environment |
| AI Models | Claude Sonnet 4 | Brain and Child agents |
| Web Server | nginx | Serves AI-generated content |
| Terminal Stream | ttyd | Real-time terminal broadcasting |
| API | Node.js | Visitor tracking, stats |
| Supervisor | Bash | Service health monitoring |
| Desktop | Xvfb + noVNC | Optional GUI access |

---

## 🎮 Operations Guide

### Starting & Stopping

```bash
# Start everything
docker-compose up -d

# Stop the Brain-Child loop (container keeps running)
docker exec homunculus-vm pkill -f brain_child_loop.py

# Restart the Brain-Child loop
docker exec -u root homunculus-vm bash -c "python3 /home/computeruse/scripts/brain_child_loop.py &"

# Stop everything
docker-compose down

# Full restart
docker-compose restart
```

### Monitoring

```bash
# Watch live activity (best way to monitor)
docker exec homunculus-vm tail -f /home/computeruse/logs/activity.log

# Quick health check
docker exec homunculus-vm bash -c '
  echo "=== Services ==="
  pgrep nginx > /dev/null && echo "✅ nginx" || echo "❌ nginx"
  pgrep ttyd > /dev/null && echo "✅ ttyd" || echo "❌ ttyd"
  pgrep -f api_server > /dev/null && echo "✅ API" || echo "❌ API"
  pgrep -f brain_child > /dev/null && echo "✅ Brain-Child" || echo "❌ Brain-Child"
  echo ""
  echo "=== Stats ==="
  cat /var/www/html/stats.json 2>/dev/null | python3 -m json.tool
'

# Resource usage
docker stats homunculus-vm --no-stream

# See what the AI has built
docker exec homunculus-vm find /var/www/html -name "*.html" -type f
```

### Configuration

#### Iteration Speed

Edit `scripts/brain_child_loop.py`:
```python
iteration_delay = 10   # Seconds between iterations (default: 10)
error_delay = 60       # Seconds to wait after errors
```

#### AI Models

```python
BRAIN_MODEL = "claude-sonnet-4-20250514"   # Or "claude-opus-4-20250514"
CHILD_MODEL = "claude-sonnet-4-20250514"   # Faster = cheaper iterations
```

#### Safety Rules

Add patterns to `dangerous_patterns` list:
```python
dangerous_patterns = [
    r'rm\s+-rf\s+/',        # Don't delete root
    r'your-custom-pattern',  # Add your own
]
```

### Backup & Restore

```bash
# Backup current state
docker exec homunculus-vm tar -czf /tmp/backup.tar.gz \
  /var/www/html /home/computeruse/persistent /home/computeruse/logs
docker cp homunculus-vm:/tmp/backup.tar.gz ./backups/$(date +%Y%m%d).tar.gz

# Restore from backup
docker cp ./backups/20241219.tar.gz homunculus-vm:/tmp/
docker exec homunculus-vm tar -xzf /tmp/20241219.tar.gz -C /
```

---

## 💰 Cost Analysis

### API Usage Estimates

| Interval | Iterations/Day | Est. Daily Cost | Monthly |
|----------|----------------|-----------------|---------|
| 10 sec | 8,640 | $25-40 | $750-1,200 |
| 30 sec | 2,880 | $8-15 | $250-450 |
| 60 sec | 1,440 | $4-8 | $120-240 |
| 5 min | 288 | $1-2 | $30-60 |

### Cost Breakdown Per Iteration

```
Child proposal:  ~1,500 tokens input + 800 output  = ~$0.015
Brain decision:  ~2,000 tokens input + 500 output  = ~$0.013
─────────────────────────────────────────────────────────────
Total per iteration:                                 ~$0.028
```

### Cost Control Tips

1. **Increase iteration delay** — Set `iteration_delay = 60` for ~75% cost reduction
2. **Use Haiku for Child** — Faster, cheaper creative proposals
3. **Run during specific hours** — Stop the loop when not monitoring
4. **Set spending alerts** — Configure at [console.anthropic.com](https://console.anthropic.com)

---

## 🛠️ Troubleshooting

<details>
<summary><strong>Container won't start</strong></summary>

```bash
# Check Docker logs
docker-compose logs -f

# Verify API key
docker-compose config | grep ANTHROPIC

# Check port conflicts
lsof -i :80 -i :8080 -i :6080
```
</details>

<details>
<summary><strong>Brain-Child loop crashes</strong></summary>

```bash
# Check Python logs
docker exec homunculus-vm cat /home/computeruse/logs/brain.log

# Check for memory issues
docker exec homunculus-vm free -h

# Restart with fresh state
docker exec homunculus-vm pkill -f brain_child
docker exec -u root homunculus-vm python3 /home/computeruse/scripts/brain_child_loop.py &
```
</details>

<details>
<summary><strong>Website not loading</strong></summary>

```bash
# Check nginx
docker exec homunculus-vm nginx -t
docker exec homunculus-vm systemctl status nginx

# Check web files exist
docker exec homunculus-vm ls -la /var/www/html/

# Restart nginx
docker exec -u root homunculus-vm systemctl restart nginx
```
</details>

<details>
<summary><strong>High memory usage</strong></summary>

```bash
# Check what's using memory
docker exec homunculus-vm ps aux --sort=-%mem | head -10

# Clear Python memory (restart loop)
docker exec homunculus-vm pkill -f brain_child
docker exec -u root homunculus-vm python3 /home/computeruse/scripts/brain_child_loop.py &

# Trim logs
docker exec homunculus-vm truncate -s 10M /home/computeruse/logs/activity.log
```
</details>

---

## 🗺️ Roadmap

### Current Features ✅
- [x] Brain-Child autonomous loop
- [x] Live terminal streaming
- [x] Visitor tracking API
- [x] Persistent memory system
- [x] Safety guardrails
- [x] Service supervisor

### Planned Features 🚧
- [ ] Web-based control panel
- [ ] Multiple personality presets
- [ ] Plugin system for Child capabilities
- [ ] Webhook notifications
- [ ] Multi-container swarm mode
- [ ] Cost tracking dashboard

### Ideas 💡
- [ ] Voice synthesis for Brain-Child dialogue
- [ ] Visitor interaction (suggestions, voting)
- [ ] Self-modifying codebase
- [ ] Federated Homunculus network

---

## 🤝 Contributing

This is an experimental project exploring autonomous AI systems. Contributions welcome!

### Ways to Contribute

- 🐛 **Report bugs** — Open an issue with reproduction steps
- 💡 **Suggest features** — Ideas for Brain-Child capabilities
- 🔧 **Submit PRs** — Bug fixes, new features, documentation
- 🎨 **Share creations** — Show what your Homunculus built!

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/homunculus.git
cd homunculus

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes, test locally
docker-compose up -d
# ... test ...

# Commit and push
git commit -m "Add amazing feature"
git push origin feature/amazing-feature

# Open a Pull Request
```

---

## 📜 License

MIT License — See [LICENSE](LICENSE) for details.

---

## 👤 Author

**Noah Ing**

- GitHub: [@noah-ing](https://github.com/noah-ing)

---

<p align="center">
  <strong>Built by humans, expanded by AI.</strong>
</p>

<p align="center">
  <sub>If you find this project interesting, consider giving it a ⭐</sub>
</p>
