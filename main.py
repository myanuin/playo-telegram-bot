import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from dotenv import load_dotenv
from bot.telegram_helpers import send_welcome_message

# ----------------------------
# Environment setup
# ----------------------------
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_SECRET_TOKEN = os.getenv("WEBHOOK_SECRET_TOKEN", "supersecret")
RENDER_WEB_URL = os.getenv("RENDER_WEB_URL")  # e.g., https://your-app.onrender.com

WEBHOOK_PATH = f"/{WEBHOOK_SECRET_TOKEN}"
WEBHOOK_URL = f"{RENDER_WEB_URL}{WEBHOOK_PATH}"

# ----------------------------
# Handlers
# ----------------------------
async def handle_test(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is alive using webhook!")

# ----------------------------
# Build Application
# ----------------------------
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Register bot handlers
application.add_handler(CommandHandler("test", handle_test))
application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, send_welcome_message))


# ----------------------------
# Run webhook server (PTB built-in)
# ----------------------------
if __name__ == "__main__":
    print("🚀 Starting PTB webhook bot on port 10000...")

    application.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=WEBHOOK_URL,
        url_path=WEBHOOK_SECRET_TOKEN   # ✅ Correct for PTB 21.1
    )
