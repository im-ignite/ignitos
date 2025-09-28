🚀 Ignitos Telegram Auto-Reply Bot Deployment Guide
<p align="center">
<img src="https://www.google.com/search?q=https://placehold.co/1000x250/161b22/8b949e%3Ftext%3DModular%2BTelegram%2BSelf-Bot%2Bwith%2BAI%2B%2526%2BImage%2BGeneration" alt="Modular Telegram Bot with AI and Image Generation">
</p>

🌟 Overview
This bot is a modular Telegram self-bot framework built on Pyrogram, designed for automated replies and extended functionality using AI plugins powered by the Gemini API and Imagen 3.

Deploy it on a VPS to run 24/7 and manage your Telegram account with powerful commands.

✨ Features at a Glance
Command Type

Prefix

Description

Powered By

AI Generation

.ai / /ai

Answers questions using the Gemini API with Google Search grounding.

plugins/ai.py

Image Generation

.img / /img

Generates images using the Imagen 3 API (Text-to-Image).

plugins/image_gen.py

Auto-Reply

Core

Automatically replies to private messages when set to .away.

main.py

⚙️ Prerequisites
You will need the following information and resources:

A Linux VPS: Running Ubuntu, Debian, or CentOS.

SSH Access: To connect to your server.

Telegram API Credentials: API ID and API Hash (from my.telegram.org).

BotFather Token: For the remote control bot.

Gemini API Key: Required for all AI features (.ai and .img).

🛠️ Deployment Steps (Linux VPS)
Step 1: Prepare the VPS Environment
Log in via SSH and install the necessary system packages.

# Update package list and install Python 3, pip, and git
$ sudo apt update && sudo apt install python3 python3-pip git -y

Step 2: Set Up Project Structure and Virtual Environment
Always use a virtual environment (venv) for dependency isolation.

# Install venv, create directory, and activate venv
$sudo apt install python3-venv -y$ mkdir ignitos_bot && cd ignitos_bot
$python3 -m venv venv$ source venv/bin/activate

Step 3: Clone Code and Install Dependencies
Transfer your source code and install the required Python libraries.

# Clone your repository (REPLACE with your actual GitHub URL)
$ git clone [YOUR_REPOSITORY_URL] .

# Install all required Python libraries. Ensure (venv) is active!
$ pip install -r requirements.txt

Step 4: Run for Initial Configuration
The bot needs to run interactively once to complete the initial setup and save credentials.

# Run the script and follow the on-screen prompts for all API keys and Telegram login
$ python3 main.py

Step 5: Run the Bot Continuously (24/7)
Use the screen utility to keep the bot running after disconnecting from SSH.

# Install screen (if needed)
$ sudo apt install screen -y

# Start a new screen session and launch the bot
$screen -S ignitos_session$ python3 main.py

To Detach: Press Ctrl + A then D. You can now safely log out.

📚 Bot Command Reference
Commands are categorized by their prefix: User Bot commands (.) are sent from your account, and Control Bot commands (/) are sent to the BotFather bot instance.

Function

User Bot Command (Self)

Control Bot Command (BotFather)

Example Usage

AI Question

.ai [prompt]

/ai [prompt]

.ai What is the capital of Canada?

Image Generation

.img [prompt]

/img [prompt]

.img A hyperrealistic neon tiger.

Check Latency

.ping

-

.ping

Enable Auto-Reply

.away

-

.away

Disable Auto-Reply

.online

-

.online

Set Offline Message

.editoff [new message]

-

.editoff I am busy coding.

💻 Console Management Commands
Action

Command

Notes

Re-attach to the console

screen -r ignitos_session

See the bot's live logs and output.

Stop the bot entirely

Re-attach, then press Ctrl + C

Stops the Python script inside the screen.

List all active sessions

screen -ls

Shows all detached sessions.

