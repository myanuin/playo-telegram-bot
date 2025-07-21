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

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_PATH = os.getenv("WEBHOOK_SECRET_TOKEN", "supersecret")
RENDER_WEB_URL = os.getenv("RENDER_WEB_URL")
WEBHOOK_URL = f"{RENDER_WEB_URL}/{WEBHOOK_PATH}"


# Define a simple /test command
async def handle_test(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is alive using webhook!")


# Build the Application
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Register handlers
application.add_handler(CommandHandler("test", handle_test))
application.add_handler(
    MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, send_welcome_message)
)

# Run the built-in webhook server (PTB handles everything)
if __name__ == "__main__":
    print("🚀 Starting PTB webhook bot on port 10000...")
    application.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=WEBHOOK_URL,
        webhook_path=f"/{WEBHOOK_PATH}",
    )
