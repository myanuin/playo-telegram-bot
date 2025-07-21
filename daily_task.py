import os
import logging
from dotenv import load_dotenv
from telegram import Bot
from bot.finder import fetch_football_games
from bot.telegram_helpers import format_games_for_telegram
import asyncio

# Load .env
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
LAT = float(os.getenv("LAT", "12.935207"))
LNG = float(os.getenv("LNG", "77.710709"))
RADIUS = int(os.getenv("RADIUS", 50))
SPORT = os.getenv("SPORT", "SP2")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ MAKE ASYNC FUNCTION
async def main():
    logger.info("📡 Running daily Playo update job...")

    config = {
        "lat": LAT,
        "lng": LNG,
        "radius": RADIUS,
        "sport": SPORT,
        "timezone": TIMEZONE,
    }

    try:
        games = fetch_football_games(config)
        logger.info(f"GAMES: {games!r}")

        message = format_games_for_telegram(games)

        if not message.strip():
            message = "⚽ No football games found today between 6PM and 10PM."

        bot = Bot(token=TELEGRAM_BOT_TOKEN)

        # ✅ AWAIT async method here
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        logger.info("✅ Daily game update sent successfully.")
    except Exception as e:
        logger.error(f"❌ Error sending daily update: {e}", exc_info=True)

# ✅ Run async main
if __name__ == "__main__":
    asyncio.run(main())
