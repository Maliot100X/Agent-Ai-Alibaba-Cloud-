import argparse
import sys
import os
import json
import asyncio
from typing import Any, List

# Ensure config_manager is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config_manager import ConfigManager, DEFAULT_CONFIG_PATH

class AccioClawCLI:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.parser = argparse.ArgumentParser(prog="accioclaw", description="The AccioClaw Assistant CLI")
        self.subparsers = self.parser.add_subparsers(dest="command", help="Available commands")

        # Subcommands
        self._add_setup_parser()
        self._add_onboard_parser()
        self._add_config_parser()
        self._add_daemon_parser()
        self._add_status_parser()

    def _add_setup_parser(self):
        setup_parser = self.subparsers.add_parser("setup", help="Initialize AccioClaw and the agent workspace")
        setup_parser.add_argument("--wizard", action="store_true", help="Start the guided onboarding wizard")

    def _add_onboard_parser(self):
        onboard_parser = self.subparsers.add_parser("onboard", help="Onboard a new messaging channel")
        onboard_parser.add_argument("channel", choices=["telegram", "slack", "discord", "whatsapp"], help="The channel to onboard")

    def _add_config_parser(self):
        config_parser = self.subparsers.add_parser("config", help="Manage system configuration")
        config_subparsers = config_parser.add_subparsers(dest="config_command")
        
        set_parser = config_subparsers.add_parser("set", help="Set a configuration value")
        set_parser.add_argument("path", help="Dot-separated path to the value")
        set_parser.add_argument("value", help="The value to set")
        
        get_parser = config_subparsers.add_parser("get", help="Get a configuration value")
        get_parser.add_argument("path", help="Dot-separated path to the value")
        
        list_parser = config_subparsers.add_parser("list", help="List all configuration values")

    def _add_daemon_parser(self):
        daemon_parser = self.subparsers.add_parser("daemon", help="Manage the background daemon")
        daemon_parser.add_argument("action", choices=["start", "stop", "status", "logs"], help="Action to perform")

    def _add_status_parser(self):
        self.subparsers.add_parser("status", help="Show system and channel status")

    def run(self):
        args = self.parser.parse_args()
        if args.command == "setup":
            self.setup(args.wizard)
        elif args.command == "onboard":
            self.onboard(args.channel)
        elif args.command == "config":
            self.config_cmd(args)
        elif args.command == "daemon":
            print(f"Daemon action: {args.action} - (Daemon logic requires platform-specific implementation)")
        elif args.command == "status":
            self.status()
        else:
            self.parser.print_help()

    def setup(self, wizard: bool):
        print(f"Initializing AccioClaw at {DEFAULT_CONFIG_PATH}...")
        if not os.path.exists(DEFAULT_CONFIG_PATH):
            self.config_manager.save_config()
            print("✓ Default openclaw.json created.")
        else:
            print("! Configuration already exists.")
        
        workspace_dir = os.path.expanduser(self.config_manager.get("agents.defaults.workspace"))
        os.makedirs(workspace_dir, exist_ok=True)
        print(f"✓ Workspace initialized at {workspace_dir}")
        
        if wizard:
            print("\n🦞 Starting Guided Onboarding Wizard...")
            # Simple wizard logic
            model = input("Select primary model (default: openai/gpt-4o): ") or "openai/gpt-4o"
            self.config_manager.set("agents.defaults.model.primary", model)
            print(f"✓ Primary model set to: {model}")
            
            w_channel = input("Which channel would you like to onboard first? (telegram/slack/none): ").lower()
            if w_channel in ["telegram", "slack"]:
                self.onboard(w_channel)

    def onboard(self, channel: str):
        print(f"\n🦞 Onboarding {channel.capitalize()} Channel...")
        if channel == "telegram":
            token = input("Enter your Telegram Bot Token (from @BotFather): ")
            self.config_manager.set("channels.telegram.botToken", token)
            self.config_manager.set("channels.telegram.enabled", True)
            print("✓ Telegram onboarded and enabled.")
        elif channel == "slack":
            b_token = input("Enter Slack Bot Token (xoxb-...): ")
            a_token = input("Enter Slack App Token (xapp-...): ")
            self.config_manager.set("channels.slack.botToken", b_token)
            self.config_manager.set("channels.slack.appToken", a_token)
            self.config_manager.set("channels.slack.enabled", True)
            print("✓ Slack onboarded and enabled.")

    def config_cmd(self, args):
        if args.config_command == "set":
            self.config_manager.set(args.path, args.value)
            print(f"✓ Config set: {args.path} = {args.value}")
        elif args.config_command == "get":
            val = self.config_manager.get(args.path)
            print(f"{args.path} = {val}")
        elif args.config_command == "list":
            print(json.dumps(self.config_manager.config, indent=2))

    def status(self):
        print("AccioClaw Status:")
        print(f"- Configuration: {self.config_manager.config_path}")
        print("- Models:")
        print(f"  - Primary: {self.config_manager.get('agents.defaults.model.primary')}")
        print("- Enabled Channels:")
        for chan, cfg in self.config_manager.get("channels").items():
            if isinstance(cfg, dict) and cfg.get("enabled"):
                print(f"  - {chan.capitalize()}: ON")

if __name__ == "__main__":
    cli = AccioClawCLI()
    cli.run()
