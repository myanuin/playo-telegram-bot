from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

async def send_welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_members = update.message.new_chat_members
    for member in new_members:
        name = member.full_name

        message = (
            f"👋 Welcome, *{name}*!\n\n"
            "📌 *Group Rules:*\n"
            "1. Be respectful 🌟\n"
            "2. Only football-related content ⚽\n"
            "3. No spam or self-promotion 🚫\n\n"
            "➖➖➖\n"
            "🛠️ _This bot runs on free cloud magic, powered by coffee & goodwill. If it glitches, please wink and reload._\n\n"
            "☕ _Like it? Say thanks with a [coffee](https://buymeacoffee.com/talkanoop88)!_ 🙌"
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
