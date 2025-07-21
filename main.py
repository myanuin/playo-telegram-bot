from flask import Flask, request, jsonify
import os
import logging
import telegram
import asyncio
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv
from bot.telegram_helpers import send_welcome_message

# ----------------------------
# Environment setup
# ----------------------------
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_SECRET_TOKEN = os.getenv("WEBHOOK_SECRET_TOKEN", "supersecret")
BOT = telegram.Bot(token=BOT_TOKEN)

# ----------------------------
# Logging setup
# ----------------------------
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ----------------------------
# Create Flask app
# ----------------------------
app = Flask(__name__)
application: Application = None  # Will be initialized in __main__


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
    try:
        update = telegram.Update.de_json(request.get_json(force=True), BOT)
        await application.process_update(update)
        return "OK", 200
    except Exception as e:
        logger.error(f"❌ Error handling update: {e}", exc_info=True)
        return "Error", 500


# ----------------------------
# Start the bot service
# ----------------------------
if __name__ == "__main__":
    logger.info("🚀 Starting Flask + Telegram bot webhook app...")

    # Build Application with handlers
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # 🌟 Add handlers
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, send_welcome_message))
    application.add_handler(CommandHandler("test", lambda update, ctx: update.message.reply_text("✅ Bot is alive using webhook!")))

    # ✅ Initialize the app *one time only* (required for post-PTB v20)
    asyncio.run(application.initialize())

    logger.info("✅ Flask app is booted and ready for Telegram webhooks!")
    app.run(host="0.0.0.0", port=10000)  # Render allocates this port
