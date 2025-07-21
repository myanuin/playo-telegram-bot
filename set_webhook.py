import os
import telegram
import asyncio
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_SECRET_TOKEN = os.getenv("WEBHOOK_SECRET_TOKEN", "topsecret")
RENDER_WEB_URL = os.getenv("RENDER_WEB_URL")
bot = telegram.Bot(token=BOT_TOKEN)
webhook_url = f"{RENDER_WEB_URL}/{WEBHOOK_SECRET_TOKEN}"

async def main():
    print(f"📡 Setting webhook: {webhook_url}")
    await bot.set_webhook(url=webhook_url)
    print("✅ Done.")

if __name__ == "__main__":
    asyncio.run(main())
