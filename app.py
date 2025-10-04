import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Ignitos Telegram Userbot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # Start your Telegram bot here.
    # Example (if your bot is started by main.py):
    # from main import start_bot
    # start_bot()
    app.run(host="0.0.0.0", port=port)