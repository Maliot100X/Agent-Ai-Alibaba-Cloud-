import os
import yaml
import json
import sys
from typing import List, Dict, Any

# Ensure project modules are importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config_manager import ConfigManager

class AccioClawAgent:
    def __init__(self, agent_id: str = "main"):
        self.config_manager = ConfigManager()
        self.agent_id = agent_id
        self.agent_config = self.get_agent_config(agent_id)
        self.workspace = os.path.expanduser(self.agent_config.get("workspace", "~/.accioclaw/workspace"))
        self.skills_dir = os.path.join(self.workspace, "skills")
        os.makedirs(self.skills_dir, exist_ok=True)
        self.skills = self.load_skills()

    def get_agent_config(self, agent_id: str) -> Dict[str, Any]:
        """Retrieves the config for a specific agent, merging defaults."""
        defaults = self.config_manager.get("agents.defaults", {})
        agent_list = self.config_manager.get("agents.list", [])
        
        agent_item = next((a for a in agent_list if a.get("id") == agent_id), {})
        return {**defaults, **agent_item}

    def load_skills(self) -> Dict[str, Dict[str, Any]]:
        """Scans the skills directory and loads SKILL.md frontmatter."""
        skills = {}
        for root, dirs, files in os.walk(self.skills_dir):
            if "SKILL.md" in files:
                skill_path = os.path.join(root, "SKILL.md")
                try:
                    with open(skill_path, "r") as f:
                        content = f.read()
                        if content.startswith("---"):
                            _, frontmatter, body = content.split("---", 2)
                            metadata = yaml.safe_load(frontmatter)
                            skills[metadata["name"]] = {
                                "metadata": metadata,
                                "body": body,
                                "path": root
                            }
                except Exception as e:
                    print(f"! Error loading skill at {skill_path}: {e}")
        return skills

    def execute_tool(self, skill_name: str, tool_name: str, params: Dict[str, Any]):
        """Executes a specific tool within the agent's sandbox environment."""
        if skill_name not in self.skills:
            return {"ok": False, "error": f"Skill '{skill_name}' not found."}
        
        print(f"🦞 Agent {self.agent_id} executing {skill_name}.{tool_name}...")
        # Add actual tool execution logic here (mapping to Accio skills)
        return {
            "ok": True, 
            "payload": {
                "agent_id": self.agent_id,
                "skill": skill_name,
                "tool": tool_name,
                "result": "Simulated B2B insight/sourcing result"
            }
        }

if __name__ == "__main__":
    agent = AccioClawAgent()
    print(f"AccioClaw Agent initialized: {agent.agent_id}")
    print(f"Workspace: {agent.workspace}")
    print(f"Primary Model: {agent.agent_config.get('model', {}).get('primary')}")
