# AccioClaw: The Personal B2B AI Assistant 🦞

AccioClaw is a feature-rich, OpenClaw-compatible personal AI assistant framework designed for autonomous B2B operations. It features a long-lived Gateway, a modular Skills system, and easy messaging platform integrations.

## 🚀 Easy Setup

Setting up AccioClaw takes less than 5 minutes with our guided wizard:

```bash
git clone https://github.com/Maliot100X/Agent-Ai-Alibaba-Cloud-.git
cd Agent-Ai-Alibaba-Cloud-
pip install -r requirements.txt
python cli/accioclaw.py setup --wizard
```

## 🛠️ CLI Commands

The `accioclaw` CLI allows you to manage the entire system from your terminal:

- `setup --wizard`: Interactive setup script for your assistant.
- `onboard <channel>`: Guided onboarding for Telegram, Slack, Discord, or WhatsApp.
- `daemon <start|stop|status|logs>`: Manage the background gateway service.
- `config <get|set|list> <path>`: View or modify system settings.
- `status`: Check the health of your assistant and connected channels.

## 🦞 Core Components

- **Gateway (Core Hub)**: The central control plane that handles all messaging and session routing. Implements the OpenClaw 1.0.0 WebSocket protocol.
- **Config Manager**: Handles the `~/.accioclaw/openclaw.json` (JSON5) configuration, storing all your secrets, models, and channel settings.
- **Agent Runtime**: The execution loop for autonomous skills, supporting multi-model routing (Image, PDF, etc.).
- **Messaging Adapters**: Standardized adapters for Telegram (via `python-telegram-bot`), Slack (via `slack-sdk` Socket Mode), and Discord.

## 📂 Configuration (openclaw.json)

AccioClaw uses a single `openclaw.json` file for all configuration, supporting comments and trailing commas:

```json5
{
  "channels": {
    "telegram": { "enabled": true, "botToken": "YOUR_TOKEN" },
    "slack": { "enabled": true, "botToken": "...", "appToken": "..." }
  },
  "agents": {
    "defaults": {
      "model": { "primary": "openai/gpt-4o" },
      "workspace": "~/.accioclaw/workspace"
    }
  }
}
```

## 📦 Requirements (requirements.txt)
json5==0.13.0
python-telegram-bot==22.7
slack-sdk==3.41.0
discord.py==2.7.1
fastapi==0.135.2
uvicorn==0.42.0
websockets==15.0.1
pyyaml==5.4.1
