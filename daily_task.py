import os
import logging
from dotenv import load_dotenv
from bot.finder import fetch_football_games
from bot.telegram_helpers import format_games_for_telegram
from telegram import Bot

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def send_daily_playo():
    logging.info("📡 Running daily Playo update job...")
    config = {
        "lat": float(os.getenv("LAT")),
        "lng": float(os.getenv("LNG")),
        "radius": int(os.getenv("RADIUS")),
        "sport": os.getenv("SPORT"),
        "timezone": os.getenv("TIMEZONE")
    }

    try:
        games = fetch_football_games(config)
        message = format_games_for_telegram(games)

        if not message:
            message = "⚽ No games found today!"

        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="Markdown")
        logging.info("✅ Message sent.")
    except Exception as e:
        logger.error(f"❌ Error sending daily update: {e}", exc_info=True)

if __name__ == "__main__":
    send_daily_playo()
