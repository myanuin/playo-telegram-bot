import os
import pytz
import datetime
from datetime import timedelta, time as dtime
from dotenv import load_dotenv

from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters
)

from bot.finder import fetch_football_games
from bot.telegram_helpers import (
    send_welcome_message,
    format_games_for_telegram
)

# Load environment variables from .env
load_dotenv()

# Load variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CONFIG = {
    "lat": float(os.getenv("LAT", 12.935207)),
    "lng": float(os.getenv("LNG", 77.710709)),
    "radius": int(os.getenv("RADIUS", 50)),
    "sport": os.getenv("SPORT", "SP2"),
    "timezone": os.getenv("TIMEZONE", "Asia/Kolkata"),
}

# ----------------------------
# Function: Fetch & send Playo data
# ----------------------------
async def daily_playo_update(context: ContextTypes.DEFAULT_TYPE):
    print("📡 Running daily Playo update...")
    games = fetch_football_games(CONFIG)
    print(f"🎯 Fetched {len(games)} games")

    message = format_games_for_telegram(games)
    if not message.strip():
        message = "⚽ No football games found today between 6PM and 10PM."

    await context.bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=message,
        parse_mode="Markdown"
    )
    print("✅ Game update sent to Telegram group.")

# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    print("🚀 Starting Telegram Bot...")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Handle new member join
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, send_welcome_message))

    # Get IST time and current now
    ist = pytz.timezone(CONFIG["timezone"])
    now = datetime.datetime.now(ist)
    print("🕒 Current time:", now.strftime("%A, %B %d, %Y, %I:%M %p %Z"))

    # Schedule daily job at 5:30 PM IST
    send_time = dtime(17, 30, tzinfo=ist)
    app.job_queue.run_daily(daily_playo_update, send_time)
    print("📅 Scheduled job for 5:30 PM IST daily.")

    # Test: Run once after 5 seconds (instant test!)
    app.job_queue.run_once(daily_playo_update, when=timedelta(seconds=5))
    print("🧪 Test job scheduled to run in 5 seconds.")

    print("🤖 Bot is running... Waiting for events.")
    app.run_polling()
