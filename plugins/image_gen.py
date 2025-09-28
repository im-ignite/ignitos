# This plugin integrates the Imagen 3 API (via Gemini API endpoint) for text-to-image generation.

from pyrogram import Client, filters
from pyrogram.types import Message
import json
import requests
import asyncio
import base64
from io import BytesIO
import time
from PIL import Image

# --- Imagen API Constants ---
# We use the 'predict' endpoint for Imagen 3.0
IMAGE_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict"
SESSION_NAME = 'user_bot_session' # Defined here to distinguish the user client

def call_imagen_api(api_key: str, prompt: str):
    """
    Calls the Imagen API to generate an image based on the prompt.
    Returns base64 image data and any error message.
    """
    headers = { 'Content-Type': 'application/json' }
    
    # Imagen API requires a different payload structure (using 'instances' and 'parameters')
    payload = {
        "instances": [
            {
                "prompt": prompt
            }
        ],
        "parameters": {
            "sampleCount": 1, # Requesting only 1 image
            "aspectRatio": "1:1", # Default to square image
            "personGeneration": "allow_adult", # Default safety setting
        }
    }

    # Append API key to the URL
    full_api_url = f"{IMAGE_API_URL}?key={api_key}"

    try:
        # Implementing exponential backoff for resilience (max 3 retries)
        for attempt in range(3):
            try:
                # Using synchronous requests for simplicity here
                response = requests.post(full_api_url, headers=headers, data=json.dumps(payload))
                response.raise_for_status() # Raise exception for bad status codes
                
                result = response.json()
                
                # Imagen API returns base64 image bytes in the predictions array
                predictions = result.get('predictions', [])
                if predictions and predictions[0].get('bytesBase64Encoded'):
                    base64_data = predictions[0]['bytesBase64Encoded']
                    return base64_data, None # Success
                
                # Handle cases where the prediction might be filtered or empty
                error_detail = result.get('error', {}).get('message', 'Unknown prediction error.')
                return None, f"Image generation failed: {error_detail}"

            except requests.exceptions.HTTPError as e:
                if 429 <= e.response.status_code < 500 and attempt < 2:
                    # Retry on rate limit errors
                    time.sleep(2 ** attempt) 
                    continue
                return None, f"API HTTP Error: {e}"
        
        return None, "API Error: Maximum retries reached due to rate limiting."

    except requests.exceptions.RequestException as e:
        return None, f"API Request Error: Failed to connect. Details: {e}"
    except Exception as e:
        return None, f"Image Processing Error: {e}"


async def image_handler(client: Client, message: Message, config: dict, is_user_bot: bool):
    """Generic handler for both .img and /img commands."""
    api_key = config.get('gemini_api_key')
    
    if not api_key:
        if is_user_bot and message.chat.type == filters.private and (await client.get_me()).id == message.from_user.id:
            await message.reply_text("❌ Error: Gemini API Key is missing in the configuration. Please restart the script and enter your key when prompted.")
        return

    try:
        # Extract the prompt text after the command
        command_text = message.text.split(None, 1)
        if len(command_text) < 2:
            await message.reply_text("Please provide a prompt after the command.\nExample: `.img A hyperrealistic cat in a spacesuit.`")
            return
        
        prompt = command_text[1].strip()
        
        # Send initial message (placeholder)
        thinking_msg = await message.reply_text("🎨 Generating image... This may take up to 20 seconds.", quote=True)
        
        # Call the API using a thread pool executor to avoid blocking the event loop
        base64_data, error = await client.loop.run_in_executor(
            None, # Default executor
            lambda: call_imagen_api(api_key, prompt)
        )
        
        if error:
            await thinking_msg.edit_text(f"❌ {error}")
            return

        # --- Process and Upload Image ---
        
        # 1. Decode base64 data to bytes
        image_bytes = base64.b64decode(base64_data)
        
        # 2. Create an in-memory file-like object
        photo_file = BytesIO(image_bytes)
        
        # 3. Use PIL to open the bytes and save it back to the buffer to ensure it's a valid Telegram photo (optional, but robust)
        # We need to explicitly name the file-like object for Pyrogram's send_photo
        photo_file.name = "generated_image.png"
        
        # 4. Send the photo
        await client.send_photo(
            chat_id=message.chat.id,
            photo=photo_file,
            caption=f"**Prompt:** `{prompt}`\n\nGenerated by Imagen 3",
            reply_to_message_id=message.id
        )

        # 5. Delete the thinking message to clean up the chat
        await thinking_msg.delete()

    except Exception as e:
        # Check if the thinking_msg exists before trying to edit/delete
        try:
            await thinking_msg.edit_text(f"An unexpected error occurred during image upload: {type(e).__name__}: {e}")
        except Exception:
            await message.reply_text(f"An unexpected error occurred: {type(e).__name__}: {e}")
        print(f"Image Command Fatal Error: {type(e).__name__}: {e}")


def setup(app: Client, config: dict, is_control_bot: bool = False):
    """Registers the image generation command handlers for the client."""
    
    if not is_control_bot:
        # 1. User Bot Command (.img)
        @app.on_message(filters.command("img", prefixes=".") & filters.me)
        async def user_bot_image_command(client, message: Message):
            await image_handler(client, message, config, is_user_bot=True)
            
    else:
        # 2. Control Bot Command (/img)
        # This handler will run for the BotFather bot
        @app.on_message(filters.command("img") & filters.private)
        async def control_bot_image_command(client, message: Message):
            await image_handler(client, message, config, is_user_bot=False)
