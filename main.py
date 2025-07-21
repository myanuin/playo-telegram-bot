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
# Logging setup for Render Logs
# ----------------------------
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ----------------------------
# Flask App init
# ----------------------------
app = Flask(__name__)
application: Application = ApplicationBuilder().token(BOT_TOKEN).build()

# Register handlers
application.add_handler(
    MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, send_welcome_message)
)

async def handle_test(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is alive using webhook!")

application.add_handler(CommandHandler("test", handle_test))

# Lazy-init flag 👇
_application_initialized = False

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
    global _application_initialized

    try:
        if not _application_initialized:
            await application.initialize()
            _application_initialized = True
            logger.info("✅ Application initialized on first request.")

        update = telegram.Update.de_json(request.get_json(force=True), BOT)
        await application.process_update(update)
        return "OK", 200

    except Exception as e:
        logger.error(f"❌ Error handling update: {e}", exc_info=True)
        return "Error", 500

# ----------------------------
# Start server
# ----------------------------
if __name__ == "__main__":
    logger.info("🚀 Starting Telegram Bot webhook server...")
    app.run(host="0.0.0.0", port=10000)
