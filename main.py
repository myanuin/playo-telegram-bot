import os
import logging
import datetime
import pytz
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)
from dotenv import load_dotenv

from bot.finder import fetch_football_games
from bot.telegram_helpers import send_welcome_message, format_games_for_telegram

# ----------------------------
# ENV Setup
# ----------------------------
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")
LAT = float(os.getenv("LAT", "12.935207"))
LNG = float(os.getenv("LNG", "77.710709"))
RADIUS = int(os.getenv("RADIUS", 50))
SPORT = os.getenv("SPORT", "SP2")

CONFIG = {
    "lat": LAT,
    "lng": LNG,
    "radius": RADIUS,
    "sport": SPORT,
    "timezone": TIMEZONE,
}

# ----------------------------
# Logging Setup for Render Logs
# ----------------------------
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ----------------------------
# Handlers
# ----------------------------

async def daily_playo_update(context: ContextTypes.DEFAULT_TYPE):
    logger.info("📡 Running daily Playo update job...")
    try:
        games = fetch_football_games(CONFIG)
        message = format_games_for_telegram(games)

        if not message.strip():
            message = "⚽ No football games found today between 6PM and 10PM."

        await context.bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode="Markdown",
        )
        logger.info("✅ Daily message sent successfully.")

    except Exception as e:
        logger.error(f"❌ Error during daily update: {e}", exc_info=True)


async def test_command(update, context):
    await update.message.reply_text("✅ Bot is alive and ready!")

# ----------------------------
# Main App
# ----------------------------
if __name__ == "__main__":
    logger.info("🚀 Starting Telegram Bot...")

    try:
        app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

        # 1. Handle new users
        app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, send_welcome_message))

        # 2. Optional test command
        app.add_handler(CommandHandler("test", test_command))

        # 3. Setup daily job
        from datetime import time as dtime, timedelta

        ist = pytz.timezone(TIMEZONE)
        send_time = dtime(17, 30, tzinfo=ist)
        now = datetime.datetime.now(ist)
        logger.info("🕒 Current time: %s", now.strftime("%A, %B %d, %Y, %I:%M %p %Z"))
        logger.info("📅 Scheduling job for 5:30 PM IST daily...")
        app.job_queue.run_daily(daily_playo_update, send_time)

        # 4. Test trigger within 10 seconds
        app.job_queue.run_once(daily_playo_update, when=timedelta(seconds=10))
        logger.info("🧪 One-time test message will send in 10 seconds.")

        # 5. Start polling
        logger.info("🤖 Bot is now polling...")
        app.run_polling()

    except Exception as e:
        logger.critical("😵 FATAL ERROR: Bot crashed on startup!", exc_info=True)
