🚀 Ignitos Telegram Auto-Reply Bot Deployment Guide
This guide will help you deploy and run your modular Telegram self-bot and its integrated control bot on a Linux-based Virtual Private Server (VPS) for continuous 24/7 operation.

✨ Features at a Glance
Command Type

Prefix

Description

Powered By

User Bot

.

Commands you send, visible only to you (.ping, .ai, .img).

Pyrogram

Control Bot

/

Commands sent to the separate BotFather bot for remote control (/ai, /img).

Pyrogram

Auto-Reply

Core

Automatically replies to private messages when set to /away.

Main Logic

⚙️ Prerequisites
Ensure you have the following information and access before starting the deployment:

A Linux VPS: Running Ubuntu, Debian, or CentOS.

SSH Access: To connect to your server.

Bot Code: The full project directory, including main.py, the plugins folder, and requirements.txt.

Credentials:

Telegram API ID and API Hash (from my.telegram.org).

BotFather Bot Token (for the remote control bot).

Gemini API Key (for the AI and Image generation features).

Step 1: Prepare the VPS Environment
Log in to your VPS via SSH to set up the necessary environment.

1.1 Update System Packages and Install Python
Use the appropriate package manager (apt for Debian/Ubuntu or yum for CentOS/RHEL).

# Update package list
sudo apt update

# Install Python 3, pip, and git
sudo apt install python3 python3-pip git -y

1.2 Install and Activate a Virtual Environment
It is highly recommended to use a Python virtual environment (venv) for dependency isolation.

# Install the venv module
sudo apt install python3-venv -y

# Create a project directory and navigate into it
mkdir ignitos_bot
cd ignitos_bot

# Create and activate the virtual environment
python3 -m venv venv
source venv/bin/activate

Step 2: Transfer Code and Install Dependencies
2.1 Transfer Code to VPS via Git
Run these commands inside the active ignitos_bot directory:

# Clone your repository (REPLACE with your actual GitHub URL)
git clone [https://github.com/im-ignite/ignitos.git](https://github.com/im-ignite/ignitos.git) .

# OR: Use scp/sftp to transfer files manually
# scp -r /local/path/to/bot user@vps_ip:/home/user/ignitos_bot

2.2 Install Python Dependencies
Make sure the virtual environment is still active ((venv) should be visible in your prompt).

# Install all required Python libraries (pyrogram, requests, Pillow, etc.)
pip install -r requirements.txt

Step 3: Run the Bot for Initial Setup
The bot must run interactively once to create the necessary session file and save your credentials securely.

Run the main script:

python3 main.py

Follow the Interactive Prompts:

The script will first ask for your BotFather Token.

It will then prompt for your Telegram API ID and API Hash.

Next, it will guide you through the Pyrogram login process (Phone Number, OTP, and 2FA password) to create the user_bot_session.session file.

Finally, it will ask for your Gemini API Key.

The script will exit gracefully once all configuration steps are complete.

Verify Configuration: Ensure the config.json and the .session file have been successfully created in the ignitos_bot directory.

Step 4: Run the Bot Continuously using screen
Use the screen utility to ensure the bot remains running even after you close your SSH connection.

4.1 Install screen (if not done in Step 1)
sudo apt install screen -y

4.2 Start the Bot in a New Screen Session
Re-activate the virtual environment (if you detached):

source venv/bin/activate

Start a new screen session and launch the bot:

screen -S ignitos_session
python3 main.py

The bot is now running inside the persistent screen session.

4.3 Detach and Exit
To detach from the screen session (leaving the bot running):

Press Ctrl + A then D

You can now safely log out of your SSH session.

🛠️ Bot Command Reference
Function

User Bot Command (Self-Command)

Control Bot Command (via BotFather)

Notes

Auto-Reply ON

.away

-

Enables auto-reply feature.

Auto-Reply OFF

.online

-

Disables auto-reply feature.

Edit Auto-Reply Message

.editoff [new message]

-

Updates the message sent when .away is active.

Check Latency

.ping

-

Returns the bot's reaction time in milliseconds.

AI Generation

.ai [prompt]

/ai [prompt]

Answers questions using the Gemini API with Google Search grounding.

Image Generation

.img [prompt]

/img [prompt]

Generates an image based on the prompt using the Imagen 3 API.

Management Commands (VPS Console)
Action

Command

Notes

Re-attach to the running bot

screen -r ignitos_session

See the bot's console output.

Stop the bot entirely

Re-attach, then press Ctrl + C

Stops the script inside the screen session.

List all running screen sessions

screen -ls

Shows all detached sessions.

