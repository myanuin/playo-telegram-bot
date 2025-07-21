import os
import logging
from dotenv import load_dotenv
from telegram import Bot
from bot.finder import fetch_football_games
from bot.telegram_helpers import format_games_for_telegram

# Load environment variables (.env or set in deployment)
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
LAT = float(os.getenv("LAT", "12.935207"))
LNG = float(os.getenv("LNG", "77.710709"))
RADIUS = int(os.getenv("RADIUS", 50))
SPORT = os.getenv("SPORT", "SP2")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("📡 Running daily Playo update job...")

    # Prepare config for fetcher
    config = {
        "lat": LAT,
        "lng": LNG,
        "radius": RADIUS,
        "sport": SPORT,
        "timezone": TIMEZONE,
    }

    try:
        games = fetch_football_games(config)
        message = format_games_for_telegram(games)

        if not message.strip():
            message = "⚽ No relevant football games found between 6PM and 10PM today!"

        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode="Markdown"
        )
        logger.info("✅ Daily game update sent successfully.")
    except Exception as e:
        logger.error(f"❌ Error sending daily update: {e}", exc_info=True)

if __name__ == "__main__":
    main()
