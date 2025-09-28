# This is a sample plugin for the Telegram Auto-reply bot.

from pyrogram import Client, filters
from pyrogram.types import Message
import time

# You must have a setup function to register your handlers.
# It receives the Pyrogram Client object and the config dictionary.
def setup(app: Client, config: dict):
    
    @app.on_message(filters.command("ping", prefixes=".") & filters.me)
    async def ping_command(client, message: Message):
        """
        A simple ping command that replies with the bot's latency.
        """
        start_time = time.monotonic()
        
        # Use a new message to measure the latency for sending
        sent_message = await message.reply_text("Pinging...")
        
        # Calculate total time taken from when the command was processed until the message was sent
        latency = (time.monotonic() - start_time) * 1000 # Convert to milliseconds
        
        # Edit the message with the result
        await sent_message.edit_text(f"**Pong!** 🏓\nLatency: `{latency:.2f} ms`")

    # You can add more handlers here if needed.
    # @app.on_message(filters.command("hello") & filters.me)
    # async def hello_command(client, message: Message):
    #     await message.reply_text("Hello there!")