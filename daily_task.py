import os
import logging
from telegram import Bot
from bot.finder import fetch_football_games
from bot.telegram_helpers import format_games_for_telegram

logger = logging.getLogger(__name__)

async def run_daily_update():
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    LAT = float(os.getenv("LAT", "12.935207"))
    LNG = float(os.getenv("LNG", "77.710709"))
    RADIUS = int(os.getenv("RADIUS", 50))
    SPORT = os.getenv("SPORT", "SP2")
    TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")

    config = {
        "lat": LAT,
        "lng": LNG,
        "radius": RADIUS,
        "sport": SPORT,
        "timezone": TIMEZONE,
    }

    games = fetch_football_games(config)
    message = format_games_for_telegram(games)
    if not message.strip():
        message = "😴 No open football matches found today between 6PM and 10PM."

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=message,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    logger.info("✅ Playo game update sent successfully.")
