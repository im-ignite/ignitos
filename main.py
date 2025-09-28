# This script creates a Telegram self-bot that replies when you're away.
# The initial setup and remote control are handled via a separate BotFather bot.

import os
import sys
import json
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import Message
import getpass # Using getpass to hide sensitive input
import importlib
import time # Needed for the ping plugin if loaded

# File path for the configuration file
CONFIG_FILE = 'config.json'
SESSION_NAME = 'user_bot_session'

# --- Custom Exception for Clean Exit ---
class SetupCompleteError(Exception):
    """Custom exception to signal that setup is complete and the script should exit."""
    pass

# --- Configuration & Setup Logic ---

def save_config(config_dict: dict):
    """Saves the provided configuration dictionary to the JSON file."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_dict, f, indent=4)
    print("Configuration saved successfully!")

def load_config():
    """Loads the configuration from the JSON file."""
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

# --- BotFather Bot for Initial Setup ---

async def setup_with_bot_father(bot_token, api_id, api_hash):
    """
    Guides the user through setting up the API credentials using a BotFather bot.
    """
    print("\nStarting the setup bot...")
    try:
        # Initialize the client with provided credentials
        setup_app = Client("setup_session", bot_token=bot_token, api_id=api_id, api_hash=api_hash)
    except Exception as e:
        print(f"Error: Could not initialize setup client. Please check your bot token, API ID, and API Hash. ({e})")
        sys.exit(1)

    setup_message = """
**Welcome to the Setup Wizard!**

I need your Telegram API credentials to run the auto-reply bot on your account.
1. Go to **[my.telegram.org](https://my.telegram.org)**.
2. Log in and click on "API Development Tools".
3. Create a new application to get your API ID and API Hash.

Once you have them, send me a message in the following format:
`API_ID API_HASH`
(e.g., `123456 0123456789abcdef0123456789abcdef`)
"""

    @setup_app.on_message(filters.command("start") & filters.private)
    async def start_handler(client, message: Message):
        await message.reply_text(setup_message, disable_web_page_preview=True)

    @setup_app.on_message(filters.private & ~filters.me)
    async def credential_handler(client, message: Message):
        try:
            if message.text.startswith('/'):
                # Ignore other commands
                return

            parts = message.text.split()
            if len(parts) != 2:
                await message.reply_text("Invalid format. Please send `API_ID API_HASH`.")
                return

            api_id_str, api_hash = parts
            api_id = int(api_id_str)

            # Validate credentials by trying to start a temporary client
            await message.reply_text("Credentials received. Validating...")
            test_client = Client("test_session", api_id=api_id, api_hash=api_hash)
            try:
                await test_client.start()
                await test_client.stop()
            except Exception as e:
                print(f"Test client failed with unknown error: {e}")
                await message.reply_text("Invalid API ID or API Hash. Please check them and try again.")
                return

            # Initial configuration dictionary
            initial_config = {
                'api_id': api_id,
                'api_hash': api_hash,
                'offline_message': "I am currently offline and will get back to you as soon as possible. Thank you!",
                'status': 'online',
                'session_string': None,
                'gemini_api_key': None,
                'bot_token': setup_app.bot_token # Save the bot token collected earlier
            }
            save_config(initial_config)
            
            await message.reply_text("Credentials saved successfully! The bot is now configured.")
            await message.reply_text("Please restart the main script to start your auto-reply bot.")
            
            # The script will now exit gracefully
            raise SetupCompleteError("Setup is complete. Exiting cleanly.")

        except ValueError:
            await message.reply_text("Invalid API ID. It must be a number.")
        except Exception as e:
            await message.reply_text(f"An error occurred: {e}")

    print("Please open your BotFather bot chat and send the /start command.")
    print("The setup bot is now waiting for your input...")

    async with setup_app:
        await setup_app.run()

# --- Main Auto-Reply Bot Logic ---

async def setup_user_session():
    """Performs the one-time user authentication and saves the session string."""
    print("Starting one-time user authentication...")
    
    config = load_config()
    if not config:
        print("Error: Configuration file not found. Cannot proceed with user authentication.")
        sys.exit(1)

    try:
        # Create a client to handle the interactive login
        user_client = Client(SESSION_NAME, api_id=config['api_id'], api_hash=config['api_hash'])

        async with user_client:
            # Let Pyrogram handle the interactive phone number login
            print("Successfully authenticated. Exporting session string...")
            session_string = await user_client.export_session_string()
            
            # Update and save the entire configuration dictionary
            config['session_string'] = session_string
            save_config(config)
            print("Session string exported and saved successfully!")
            
    except Exception as e:
        print(f"An error occurred during user authentication: {e}")
        sys.exit(1)

# Function to load plugins from the 'plugins' folder
def load_plugins(app: Client, config: dict, is_control_bot: bool):
    plugins_dir = "plugins"
    if os.path.exists(plugins_dir) and os.path.isdir(plugins_dir):
        sys.path.insert(0, plugins_dir)
        for filename in os.listdir(plugins_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                try:
                    module_name = filename[:-3]
                    module = importlib.import_module(module_name)
                    if hasattr(module, 'setup'):
                        # Pass all three required arguments
                        module.setup(app, config, is_control_bot=is_control_bot) 
                        print(f"Loaded plugin: {module_name}")
                    else:
                        print(f"Skipping plugin {module_name}: 'setup' function not found.")
                except Exception as e:
                    print(f"Failed to load plugin {filename}: {e}")
    else:
        print(f"No plugins directory found at '{plugins_dir}'.")
        print("Please create a 'plugins' folder to add new features.")

async def main():
    """Main function to run the auto-reply bot."""
    config = load_config()

    # --- Initial Configuration Check ---
    if not config:
        print("Bot is not yet configured. Please provide initial credentials.")
        bot_token = input("Enter your BotFather bot token: ")
        
        # New interactive prompt for API credentials
        print("\nNow, provide your Telegram API credentials. You can also press Enter to skip and set them up via the bot later.")
        api_id_str = input("Enter your API ID from my.telegram.org (or press Enter): ")
        api_hash = getpass.getpass("Enter your API Hash from my.telegram.org (or press Enter): ")
        
        if api_id_str and api_hash:
            # Terminal-based setup
            try:
                api_id = int(api_id_str)
                # Initial configuration dictionary for terminal setup
                initial_config = {
                    'api_id': api_id,
                    'api_hash': api_hash,
                    'offline_message': "I am currently offline and will get back to you as soon as possible. Thank you!",
                    'status': 'online',
                    'session_string': None,
                    'gemini_api_key': None,
                    'bot_token': bot_token # Save the bot token collected from the input
                }
                save_config(initial_config)
                print("Credentials saved. Please re-run the script to start the user session setup.")
                return
            except (ValueError, Exception) as e:
                print(f"Invalid API ID or Hash provided. Please check and try again. ({e})")
                sys.exit(1)
        else:
            # Bot-based setup
            try:
                # Dummy credentials for setup bot until user provides real ones
                await setup_with_bot_father(bot_token, api_id=0, api_hash='') 
            except SetupCompleteError:
                print("Setup process finished. Please re-run the script to start the main bot.")
                return

    # --- User Session Check ---
    if 'session_string' not in config or not config.get('session_string'):
        print("User session not found. Starting one-time user authentication process...")
        await setup_user_session()
        print("User session created. Please re-run the script to start the main bot.")
        return

    # --- Gemini API Key Check ---
    if 'gemini_api_key' not in config or not config.get('gemini_api_key'):
        print("\n--- GEMINI API KEY SETUP ---")
        api_key = getpass.getpass("Enter your Gemini API Key: ")
        if api_key:
            config['gemini_api_key'] = api_key
            save_config(config)
            # Reload config to ensure we have the latest version for the next step
            config = load_config()
            print("Gemini API Key saved. Restarting bot to apply changes...")
            # Exit to force a clean restart and re-run main()
            return
        else:
            print("Warning: Gemini API Key not provided. AI commands will be disabled.")


    # --- Create and run the main auto-reply client ---
    try:
        # Initialize the user bot client using the saved session string
        user_app = Client(SESSION_NAME, session_string=config['session_string'])

        # Initialize the BotFather client using the API key and bot token from config (if available)
        bot_app_token = config.get('bot_token')
        if bot_app_token:
             # The bot client runs alongside the user bot
             bot_app = Client("control_bot", 
                              bot_token=bot_app_token,
                              api_id=config['api_id'],
                              api_hash=config['api_hash'])
             print("Control Bot Client initialized.")
        else:
             bot_app = None
             print("Control Bot Token not found. Only user-bot commands (.commands) will work.")


        # Load plugins for both user_app and bot_app
        print("\nLoading plugins...")
        load_plugins(user_app, config, is_control_bot=False)
        if bot_app:
            load_plugins(bot_app, config, is_control_bot=True)
        
        # --- Core command handlers (only for the user bot) ---

        @user_app.on_message(filters.command("editoff") & filters.me)
        async def edit_offline_message(client, message: Message):
            """Handles the /editoff command to update the offline message."""
            try:
                new_message = message.text.split(" ", 1)[1].strip()
                config['offline_message'] = new_message
                save_config(config)
                await message.reply_text(f"Offline message updated successfully to: \n`{new_message}`")
            except IndexError:
                await message.reply_text("Please provide a new message after the /editoff command.\nExample: `/editoff I will reply later.`")
            except Exception as e:
                await message.reply_text(f"An error occurred: {e}")

        @user_app.on_message(filters.command("away") & filters.me)
        async def set_away_status(client, message: Message):
            config['status'] = 'offline'
            save_config(config)
            await message.reply_text("✅ Auto-reply is now **ON**. Send `/online` when you're back.")
            print("Auto-reply status set to OFF")

        @user_app.on_message(filters.command("online") & filters.me)
        async def set_online_status(client, message: Message):
            config['status'] = 'online'
            save_config(config)
            await message.reply_text("✅ Auto-reply is now **OFF**. Send `/away` to enable it.")
            print("Auto-reply status set to ON")
        
        @user_app.on_message(filters.private & filters.incoming & ~filters.me)
        async def auto_reply(client, message: Message):
            if config.get('status') == 'offline':
                try:
                    current_message = config.get('offline_message', "I am currently offline.")
                    await asyncio.sleep(3)
                    await message.reply(current_message)
                    print(f"Replied to {message.from_user.first_name} with: '{current_message}'")
                except Exception as e:
                    print(f"An error occurred during auto-reply: {e}")

        print("\nTelegram Auto-reply bot is running...")
        print("User Bot Client is connected.")
        if bot_app:
            print("Control Bot Client is connected.")
        print("Press Ctrl+C to stop the bot.")
        
        # Start both clients concurrently
        clients_to_run = [user_app]
        if bot_app:
            clients_to_run.append(bot_app)

        await asyncio.gather(*(client.start() for client in clients_to_run))
        await idle()
        await asyncio.gather(*(client.stop() for client in clients_to_run))


    except Exception as e:
        print(f"An error occurred while starting the main bot. Please check your configuration. ({e})")
        
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except SetupCompleteError:
        # Expected exception for clean exit after initial setup
        pass
    except RuntimeError as e:
        if "cannot await on itself" in str(e):
             # Ignore this common pyrogram shutdown error
             pass
        else:
            raise
