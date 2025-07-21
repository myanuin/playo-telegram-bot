from flask import Flask, request, jsonify
import os
import logging
import telegram
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters
)
from bot.telegram_helpers import send_welcome_message
from dotenv import load_dotenv

# Load env vars
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_SECRET_TOKEN = os.getenv("WEBHOOK_SECRET_TOKEN", "topsecret")
BOT = telegram.Bot(token=BOT_TOKEN)

app = Flask(__name__)
application = None  # Will be initialized when the script starts

# Logging for Render logs
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ----------------------------
# Routes
# ----------------------------

@app.route("/", methods=["GET"])
def home():
    return "👋 Bot is running with Flask + Webhooks on Render!"

@app.route("/healthz", methods=["GET"])
def health_check():
    return jsonify(status="ok", message="Webhook bot running 🎉"), 200

@app.route(f"/{WEBHOOK_SECRET_TOKEN}", methods=["POST"])
async def telegram_webhook():
    update = telegram.Update.de_json(request.get_json(force=True), BOT)
    await application.initialize()  # Ensure handlers/context/etc are set up
    await application.process_update(update)
    return "OK", 200

# ----------------------------
# Start the bot app
# ----------------------------
if __name__ == "__main__":
    logger.info("🚀 Starting Flask + Telegram bot webhook app...")

    # Create Application instance for Telegram
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, send_welcome_message))
    application.add_handler(CommandHandler("test", lambda update, ctx: update.message.reply_text("✅ Bot is alive using webhook!")))

    logger.info("✅ Flask app is booted and ready for Telegram webhooks!")
    app.run(host="0.0.0.0", port=10000)  # Render auto-detects this port
