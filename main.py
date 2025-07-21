from flask import Flask, request
import os
import logging
import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot.telegram_helpers import send_welcome_message
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_SECRET_TOKEN = os.getenv("WEBHOOK_SECRET_TOKEN", "topsecret")
BOT = telegram.Bot(token=BOT_TOKEN)

app = Flask(__name__)
application = None  # will be set after creation

# Logging for Render logs tab
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


@app.route(f"/{WEBHOOK_SECRET_TOKEN}", methods=["POST"])
async def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), BOT)
    await application.initialize()
    await application.process_update(update)
    return "OK!", 200


if __name__ == "__main__":
    from telegram.ext import ApplicationBuilder

    logger.info("🚀 Starting Flask + Telegram bot webhook")

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, send_welcome_message))
    application.add_handler(CommandHandler("test", lambda update, ctx: update.message.reply_text("✅ Bot is alive using webhook!")))

    # Don’t start polling here — Telegram will POST via webhook
    logger.info("✅ Flask app is booted and ready for Telegram webhooks!")
    app.run(host="0.0.0.0", port=10000)  # Render auto-detects on exposed port
