import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
from bot.finder import fetch_football_games
from bot.telegram_helpers import send_telegram_message, format_games_for_telegram
import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "lat": float(os.getenv("LAT", "12.935207")),
    "lng": float(os.getenv("LNG", "77.710709")),
    "radius": int(os.getenv("RADIUS", "50")),
    "sport": os.getenv("SPORT", "SP2"),
    "timezone": os.getenv("TIMEZONE", "Asia/Kolkata"),
}

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def main():
    games = fetch_football_games(CONFIG)
    message = format_games_for_telegram(games)
    await send_telegram_message(message, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)

if __name__ == "__main__":
    asyncio.run(main())
