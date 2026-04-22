from flask import Flask
import threading
import asyncio

from src.app.main import main  # tera aiogram bot main()

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running ✅"

def run_bot():
    asyncio.run(main())

if __name__ == "__main__":
    # Bot thread
    threading.Thread(target=run_bot).start()

    # Flask server
    app.run(host="0.0.0.0", port=10000)
