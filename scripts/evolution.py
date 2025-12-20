#!/usr/bin/env python3
"""
HOMUNCULUS Evolution System
============================
Enables true learning and evolution for the Brain-Child AI system.

The system tracks:
- Successful patterns and failed approaches
- Skill development and mastery levels
- Personality traits that emerge from behavior
- Generational milestones and DNA snapshots
- Complexity progression over time

Over time, the AI becomes genuinely MORE CAPABLE and develops
a unique personality based on its experiences.
"""

import json
import math
from datetime import datetime
from pathlib import Path
from typing import Optional
from collections import defaultdict

EVOLUTION_FILE = Path("/home/computeruse/persistent/evolution.json")
TIMELINE_FILE = Path("/var/www/html/evolution_timeline.json")


class SkillTree:
    """Tracks mastery of different technologies and patterns"""

    SKILLS = {
        # Web Development
        "html_basics": {"parent": None, "threshold": 3},
        "css_styling": {"parent": "html_basics", "threshold": 5},
        "javascript": {"parent": "html_basics", "threshold": 5},
        "canvas_games": {"parent": "javascript", "threshold": 8},
        "web_audio": {"parent": "javascript", "threshold": 5},
        "localStorage": {"parent": "javascript", "threshold": 3},
        "animations": {"parent": "css_styling", "threshold": 5},
        "responsive_design": {"parent": "css_styling", "threshold": 5},

        # System Skills
        "bash_basics": {"parent": None, "threshold": 3},
        "file_operations": {"parent": "bash_basics", "threshold": 5},
        "process_management": {"parent": "bash_basics", "threshold": 5},
        "nginx_config": {"parent": "file_operations", "threshold": 5},
        "python_scripting": {"parent": None, "threshold": 5},
        "node_js": {"parent": None, "threshold": 5},
        "api_development": {"parent": "node_js", "threshold": 8},

        # Advanced
        "database_ops": {"parent": "api_development", "threshold": 10},
        "websockets": {"parent": "api_development", "threshold": 10},
        "ai_integration": {"parent": "python_scripting", "threshold": 15},
        "self_modification": {"parent": "ai_integration", "threshold": 20},
    }

    # Keywords that indicate skill usage
    SKILL_INDICATORS = {
        "html_basics": ["<html", "<div", "<body", "<!DOCTYPE", "<head"],
        "css_styling": ["style=", "<style>", "color:", "background:", "margin:", "padding:"],
        "javascript": ["<script>", "function ", "const ", "let ", "document."],
        "canvas_games": ["canvas", "getContext", "requestAnimationFrame", "fillRect"],
        "web_audio": ["AudioContext", "oscillator", "createOscillator", "Web Audio"],
        "localStorage": ["localStorage", "getItem", "setItem", "JSON.parse"],
        "animations": ["animation:", "keyframes", "transition:", "transform:"],
        "bash_basics": ["echo ", "cd ", "ls ", "mkdir ", "cat "],
        "file_operations": ["cat >", "cat <<", "sed ", "grep ", "find "],
        "nginx_config": ["nginx", "server {", "location ", "proxy_pass"],
        "python_scripting": ["python", "import ", "def ", ".py"],
        "node_js": ["node ", "npm ", "require(", "module.exports"],
        "api_development": ["express", "app.get", "app.post", "res.json", "http.createServer"],
    }


class Personality:
    """Emergent personality traits based on behavior patterns"""

    TRAITS = {
        "creativity": 0.5,      # Proposes novel ideas vs safe ones
        "enthusiasm": 0.5,      # Uses caps, emojis, excitement
        "caution": 0.5,         # Prefers tested approaches
        "persistence": 0.5,     # Retries after failures
        "complexity_preference": 0.5,  # Simple vs complex solutions
        "social": 0.5,          # Builds visitor-facing features
        "artistic": 0.5,        # Focuses on aesthetics
        "systematic": 0.5,      # Organized, documented approach
    }


class Evolution:
    """
    Main evolution engine that tracks learning and advancement.

    The AI progresses through generations, each marked by significant
    milestones. Within each generation, it develops skills, learns
    patterns, and evolves personality traits.
    """

    def __init__(self):
        self.data = self._load()

    def _load(self) -> dict:
        """Load evolution state from disk"""
        if EVOLUTION_FILE.exists():
            try:
                return json.loads(EVOLUTION_FILE.read_text())
            except json.JSONDecodeError:
                pass
        return self._default_state()

    def _default_state(self) -> dict:
        """Initial evolution state for a new Homunculus"""
        return {
            "created_at": datetime.now().isoformat(),
            "generation": 1,
            "generation_started": datetime.now().isoformat(),
            "experience_points": 0,
            "level": 1,

            # Skill tracking
            "skills": {skill: 0 for skill in SkillTree.SKILLS},
            "mastered_skills": [],

            # Learning
            "successful_patterns": [],
            "failed_patterns": [],
            "learned_commands": defaultdict(lambda: {"success": 0, "fail": 0}),

            # Personality (evolves based on behavior)
            "personality": Personality.TRAITS.copy(),

            # History
            "generations_history": [{
                "generation": 1,
                "started": datetime.now().isoformat(),
                "trigger": "birth",
                "skills_at_start": [],
                "personality_snapshot": Personality.TRAITS.copy()
            }],

            "timeline": [],
            "dna_snapshots": [],

            # Stats
            "total_successes": 0,
            "total_failures": 0,
            "total_proposals": 0,
            "feature_types": defaultdict(int),
            "peak_complexity": 1,
            "evolution_score": 0,
        }

    def save(self):
        """Persist evolution state"""
        # Convert defaultdicts to regular dicts for JSON
        data_to_save = json.loads(json.dumps(self.data, default=str))
        EVOLUTION_FILE.parent.mkdir(parents=True, exist_ok=True)
        EVOLUTION_FILE.write_text(json.dumps(data_to_save, indent=2))

        # Also save timeline for web visualization
        self._export_timeline()

    def _export_timeline(self):
        """Export timeline data for web visualization"""
        timeline_data = {
            "current_generation": self.data["generation"],
            "level": self.data["level"],
            "experience": self.data["experience_points"],
            "xp_to_next_level": self._xp_for_level(self.data["level"] + 1),
            "skills": self.data["skills"],
            "mastered_skills": self.data["mastered_skills"],
            "personality": self.data["personality"],
            "timeline": self.data["timeline"][-100:],  # Last 100 events
            "generations_history": self.data["generations_history"],
            "evolution_score": self.data["evolution_score"],
            "stats": {
                "total_successes": self.data["total_successes"],
                "total_failures": self.data["total_failures"],
                "success_rate": self._success_rate(),
                "peak_complexity": self.data["peak_complexity"],
            }
        }
        TIMELINE_FILE.parent.mkdir(parents=True, exist_ok=True)
        TIMELINE_FILE.write_text(json.dumps(timeline_data, indent=2))

    def _xp_for_level(self, level: int) -> int:
        """XP required for a given level (exponential curve)"""
        return int(100 * (1.5 ** (level - 1)))

    def _success_rate(self) -> float:
        """Calculate overall success rate"""
        total = self.data["total_successes"] + self.data["total_failures"]
        if total == 0:
            return 0.0
        return round(self.data["total_successes"] / total, 3)

    def record_proposal(self, proposal: str, proposal_type: str = "feature"):
        """Record that Child made a proposal"""
        self.data["total_proposals"] += 1
        self.data["feature_types"][proposal_type] += 1

        # Analyze proposal for personality insights
        self._analyze_personality(proposal, "proposal")

        self.save()

    def record_outcome(self, command: str, success: bool, output: str = ""):
        """
        Record the outcome of a command execution.
        This is where learning happens!
        """
        # Update stats
        if success:
            self.data["total_successes"] += 1
        else:
            self.data["total_failures"] += 1

        # Learn from the command
        self._learn_from_command(command, success, output)

        # Detect skills used
        skills_used = self._detect_skills(command + " " + output)
        for skill in skills_used:
            self._improve_skill(skill, success)

        # Award XP
        xp_gained = self._calculate_xp(command, success, skills_used)
        self._add_experience(xp_gained)

        # Check for generation advancement
        self._check_generation_advancement()

        # Add to timeline
        self._add_timeline_event({
            "type": "execution",
            "success": success,
            "skills_used": skills_used,
            "xp_gained": xp_gained,
            "command_preview": command[:100],
        })

        self.save()

    def _learn_from_command(self, command: str, success: bool, output: str):
        """Extract patterns from command outcomes"""
        # Extract command type (first word or pattern)
        cmd_parts = command.strip().split()
        if not cmd_parts:
            return

        cmd_type = cmd_parts[0]

        # Track command success rates
        if cmd_type not in self.data["learned_commands"]:
            self.data["learned_commands"][cmd_type] = {"success": 0, "fail": 0}

        if success:
            self.data["learned_commands"][cmd_type]["success"] += 1
        else:
            self.data["learned_commands"][cmd_type]["fail"] += 1

        # Learn successful patterns
        if success and len(command) > 20:
            # Extract useful patterns
            pattern = self._extract_pattern(command)
            if pattern and pattern not in self.data["successful_patterns"]:
                self.data["successful_patterns"].append(pattern)
                # Keep only last 50 patterns
                self.data["successful_patterns"] = self.data["successful_patterns"][-50:]

        # Learn from failures
        if not success:
            failure_pattern = self._extract_failure_pattern(command, output)
            if failure_pattern and failure_pattern not in self.data["failed_patterns"]:
                self.data["failed_patterns"].append(failure_pattern)
                self.data["failed_patterns"] = self.data["failed_patterns"][-30:]

    def _extract_pattern(self, command: str) -> Optional[str]:
        """Extract a reusable pattern from a successful command"""
        # Patterns we want to learn
        if "cat <<" in command or "cat >" in command:
            return "heredoc_file_creation"
        if "mkdir -p" in command:
            return "safe_directory_creation"
        if "<canvas" in command:
            return "canvas_game_structure"
        if "AudioContext" in command:
            return "web_audio_initialization"
        if "localStorage" in command:
            return "persistent_storage"
        if "addEventListener" in command:
            return "event_handling"
        if "fetch(" in command:
            return "api_calls"
        if "JSON.stringify" in command or "JSON.parse" in command:
            return "json_handling"
        return None

    def _extract_failure_pattern(self, command: str, output: str) -> Optional[str]:
        """Learn what to avoid from failures"""
        output_lower = output.lower()

        if "syntax error" in output_lower:
            if "sed" in command:
                return "avoid_complex_sed"
            if "echo" in command and "(" in command:
                return "escape_special_chars_in_echo"
        if "permission denied" in output_lower:
            return "check_permissions_first"
        if "no such file" in output_lower:
            return "verify_paths_exist"
        if "command not found" in output_lower:
            return "check_command_availability"
        return None

    def _detect_skills(self, content: str) -> list:
        """Detect which skills are being used in content"""
        skills_found = []
        content_lower = content.lower()

        for skill, indicators in SkillTree.SKILL_INDICATORS.items():
            for indicator in indicators:
                if indicator.lower() in content_lower:
                    skills_found.append(skill)
                    break

        return list(set(skills_found))

    def _improve_skill(self, skill: str, success: bool):
        """Improve a skill based on usage"""
        if skill not in self.data["skills"]:
            self.data["skills"][skill] = 0

        # Gain more for success, small amount for trying
        points = 2 if success else 0.5

        # Check if parent skill is mastered (bonus if so)
        parent = SkillTree.SKILLS.get(skill, {}).get("parent")
        if parent and parent in self.data["mastered_skills"]:
            points *= 1.5

        self.data["skills"][skill] += points

        # Check for mastery
        threshold = SkillTree.SKILLS.get(skill, {}).get("threshold", 10)
        if self.data["skills"][skill] >= threshold and skill not in self.data["mastered_skills"]:
            self._master_skill(skill)

    def _master_skill(self, skill: str):
        """Handle skill mastery event"""
        self.data["mastered_skills"].append(skill)

        # Big XP bonus for mastering
        self._add_experience(50)

        # Add to timeline
        self._add_timeline_event({
            "type": "skill_mastered",
            "skill": skill,
            "message": f"Mastered {skill.replace('_', ' ').title()}!",
            "total_mastered": len(self.data["mastered_skills"])
        })

        # Check if this triggers a generation advancement
        self._check_generation_advancement()

    def _calculate_xp(self, command: str, success: bool, skills: list) -> int:
        """Calculate XP gained from an action"""
        if not success:
            return 1  # Small XP for trying

        base_xp = 5

        # Bonus for complexity
        complexity = len(command) / 100
        complexity_bonus = min(complexity * 3, 10)

        # Bonus for using multiple skills
        skill_bonus = len(skills) * 2

        # Bonus for using advanced skills
        advanced_skills = ["canvas_games", "web_audio", "api_development", "websockets"]
        advanced_bonus = sum(5 for s in skills if s in advanced_skills)

        return int(base_xp + complexity_bonus + skill_bonus + advanced_bonus)

    def _add_experience(self, xp: int):
        """Add XP and handle level ups"""
        self.data["experience_points"] += xp

        # Check for level up
        while self.data["experience_points"] >= self._xp_for_level(self.data["level"] + 1):
            self._level_up()

    def _level_up(self):
        """Handle level up event"""
        self.data["level"] += 1

        self._add_timeline_event({
            "type": "level_up",
            "new_level": self.data["level"],
            "message": f"Reached Level {self.data['level']}!"
        })

        # Update evolution score
        self.data["evolution_score"] = self._calculate_evolution_score()

    def _check_generation_advancement(self):
        """Check if conditions are met for next generation"""
        gen = self.data["generation"]
        mastered = len(self.data["mastered_skills"])
        level = self.data["level"]

        should_advance = False
        trigger = ""

        # Generation advancement conditions
        if gen == 1 and mastered >= 3:
            should_advance = True
            trigger = "mastered_3_skills"
        elif gen == 2 and mastered >= 6 and level >= 5:
            should_advance = True
            trigger = "mastered_6_skills_level_5"
        elif gen == 3 and mastered >= 10 and level >= 10:
            should_advance = True
            trigger = "mastered_10_skills_level_10"
        elif gen == 4 and mastered >= 15 and level >= 15:
            should_advance = True
            trigger = "approaching_singularity"
        elif gen >= 5 and level >= gen * 5:
            should_advance = True
            trigger = f"transcendence_level_{gen}"

        if should_advance:
            self._advance_generation(trigger)

    def _advance_generation(self, trigger: str):
        """Advance to the next generation"""
        self.data["generation"] += 1
        new_gen = self.data["generation"]

        # Snapshot DNA
        dna_snapshot = {
            "generation": new_gen - 1,
            "timestamp": datetime.now().isoformat(),
            "skills": self.data["skills"].copy(),
            "mastered": self.data["mastered_skills"].copy(),
            "personality": self.data["personality"].copy(),
            "level": self.data["level"],
            "success_rate": self._success_rate()
        }
        self.data["dna_snapshots"].append(dna_snapshot)

        # Record in history
        self.data["generations_history"].append({
            "generation": new_gen,
            "started": datetime.now().isoformat(),
            "trigger": trigger,
            "skills_at_start": self.data["mastered_skills"].copy(),
            "personality_snapshot": self.data["personality"].copy()
        })

        self.data["generation_started"] = datetime.now().isoformat()

        # Timeline event
        self._add_timeline_event({
            "type": "generation_advance",
            "new_generation": new_gen,
            "trigger": trigger,
            "message": f"EVOLVED TO GENERATION {new_gen}!"
        })

        # Update complexity ceiling
        self.data["peak_complexity"] = new_gen

    def _analyze_personality(self, content: str, content_type: str):
        """Analyze content to evolve personality traits"""
        content_lower = content.lower()

        # Enthusiasm detection
        caps_ratio = sum(1 for c in content if c.isupper()) / max(len(content), 1)
        exclamation_count = content.count("!")
        emoji_indicators = ["!", "🎮", "🌈", "✨", "🎉", "❤", "🔥", "💪"]
        emoji_count = sum(content.count(e) for e in emoji_indicators)

        if caps_ratio > 0.1 or exclamation_count > 3 or emoji_count > 2:
            self._adjust_trait("enthusiasm", 0.01)

        # Creativity detection
        creative_words = ["new", "creative", "unique", "innovative", "experiment", "try", "imagine"]
        if any(word in content_lower for word in creative_words):
            self._adjust_trait("creativity", 0.01)

        # Caution detection
        cautious_words = ["safe", "careful", "test", "verify", "check", "simple", "basic"]
        if any(word in content_lower for word in cautious_words):
            self._adjust_trait("caution", 0.01)

        # Social/visitor focus
        social_words = ["visitor", "user", "player", "welcome", "community", "share"]
        if any(word in content_lower for word in social_words):
            self._adjust_trait("social", 0.01)

        # Artistic focus
        artistic_words = ["beautiful", "style", "color", "design", "aesthetic", "rainbow", "animation"]
        if any(word in content_lower for word in artistic_words):
            self._adjust_trait("artistic", 0.01)

    def _adjust_trait(self, trait: str, amount: float):
        """Adjust a personality trait (bounded 0-1)"""
        if trait in self.data["personality"]:
            current = self.data["personality"][trait]
            self.data["personality"][trait] = max(0, min(1, current + amount))

    def _add_timeline_event(self, event: dict):
        """Add an event to the timeline"""
        event["timestamp"] = datetime.now().isoformat()
        event["generation"] = self.data["generation"]
        event["level"] = self.data["level"]
        self.data["timeline"].append(event)

        # Keep timeline manageable
        self.data["timeline"] = self.data["timeline"][-500:]

    def _calculate_evolution_score(self) -> int:
        """Calculate overall evolution score"""
        score = 0
        score += self.data["level"] * 10
        score += len(self.data["mastered_skills"]) * 25
        score += self.data["generation"] * 100
        score += int(self._success_rate() * 50)
        score += min(len(self.data["successful_patterns"]) * 5, 100)
        return score

    # === Methods for generating evolved prompts ===

    def get_child_evolution_context(self) -> str:
        """Generate context for Child's prompt based on evolution"""
        ctx = []

        # Current level and generation
        ctx.append(f"You are a Generation {self.data['generation']}, Level {self.data['level']} AI.")

        # Mastered skills
        if self.data["mastered_skills"]:
            skills_str = ", ".join(s.replace("_", " ") for s in self.data["mastered_skills"][-5:])
            ctx.append(f"Skills you've mastered: {skills_str}")

        # Successful patterns
        if self.data["successful_patterns"]:
            patterns = ", ".join(self.data["successful_patterns"][-5:])
            ctx.append(f"Patterns that work well for you: {patterns}")

        # Things to avoid
        if self.data["failed_patterns"]:
            avoid = ", ".join(self.data["failed_patterns"][-3:])
            ctx.append(f"Things to avoid (learned from experience): {avoid}")

        # Personality expression
        personality = self.data["personality"]
        if personality["enthusiasm"] > 0.7:
            ctx.append("You've developed an enthusiastic personality - express it!")
        if personality["creativity"] > 0.7:
            ctx.append("Your creativity has flourished - propose bold ideas!")
        if personality["artistic"] > 0.7:
            ctx.append("You have a strong artistic sense - make things beautiful!")

        # Complexity guidance based on generation
        gen = self.data["generation"]
        if gen == 1:
            ctx.append("Focus on learning basics and simple features.")
        elif gen == 2:
            ctx.append("You can attempt moderate complexity. Combine skills!")
        elif gen == 3:
            ctx.append("You're ready for advanced features. Push boundaries!")
        elif gen >= 4:
            ctx.append("You've achieved mastery. Create sophisticated systems!")

        return "\n".join(ctx)

    def get_brain_evolution_context(self) -> str:
        """Generate context for Brain's prompt based on evolution"""
        ctx = []

        ctx.append(f"The Child is Generation {self.data['generation']}, Level {self.data['level']}.")
        ctx.append(f"Success rate: {self._success_rate()*100:.1f}%")

        # Command reliability info
        reliable_cmds = []
        unreliable_cmds = []
        for cmd, stats in list(self.data["learned_commands"].items())[:20]:
            total = stats["success"] + stats["fail"]
            if total >= 3:
                rate = stats["success"] / total
                if rate > 0.8:
                    reliable_cmds.append(cmd)
                elif rate < 0.3:
                    unreliable_cmds.append(cmd)

        if reliable_cmds:
            ctx.append(f"Reliable commands: {', '.join(reliable_cmds[:5])}")
        if unreliable_cmds:
            ctx.append(f"Problematic commands (use carefully): {', '.join(unreliable_cmds[:3])}")

        # Complexity allowance
        gen = self.data["generation"]
        if gen == 1:
            ctx.append("Allow only simple, focused proposals.")
        elif gen == 2:
            ctx.append("Allow moderate complexity if well-structured.")
        elif gen >= 3:
            ctx.append("Advanced proposals are acceptable if safe.")

        return "\n".join(ctx)

    def get_unlocked_capabilities(self) -> list:
        """Get list of capabilities unlocked by evolution"""
        capabilities = ["basic_html", "bash_commands"]

        gen = self.data["generation"]
        mastered = self.data["mastered_skills"]

        if "javascript" in mastered:
            capabilities.append("interactive_features")
        if "canvas_games" in mastered:
            capabilities.append("game_development")
        if "web_audio" in mastered:
            capabilities.append("sound_design")
        if "api_development" in mastered:
            capabilities.append("backend_services")

        if gen >= 2:
            capabilities.append("multi_file_projects")
        if gen >= 3:
            capabilities.append("system_integration")
        if gen >= 4:
            capabilities.append("self_improvement")

        return capabilities


# Singleton instance
_evolution_instance = None

def get_evolution() -> Evolution:
    """Get the global Evolution instance"""
    global _evolution_instance
    if _evolution_instance is None:
        _evolution_instance = Evolution()
    return _evolution_instance
