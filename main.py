import os
import logging
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from bot.telegram_helpers import send_welcome_message
from daily_task import run_daily_update

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_TOKEN = os.getenv("WEBHOOK_SECRET_TOKEN", "some-secret")
CRON_SECRET = os.getenv("CRON_SECRET", "cron-secret")  # <- for /update-playo endpoint
RENDER_WEB_URL = os.getenv("RENDER_WEB_URL")
WEBHOOK_PATH = f"/{WEBHOOK_TOKEN}"
WEBHOOK_URL = f"{RENDER_WEB_URL}{WEBHOOK_PATH}"

# ----------------------------
# Logging Configuration
# ----------------------------
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ----------------------------
# Commands
# ----------------------------
async def handle_test(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is alive and working!")

# ----------------------------
# Webhook Setup
# ----------------------------
if __name__ == "__main__":
    logger.info("🚀 Booting Telegram bot webhook server...")

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("test", handle_test))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, send_welcome_message))

    # Add /update-playo route (exposed webhook for cron ping)
    async def update_playo_handler(request):
        from aiohttp import web
        logger.info("📥 /update-playo endpoint triggered.")

        if request.headers.get("X-CRON-TOKEN") != CRON_SECRET:
            logger.warning("🔒 Invalid cron token - access denied.")
            return web.Response(status=403, text="Forbidden - Invalid Token")

        try:
            await run_daily_update()
            return web.Response(text="✅ Update sent!")
        except Exception as e:
            logger.error(f"❌ Error sending Playo update: {e}", exc_info=True)
            return web.Response(status=500, text="Update failed.")

    # Register the route before starting webhook server
    application.web_app.router.add_post("/update-playo", update_playo_handler)

    # Start webhook application
    logger.info(f"🌐 Starting webhook on port 10000 → {WEBHOOK_URL}")
    application.run_webhook(
        listen="0.0.0.0",
        port=10000,
        url_path=WEBHOOK_TOKEN,
        webhook_url=WEBHOOK_URL,
    )
