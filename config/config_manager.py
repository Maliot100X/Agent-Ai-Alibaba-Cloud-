import os
import json5
from typing import Any, Dict

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.accioclaw/openclaw.json")

class ConfigManager:
    def __init__(self, config_path: str = DEFAULT_CONFIG_PATH):
        self.config_path = config_path
        self.config: Dict[str, Any] = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Loads and parses the openclaw.json file (JSON5)."""
        if not os.path.exists(self.config_path):
            return self.get_default_config()
        
        try:
            with open(self.config_path, "r") as f:
                return json5.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.get_default_config()

    def save_config(self):
        """Saves the current config back to openclaw.json."""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        try:
            with open(self.config_path, "w") as f:
                json5.dump(self.config, f, indent=2, quote_keys=True)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, path: str, default: Any = None) -> Any:
        """Gets a value from the config using a dot-separated path."""
        parts = path.split(".")
        val = self.config
        for part in parts:
            if isinstance(val, dict) and part in val:
                val = val[part]
            else:
                return default
        return val

    def set(self, path: str, value: Any):
        """Sets a value in the config using a dot-separated path."""
        parts = path.split(".")
        val = self.config
        for i, part in enumerate(parts[:-1]):
            if part not in val or not isinstance(val[part], dict):
                val[part] = {}
            val = val[part]
        val[parts[-1]] = value
        self.save_config()

    def get_default_config(self) -> Dict[str, Any]:
        """Returns the base OpenClaw configuration template."""
        return {
            "channels": {
                "defaults": {
                    "groupPolicy": "allowlist",
                    "heartbeat": {"showOk": False, "showAlerts": True, "useIndicator": True}
                },
                "telegram": {"enabled": False, "botToken": "", "dmPolicy": "pairing"},
                "slack": {"enabled": False, "botToken": "", "appToken": "", "socketMode": True},
                "discord": {"enabled": False, "token": ""},
                "whatsapp": {"enabled": False}
            },
            "agents": {
                "defaults": {
                    "workspace": "~/.accioclaw/workspace",
                    "model": {"primary": "openai/gpt-4o", "fallbacks": []},
                    "sandbox": {"mode": "non-main", "backend": "docker"}
                },
                "list": [
                    {"id": "main", "default": True, "identity": {"name": "AccioClaw", "emoji": "🦞"}}
                ]
            },
            "logging": {"level": "info"}
        }

if __name__ == "__main__":
    cm = ConfigManager("./test_config.json")
    cm.set("channels.telegram.enabled", True)
    print(cm.get("channels.telegram.enabled"))
    cm.save_config()
