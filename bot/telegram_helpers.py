from telegram import Bot, Update
from telegram.constants import ParseMode

async def send_telegram_message(message, token, chat_id):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN)

def format_games_for_telegram(games):
    if not games:
        return "⚽ No football games found today between 6PM - 10PM."

    message = "*Available Football Matches:*\n\n"
    for i, g in enumerate(games, 1):
        message += f"*{i}) {g['venue']}*\n"
        message += f"🕐 {g['start']} - {g['end']}\n"
        message += f"👥 {g['players']}, 👤 {g['host']}\n"
        message += f"📍 {g['distance']} km away\n"
        message += f"🔗 [Join]({g['link']})\n\n"
    return message

async def send_welcome_message(update: Update, context):
    new_members = update.message.new_chat_members
    for member in new_members:
        name = member.full_name
        rules = (
            f"👋 Welcome, *{name}*!\n\n"
            "📌 *Group Rules:*\n"
            "1. Be respectful 🌟\n"
            "2. Only football-related content ⚽\n"
            "3. No spam or self-promotion 🚫\n"
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=rules, parse_mode=ParseMode.MARKDOWN)
