# 🚀 Ignitos Telegram Auto-Reply Bot Deployment Guide

<p align="center">
  <img src="https://placehold.co/1000x250/161b22/8b949e?text=Modular+Telegram+Self-Bot+with+AI+%26+Image+Generation" alt="Modular Telegram Bot with AI and Image Generation" />
</p>

## 🌟 Overview

Ignitos is a modular Telegram self-bot framework built with Pyrogram, designed for automated replies and extended functionality using AI plugins powered by Gemini API and Imagen 3.

Deploy it on a VPS to run 24/7 and manage your Telegram account with powerful commands.

---

## ✨ Features at a Glance

| Command Type    | Prefix       | Description                                  | Powered By       |
|-----------------|-------------|----------------------------------------------|------------------|
| AI Generation   | `.ai` or `/ai` | Answers questions using Gemini API with Google Search grounding | `plugins/ai.py`  |
| Image Generation| `.img` or `/img` | Generates images using Imagen 3 API (Text-to-Image) | `plugins/image_gen.py` |
| Auto-Reply      | Core         | Automatically replies to private messages when set to `.away` | `main.py`        |

---

## ⚙️ Prerequisites

- **Linux VPS**: Ubuntu, Debian, or CentOS.
- **SSH Access**: Ability to connect to your server.
- **Telegram API Credentials**: API ID and API Hash from [my.telegram.org](https://my.telegram.org).
- **BotFather Token**: For the remote control bot.
- **Gemini API Key**: Required for all AI features (`.ai` and `.img`).

---

## 🛠️ Deployment Steps (Linux VPS)

### Step 1: Prepare the VPS Environment

Log in via SSH and install the necessary system packages.

```bash
sudo apt update && sudo apt install python3 python3-pip git -y
```

### Step 2: Set Up Project Structure and Virtual Environment

Always use a virtual environment (venv) for dependency isolation.

```bash
sudo apt install python3-venv -y
mkdir ignitos_bot && cd ignitos_bot
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Clone Code and Install Dependencies

Transfer your source code and install required Python libraries.

```bash
# Clone your repository (REPLACE with your actual GitHub URL)
git clone [YOUR_REPOSITORY_URL] .

# Install all required Python libraries. Ensure (venv) is active!
pip install -r requirements.txt
```

### Step 4: Run for Initial Configuration

Run the bot interactively once to complete setup and save credentials.

```bash
python3 main.py
```

Follow the on-screen prompts for all API keys and Telegram login.

### Step 5: Run the Bot Continuously (24/7)

Use the screen utility to keep the bot running after disconnecting from SSH.

```bash
sudo apt install screen -y
screen -S ignitos_session
python3 main.py
```

To detach from screen: Press `Ctrl + A` then `D`. You can now safely log out.

---

## 📚 Bot Command Reference

Commands are categorized by their prefix:  
- **User Bot commands (`.`)** are sent from your account  
- **Control Bot commands (`/`)** are sent to the BotFather bot instance

| Function         | User Bot Command (Self) | Control Bot Command (BotFather) | Example Usage                |
|------------------|------------------------|---------------------------------|------------------------------|
| AI Question      | `.ai [prompt]`         | `/ai [prompt]`                  | `.ai What is the capital of Canada?` |
| Image Generation | `.img [prompt]`        | `/img [prompt]`                 | `.img A hyperrealistic neon tiger.` |
| Check Latency    | `.ping`                | -                               | `.ping`                      |
| Enable Auto-Reply| `.away`                | -                               | `.away`                      |
| Disable Auto-Reply| `.online`             | -                               | `.online`                    |
| Set Offline Message| `.editoff [message]` | -                               | `.editoff I am busy coding.` |

---

## 💻 Console Management Commands

| Action                  | Command                       | Notes                                    |
|-------------------------|------------------------------|------------------------------------------|
| Re-attach to the console| `screen -r ignitos_session`  | See the bot's live logs and output.      |
| Stop the bot entirely   | Re-attach, then press `Ctrl + C` | Stops the Python script inside screen. |
| List all active sessions| `screen -ls`                 | Shows all detached sessions.             |

---

Enjoy your turbocharged Telegram userbot! 🚀❤️
