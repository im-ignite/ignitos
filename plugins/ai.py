# This plugin integrates the Gemini API for AI responses in the user bot and control bot.

from pyrogram import Client, filters
from pyrogram.types import Message
import json
import requests
import asyncio
import time

# --- Gemini API Constants ---
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"
SESSION_NAME = 'user_bot_session' # Defined here to distinguish the user client

def call_gemini_api(api_key: str, prompt: str, use_search: bool = True):
    """
    Calls the Gemini API to generate content with optional Google Search grounding.
    Returns the generated text and a list of sources.
    """
    headers = { 'Content-Type': 'application/json' }
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": "You are a helpful and concise AI assistant."}]}
    }

    if use_search:
        payload["tools"] = [{"google_search": {}}]

    # Append API key to the URL
    full_api_url = f"{API_URL}?key={api_key}"

    try:
        # Implementing exponential backoff for resilience (max 3 retries)
        for attempt in range(3):
            try:
                # Using synchronous requests for simplicity here, as requests.post is blocking
                response = requests.post(full_api_url, headers=headers, data=json.dumps(payload))
                response.raise_for_status() # Raise exception for bad status codes
                
                result = response.json()
                candidate = result.get('candidates', [{}])[0]
                text = candidate.get('content', {}).get('parts', [{}])[0].get('text', "Error: AI response text missing.")

                sources = []
                grounding_metadata = candidate.get('groundingMetadata', {})
                if grounding_metadata and grounding_metadata.get('groundingAttributions'):
                    sources = [
                        f"[{i+1}]({attr.get('web', {}).get('uri')})"
                        for i, attr in enumerate(grounding_metadata['groundingAttributions'])
                        if attr.get('web', {}).get('uri')
                    ]
                
                return text, sources
            except requests.exceptions.HTTPError as e:
                if 429 <= e.response.status_code < 500 and attempt < 2:
                    # Retry on rate limit errors
                    time.sleep(2 ** attempt) 
                    continue
                raise # Re-raise other HTTP errors
        
        return "AI API Error: Maximum retries reached due to rate limiting.", []

    except requests.exceptions.RequestException as e:
        return f"AI API Error: Failed to connect or received a bad response. Details: {e}", []
    except Exception as e:
        return f"AI Processing Error: {e}", []


async def ai_handler(client: Client, message: Message, config: dict, is_user_bot: bool):
    """Generic handler for both .ai and /ai commands."""
    api_key = config.get('gemini_api_key')
    
    if not api_key:
        # Check if the message is from the owner in private chat to provide instruction
        if is_user_bot and message.chat.type == filters.private and (await client.get_me()).id == message.from_user.id:
            await message.reply_text("❌ Error: Gemini API Key is missing in the configuration. Please restart the script and enter your key when prompted.")
        return

    try:
        # Extract the prompt text after the command
        command_text = message.text.split(None, 1)
        if len(command_text) < 2:
            await message.reply_text("Please provide a prompt after the command.\nExample: `.ai What is the capital of France?`")
            return
        
        prompt = command_text[1].strip()
        
        # Send initial message (placeholder)
        thinking_msg = await message.reply_text("🤖 Thinking...", quote=True)
        
        # Call the API using a thread pool executor to avoid blocking the event loop
        text, sources = await client.loop.run_in_executor(
            None, # Default executor
            lambda: call_gemini_api(api_key, prompt, use_search=True)
        )
        
        response_text = text
        if sources:
            response_text += "\n\n**Sources:** " + " ".join(sources)

        await thinking_msg.edit_text(response_text, disable_web_page_preview=True)

    except Exception as e:
        await thinking_msg.edit_text(f"An unexpected error occurred: {e}")
        print(f"AI Command Error: {e}")


def setup(app: Client, config: dict, is_control_bot: bool = False):
    """Registers the AI command handlers for the client."""
    
    if not is_control_bot:
        # 1. User Bot Command (.ai)
        @app.on_message(filters.command("ai", prefixes=".") & filters.me)
        async def user_bot_ai_command(client, message: Message):
            # is_user_bot is True
            await ai_handler(client, message, config, is_user_bot=True)
            
    else:
        # 2. Control Bot Command (/ai)
        # This branch runs if the app is a bot client (the control bot)
        @app.on_message(filters.command("ai") & filters.private)
        async def control_bot_ai_command(client, message: Message):
            # This handler is restricted to private chats to prevent group spam.
            # is_user_bot is False
            await ai_handler(client, message, config, is_user_bot=False)