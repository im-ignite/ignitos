Deployment Guide: Ignitos Telegram Auto-Reply Bot
This guide provides the necessary steps to deploy your Telegram self-bot and its plugins on a Linux-based Virtual Private Server (VPS) for 24/7 operation.

Prerequisites
Before starting, ensure you have the following:

A VPS Running Linux (e.g., Ubuntu, Debian, CentOS).

SSH Access to your VPS.

Your Bot Code (including main.py, config.json if it exists, the plugins folder, and requirements.txt).

Your Credentials:

Telegram API ID and API Hash (from my.telegram.org).

BotFather Bot Token (for the control bot).

Gemini API Key (for the .ai and .img commands).

Step 1: Prepare the VPS Environment
Log in to your VPS via SSH and run these commands to install required tools and Python dependencies.

1.1 Update System Packages and Install Python
# Update package list
sudo apt update

# Install Python 3 and pip (or use 'yum install' on CentOS/RHEL)
sudo apt install python3 python3-pip -y

1.2 Install a Virtual Environment
It's best practice to use a virtual environment to manage dependencies.

# Install the venv module
sudo apt install python3-venv -y

# Create a new directory for your project
mkdir ignitos_bot
cd ignitos_bot

# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

Step 2: Transfer and Install Code
2.1 Transfer Code to VPS
Use tools like scp, sftp, or Git to move your project files (main.py, plugins/, requirements.txt, etc.) into the ignitos_bot directory on your VPS.

If you are using Git, run these commands inside the ignitos_bot directory:

# Install git if you haven't already
sudo apt install git -y

# Clone your repository (replace with your actual URL)
git clone [https://github.com/im-ignite/ignitos.git](https://github.com/im-ignite/ignitos.git) .

2.2 Install Python Dependencies
Make sure your virtual environment is still active ((venv) should be visible in your prompt).

# Install the required Python libraries (pyrogram, requests, Pillow)
pip install -r requirements.txt

Step 3: Run the Bot for Initial Setup
The bot needs to run interactively once to create the user session file (user_bot_session.session) and save your API keys.

Run the main script:

python3 main.py

Follow the Prompts: The script will guide you through entering your:

BotFather Bot Token.

Telegram API ID and API Hash.

Phone number, OTP, and 2FA password (for the user session).

Gemini API Key.

The script will exit automatically after successfully saving all configuration details.

Check for Files: Verify that config.json and the .session file have been created in your project directory.

Step 4: Run the Bot Continuously using screen
The screen utility is perfect for running applications in the background, even after you disconnect from SSH.

4.1 Install screen
sudo apt install screen -y

4.2 Start the Bot in a New Screen Session
Activate the virtual environment (if not already active):

source venv/bin/activate

Start a new screen session and run the bot:

screen -S ignitos_session
python3 main.py

The bot is now running inside the virtual session.

4.3 Detach and Exit
To detach from the screen session (leaving the bot running), press:
Ctrl + A then D

You can now safely log out of your SSH session. The bot will continue running.

Management Commands
Action

Command

Notes

Re-attach to the running bot

screen -r ignitos_session

See the bot's console output.

Detach from the session

Ctrl + A then D

Leaves the bot running in the background.

Stop the bot entirely

screen -r ignitos_session and press Ctrl + C

You must be attached to the session to stop it.

List all running screen sessions

screen -ls



