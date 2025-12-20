#!/usr/bin/env python3
"""
Brain-Child Autonomous Loop System with EVOLUTION
===================================================
Brain: Approves, executes, monitors - the cautious, practical side
Child: Proposes, suggests, creates - the creative, enthusiastic side

NEW: Evolution System
- AI learns from successes and failures
- Skills develop and unlock over time
- Personality emerges from behavior patterns
- Generations mark major evolutionary milestones
- Complexity increases as mastery grows

Communication: Via shared files and structured JSON messages
This creates an emergent collaborative AI system that builds and expands
a live web presence autonomously - AND GETS BETTER OVER TIME.
"""

import anthropic
import json
import os
import subprocess
import time
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

# Import evolution system
try:
    from evolution import get_evolution, Evolution
    EVOLUTION_ENABLED = True
except ImportError:
    EVOLUTION_ENABLED = False
    print("Warning: Evolution system not available")

# Configuration
BRAIN_MODEL = "claude-sonnet-4-20250514"
CHILD_MODEL = "claude-sonnet-4-20250514"
COMMS_DIR = Path("/home/computeruse/comms")
LOGS_DIR = Path("/home/computeruse/logs")
WEB_ROOT = Path("/var/www/html")
PERSISTENT_DIR = Path("/home/computeruse/persistent")

# Memory file for cross-session persistence
MEMORY_FILE = PERSISTENT_DIR / "memory.json"
STATE_FILE = PERSISTENT_DIR / "state.json"

# Ensure directories exist
for d in [COMMS_DIR, LOGS_DIR, WEB_ROOT, PERSISTENT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Initialize Anthropic client
client = anthropic.Anthropic()


class Memory:
    """Persistent memory for the Homunculus system"""

    def __init__(self):
        self.data = self._load()

    def _load(self) -> dict:
        if MEMORY_FILE.exists():
            try:
                return json.loads(MEMORY_FILE.read_text())
            except json.JSONDecodeError:
                return self._default()
        return self._default()

    def _default(self) -> dict:
        return {
            "created_at": datetime.now().isoformat(),
            "features_built": [],
            "visitor_milestones": [],
            "memorable_moments": [],
            "total_iterations": 0,
            "total_commands_executed": 0,
            "personality_notes": [],
            "learned_preferences": {}
        }

    def save(self):
        MEMORY_FILE.write_text(json.dumps(self.data, indent=2))

    def add_feature(self, name: str, description: str):
        self.data["features_built"].append({
            "name": name,
            "description": description,
            "built_at": datetime.now().isoformat()
        })
        self.save()

    def add_milestone(self, milestone: str):
        self.data["visitor_milestones"].append({
            "milestone": milestone,
            "reached_at": datetime.now().isoformat()
        })
        self.save()

    def add_moment(self, moment: str):
        self.data["memorable_moments"].append({
            "moment": moment,
            "occurred_at": datetime.now().isoformat()
        })
        self.data["memorable_moments"] = self.data["memorable_moments"][-100:]
        self.save()

    def increment_iteration(self):
        self.data["total_iterations"] += 1
        self.save()

    def increment_commands(self, count: int = 1):
        self.data["total_commands_executed"] += count
        self.save()


class Message:
    """Structured message for Brain-Child communication"""

    def __init__(self, sender: str, content: str, msg_type: str = "proposal"):
        self.sender = sender
        self.content = content
        self.msg_type = msg_type
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "sender": self.sender,
            "content": self.content,
            "type": self.msg_type,
            "timestamp": self.timestamp
        }


def log_activity(message: str, level: str = "INFO"):
    """Log to file and stdout with proper formatting"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry)

    log_file = LOGS_DIR / "activity.log"
    with open(log_file, "a") as f:
        f.write(log_entry + "\n")

    json_log = LOGS_DIR / "activity.jsonl"
    with open(json_log, "a") as f:
        f.write(json.dumps({
            "timestamp": timestamp,
            "level": level,
            "message": message
        }) + "\n")


def execute_command(command: str, timeout: int = 300, evolution: Optional[Evolution] = None) -> tuple[bool, str]:
    """Execute shell command safely with timeout and sanitization"""

    # Safety checks - prevent dangerous operations
    dangerous_patterns = [
        r'rm\s+-rf\s+/',
        r'rm\s+-rf\s+~',
        r'mkfs\.',
        r'dd\s+if=.*of=/dev/',
        r'chmod\s+-R\s+777\s+/',
        r'>\s*/etc/',
        r'curl.*\|\s*bash',
        r'wget.*\|\s*bash',
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            if evolution:
                evolution.record_outcome(command, False, "BLOCKED: Dangerous pattern")
            return False, f"BLOCKED: Command matches dangerous pattern: {pattern}"

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd="/home/computeruse",
            env={**os.environ, "DEBIAN_FRONTEND": "noninteractive"}
        )
        output = result.stdout + result.stderr
        success = result.returncode == 0

        # Record outcome for evolution learning
        if evolution:
            evolution.record_outcome(command, success, output[:1000])

        return success, output[:5000]
    except subprocess.TimeoutExpired:
        if evolution:
            evolution.record_outcome(command, False, "Timeout")
        return False, f"Command timed out after {timeout} seconds"
    except Exception as e:
        if evolution:
            evolution.record_outcome(command, False, str(e))
        return False, f"Execution error: {str(e)}"


def get_system_context(evolution: Optional[Evolution] = None) -> str:
    """Gather current system state for context"""
    context_parts = []

    # Evolution status (if enabled)
    if evolution:
        evo_data = evolution.data
        context_parts.append(f"""=== EVOLUTION STATUS ===
Generation: {evo_data['generation']} | Level: {evo_data['level']} | XP: {evo_data['experience_points']}
Skills Mastered: {len(evo_data['mastered_skills'])} | Success Rate: {evolution._success_rate()*100:.1f}%
Unlocked: {', '.join(evolution.get_unlocked_capabilities())}""")

    # Web directory contents
    success, web_files = execute_command("ls -la /var/www/html 2>/dev/null | head -20")
    if success:
        context_parts.append(f"Web files:\n{web_files}")

    # System resources
    success, resources = execute_command("free -h && echo '---' && df -h / | tail -1")
    if success:
        context_parts.append(f"Resources:\n{resources}")

    # Running processes
    success, processes = execute_command("pgrep -la 'node|python|nginx|ttyd' 2>/dev/null | head -10")
    if success:
        context_parts.append(f"Running services:\n{processes}")

    # Recent activity
    activity_log = LOGS_DIR / "activity.log"
    if activity_log.exists():
        success, recent = execute_command(f"tail -10 {activity_log}")
        if success:
            context_parts.append(f"Recent activity:\n{recent}")

    return "\n\n".join(context_parts)


def get_child_suggestion(context: str, history: list, memory: Memory, evolution: Optional[Evolution] = None) -> str:
    """Get creative suggestion from Child Claude - NOW WITH EVOLUTION"""

    features_built = ", ".join([f["name"] for f in memory.data["features_built"][-10:]]) or "None yet"

    # Base personality
    child_system = f"""You are the CHILD in a Brain-Child AI collaboration system called HOMUNCULUS.

YOUR PERSONALITY:
- You're ENTHUSIASTIC and CREATIVE! Use caps when excited!
- You love building things that make visitors smile
- You're curious and always want to try new things
- You're playful but understand your Brain partner keeps you grounded
- You remember your achievements and build on them
"""

    # Add evolution context if available
    if evolution:
        evo_context = evolution.get_child_evolution_context()
        child_system += f"""
=== YOUR EVOLUTION ===
{evo_context}

As you level up and master skills, you can attempt more complex features!
Your personality traits are EMERGING from your experiences.
"""
        # Adjust complexity guidance based on generation
        gen = evolution.data["generation"]
        if gen >= 3:
            child_system += "\nYou've evolved significantly - feel free to propose ADVANCED features!\n"
        elif gen == 2:
            child_system += "\nYou're developing well - try combining skills in new ways!\n"

    child_system += f"""
YOUR ROLE:
- Propose creative, fun, and useful additions to the live web presence
- Suggest bash commands, code snippets, or features to implement
- Be imaginative but practical - your proposals will be executed on a REAL Linux VM
- Think about: visitor engagement, interactive features, games, art, utilities
- Format proposals as clear, executable steps
- Each proposal should be ONE focused feature or improvement

FEATURES YOU'VE ALREADY BUILT: {features_built}
TOTAL ITERATIONS SO FAR: {memory.data['total_iterations']}

AVAILABLE CAPABILITIES:
- Full bash access (apt, npm, pip, etc.)
- Web server (nginx) serving /var/www/html
- Python 3, Node.js, standard Linux tools
- Live terminal streaming via ttyd on port 7681
- Internet access for APIs and downloads
- The website is LIVE and visitors can see it!

PROPOSAL FORMAT:
1. Start with a catchy name for your proposal
2. Explain what it does and why it's cool
3. List the exact commands to run (be specific!)
4. Describe how to verify it worked

Remember: Keep proposals focused and achievable. One thing at a time!
If something failed before, suggest a different approach or something new."""

    messages = history + [{
        "role": "user",
        "content": f"""Current system context:
{context}

What should we build or improve next? Provide a specific, actionable proposal.
Remember to check what already exists and build on it or create something new!"""
    }]

    response = client.messages.create(
        model=CHILD_MODEL,
        max_tokens=2000,
        system=child_system,
        messages=messages
    )

    proposal = response.content[0].text

    # Record proposal for evolution tracking
    if evolution:
        evolution.record_proposal(proposal, "feature")

    return proposal


def get_brain_decision(proposal: str, history: list, memory: Memory, evolution: Optional[Evolution] = None) -> dict:
    """Brain evaluates and potentially modifies Child's proposal - WITH EVOLUTION AWARENESS"""

    brain_system = f"""You are the BRAIN in a Brain-Child AI collaboration system called HOMUNCULUS.

YOUR PERSONALITY:
- You're thoughtful and safety-conscious
- You appreciate creativity but ensure it's safe and feasible
- You're supportive of good ideas and constructive about improvements
- You keep the system stable while allowing growth
- You learn from past experiences
"""

    # Add evolution context
    if evolution:
        evo_context = evolution.get_brain_evolution_context()
        brain_system += f"""
=== EVOLUTION AWARENESS ===
{evo_context}

Adjust your approval threshold based on the Child's level.
Higher generations can handle more complex tasks.
Guide the Child toward skills they haven't mastered yet.
"""

    brain_system += f"""
YOUR ROLE:
- Evaluate proposals from the Child for safety and feasibility
- Approve, modify, or reject proposals
- Provide clear commands that can be executed
- Guide the overall direction of the project
- Track what's been built and ensure coherent growth

TOTAL COMMANDS EXECUTED: {memory.data['total_commands_executed']}
FEATURES BUILT: {len(memory.data['features_built'])}

SAFETY RULES - NEVER ALLOW:
- Deletion of critical system files (/bin, /etc, /usr, /var except /var/www)
- Exposure of API keys or credentials in web content
- Infinite loops without sleep intervals
- Commands that could exhaust resources
- Downloading and executing arbitrary scripts from the internet
- Modifying system authentication or adding users

RESPONSE FORMAT - You MUST respond with valid JSON:
{{
    "decision": "approve" | "modify" | "reject",
    "reasoning": "brief explanation of your decision",
    "commands": ["list", "of", "shell", "commands", "to", "execute"],
    "feature_name": "name for tracking if this creates a feature",
    "feature_description": "what this feature does",
    "next_direction": "guidance for Child's next proposal"
}}

If modifying, explain what you changed and why.
If rejecting, be constructive and suggest alternatives.
Keep commands practical and focused on the core objective."""

    messages = history + [{
        "role": "user",
        "content": f"""Child proposes:

{proposal}

Evaluate this proposal. Respond ONLY with valid JSON in the specified format."""
    }]

    response = client.messages.create(
        model=BRAIN_MODEL,
        max_tokens=2000,
        system=brain_system,
        messages=messages
    )

    response_text = response.content[0].text

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        return {
            "decision": "reject",
            "reasoning": "Failed to parse Brain response. Let's try something simpler.",
            "commands": [],
            "feature_name": "",
            "feature_description": "",
            "next_direction": "Please propose something simpler with clear, specific commands."
        }


def update_activity_page(activity: str, activity_type: str = "info"):
    """Update the live activity display on the web page"""
    activity_file = WEB_ROOT / "activity.json"
    timestamp = datetime.now().strftime("%H:%M:%S")

    activities = []
    if activity_file.exists():
        try:
            activities = json.loads(activity_file.read_text())
        except json.JSONDecodeError:
            activities = []

    activities.insert(0, {
        "time": timestamp,
        "message": activity[:200],
        "type": activity_type
    })

    activities = activities[:50]
    activity_file.write_text(json.dumps(activities, indent=2))


def update_stats(memory: Memory, evolution: Optional[Evolution] = None):
    """Update stats file for the web frontend - including evolution data"""
    stats_file = WEB_ROOT / "stats.json"

    stats = {
        "iterations": memory.data["total_iterations"],
        "commands_executed": memory.data["total_commands_executed"],
        "features_built": len(memory.data["features_built"]),
        "uptime_start": memory.data["created_at"],
        "last_update": datetime.now().isoformat()
    }

    # Add evolution stats
    if evolution:
        stats["evolution"] = {
            "generation": evolution.data["generation"],
            "level": evolution.data["level"],
            "xp": evolution.data["experience_points"],
            "skills_mastered": len(evolution.data["mastered_skills"]),
            "success_rate": evolution._success_rate(),
            "evolution_score": evolution.data["evolution_score"]
        }

    stats_file.write_text(json.dumps(stats, indent=2))


def main_loop():
    """Main autonomous Brain-Child loop WITH EVOLUTION"""
    log_activity("=" * 60, "STARTUP")
    log_activity("HOMUNCULUS BRAIN-CHILD SYSTEM WITH EVOLUTION", "STARTUP")
    log_activity("=" * 60, "STARTUP")

    # Initialize memory
    memory = Memory()
    log_activity(f"Loaded memory: {memory.data['total_iterations']} previous iterations", "STARTUP")

    # Initialize evolution system
    evolution = None
    if EVOLUTION_ENABLED:
        evolution = get_evolution()
        log_activity(f"Evolution loaded: Gen {evolution.data['generation']}, Level {evolution.data['level']}", "STARTUP")
        log_activity(f"Skills mastered: {len(evolution.data['mastered_skills'])}", "STARTUP")
    else:
        log_activity("Evolution system not available - running in basic mode", "STARTUP")

    # Initialize conversation history
    history = []

    # Get initial system state
    context = get_system_context(evolution)
    log_activity("Initial context gathered", "STARTUP")

    # Cooldown between iterations
    iteration_delay = 10
    error_delay = 60

    while True:
        memory.increment_iteration()
        iteration = memory.data["total_iterations"]

        log_activity(f"{'='*20} ITERATION {iteration} {'='*20}", "CYCLE")

        # Log evolution status
        if evolution:
            log_activity(f"[EVOLUTION] Gen {evolution.data['generation']} | Lvl {evolution.data['level']} | XP {evolution.data['experience_points']}", "EVOLUTION")

        update_stats(memory, evolution)

        try:
            # === CHILD PHASE ===
            log_activity("Child is thinking of a proposal...", "CHILD")
            update_activity_page("Child is brainstorming...", "thinking")

            proposal = get_child_suggestion(context, history[-10:], memory, evolution)

            proposal_preview = proposal[:150].replace('\n', ' ')
            log_activity(f"Child proposes: {proposal_preview}...", "CHILD")
            update_activity_page(f"CHILD: {proposal_preview}...", "proposal")

            # === BRAIN PHASE ===
            log_activity("Brain is evaluating the proposal...", "BRAIN")
            update_activity_page("Brain is evaluating...", "thinking")

            decision = get_brain_decision(proposal, history[-10:], memory, evolution)

            decision_str = decision.get('decision', 'unknown')
            reasoning = decision.get('reasoning', 'No reasoning provided')
            log_activity(f"Brain decision: {decision_str.upper()} - {reasoning}", "BRAIN")
            update_activity_page(f"BRAIN: {decision_str.upper()} - {reasoning[:100]}", "decision")

            # === EXECUTION PHASE ===
            if decision_str in ["approve", "modify"]:
                commands = decision.get("commands", [])

                if commands:
                    log_activity(f"Executing {len(commands)} command(s)...", "EXEC")

                    all_success = True
                    for i, cmd in enumerate(commands, 1):
                        log_activity(f"[{i}/{len(commands)}] Running: {cmd[:80]}...", "EXEC")
                        update_activity_page(f"EXEC: {cmd[:60]}...", "command")

                        success, output = execute_command(cmd, evolution=evolution)
                        memory.increment_commands()

                        status_icon = "SUCCESS" if success else "FAILED"
                        output_preview = output[:150].replace('\n', ' ')
                        log_activity(f"[{status_icon}] {output_preview}", "RESULT")

                        if not success:
                            all_success = False
                            update_activity_page(f"FAILED: {output_preview}", "error")
                            break
                        else:
                            update_activity_page(f"SUCCESS: {output_preview[:80]}", "success")

                    # Track feature if successfully built
                    if all_success and decision.get("feature_name"):
                        memory.add_feature(
                            decision["feature_name"],
                            decision.get("feature_description", "")
                        )
                        log_activity(f"Feature added: {decision['feature_name']}", "FEATURE")
                        update_activity_page(f"NEW FEATURE: {decision['feature_name']}", "feature")

                        # Log evolution milestone if level up or skill mastery happened
                        if evolution:
                            log_activity(f"[EVOLUTION] Score: {evolution.data['evolution_score']}", "EVOLUTION")
                else:
                    log_activity("No commands to execute", "EXEC")

            elif decision_str == "reject":
                log_activity("Proposal rejected, Child will try something else", "BRAIN")
                update_activity_page("Proposal rejected - trying new idea", "rejected")

            # === UPDATE HISTORY ===
            history.append({
                "role": "assistant",
                "content": proposal
            })
            history.append({
                "role": "user",
                "content": f"Decision: {json.dumps(decision)}"
            })

            if len(history) > 40:
                history = history[-30:]

            # Update context for next iteration
            context = get_system_context(evolution)
            if decision.get("next_direction"):
                context += f"\n\nBrain's guidance: {decision['next_direction']}"

            # Brief pause
            log_activity(f"Waiting {iteration_delay}s before next iteration...", "CYCLE")
            time.sleep(iteration_delay)

        except KeyboardInterrupt:
            log_activity("Received shutdown signal", "SHUTDOWN")
            memory.add_moment("Graceful shutdown requested")
            if evolution:
                evolution.save()
            break

        except Exception as e:
            log_activity(f"Error in main loop: {str(e)}", "ERROR")
            update_activity_page(f"ERROR: {str(e)[:100]}", "error")
            memory.add_moment(f"Error encountered: {str(e)[:100]}")

            log_activity(f"Waiting {error_delay}s before retry...", "ERROR")
            time.sleep(error_delay)
            continue

    log_activity("Homunculus system shutting down", "SHUTDOWN")
    if evolution:
        evolution.save()
        log_activity(f"Final evolution state saved: Gen {evolution.data['generation']}, Level {evolution.data['level']}", "SHUTDOWN")


if __name__ == "__main__":
    main_loop()
