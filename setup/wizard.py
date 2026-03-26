import os
import sys
import argparse

# Ensure config_manager is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config_manager import ConfigManager, DEFAULT_CONFIG_PATH

class SetupWizard:
    def __init__(self):
        self.config_manager = ConfigManager()

    def start(self):
        print("\n" + "="*40)
        print("  🦞 Welcome to the AccioClaw Setup Wizard 🦞")
        print("="*40)
        print("This wizard will help you set up your personal AI assistant.")

        # 1. Workspace
        workspace = input(f"\n[1/4] Where should AccioClaw store its workspace? (default: ~/.accioclaw/workspace): ") or "~/.accioclaw/workspace"
        self.config_manager.set("agents.defaults.workspace", workspace)
        os.makedirs(os.path.expanduser(workspace), exist_ok=True)
        print(f"✓ Workspace set to: {workspace}")

        # 2. Primary Model
        print("\n[2/4] Choose your primary model:")
        print("1. OpenAI (gpt-4o)")
        print("2. Anthropic (claude-3-5-sonnet)")
        print("3. DeepSeek (deepseek-chat)")
        print("4. Custom")
        choice = input("Enter your choice (1-4, default: 1): ") or "1"
        
        models = {
            "1": "openai/gpt-4o",
            "2": "anthropic/claude-3-5-sonnet",
            "3": "deepseek/deepseek-chat",
            "4": "custom"
        }
        model_name = models.get(choice, "openai/gpt-4o")
        if choice == "4":
            model_name = input("Enter custom model name (e.g., 'google/gemini-pro'): ")
            
        self.config_manager.set("agents.defaults.model.primary", model_name)
        print(f"✓ Primary model set to: {model_name}")

        # 3. Onboarding Channels
        print("\n[3/4] Which channels do you want to enable? (y/n)")
        if input("Enable Telegram? ").lower() == "y":
            token = input("  - Enter Telegram Bot Token: ")
            self.config_manager.set("channels.telegram.botToken", token)
            self.config_manager.set("channels.telegram.enabled", True)
            print("  ✓ Telegram enabled.")

        if input("Enable Slack? ").lower() == "y":
            b_token = input("  - Enter Slack Bot Token (xoxb-...): ")
            a_token = input("  - Enter Slack App Token (xapp-...): ")
            self.config_manager.set("channels.slack.botToken", b_token)
            self.config_manager.set("channels.slack.appToken", a_token)
            self.config_manager.set("channels.slack.enabled", True)
            print("  ✓ Slack enabled.")

        # 4. Final Review
        print("\n[4/4] Setup complete!")
        print(f"Configuration saved to: {DEFAULT_CONFIG_PATH}")
        print("\nTo start your assistant, run:")
        print("  accioclaw daemon start")
        print("\n" + "="*40)

if __name__ == "__main__":
    wizard = SetupWizard()
    wizard.start()
