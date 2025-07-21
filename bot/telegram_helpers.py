import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

# ----------------------------------------
# 👋 WELCOME MESSAGE
# ----------------------------------------

async def send_welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_members = getattr(update.message, "new_chat_members", [])
    chat_id = update.effective_chat.id if update.effective_chat else None

    for member in new_members:
        name = getattr(member, "full_name", None) or getattr(member, "name", None) or "friend"

        welcome_text = (
            f"👋 Welcome, *{name}*!\n\n"
            "📌 *Group Rules:*\n"
            "1. Be respectful 🌟\n"
            "2. Only football-related content ⚽\n"
            "3. No spam or self-promotion 🚫\n\n"
            "➖➖➖\n"
            "🤖 This bot runs on free cloud ☁️\n"
            "😴 If no matches show up, it’s not the bot’s fault — Playo’s just quiet.\n"
            "☕ Want more consistency? [Buy me a coffee](https://buymeacoffee.com/talkanoop8y)!"
        )

        try:
            logger.info(f"➡️ Sending welcome to '{name}' (id={getattr(member, 'id', 'N/A')}) in chat {chat_id}.")
            sent = await context.bot.send_message(
                chat_id=chat_id,
                text=welcome_text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            logger.info(f"✅ Welcome sent to '{name}' (message_id={sent.message_id}).")
        except Exception as e:
            logger.error(f"❌ Failed to welcome '{name}' (id={getattr(member, 'id', 'N/A')}): {e}", exc_info=True)

            # Fallback to basic message
            try:
                fallback = (
                    f"❗ Sorry *{name}*, we had a hiccup while sending your welcome.\n"
                    "Have a look at the group rules above and enjoy your stay!"
                )
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=fallback,
                    parse_mode=ParseMode.MARKDOWN
                )
                logger.info(f"🔁 Fallback welcome sent to '{name}'.")
            except Exception as fallback_exc:
                logger.error(f"💥 Double-failure welcoming '{name}': {fallback_exc}", exc_info=True)

# ----------------------------------------
# ⚽ FORMAT PLAYO GAMES
# ----------------------------------------

def format_games_for_telegram(games: list) -> str:
    if not games:
        return "😴 No football matches found today between 6PM and 10PM!"

    messages = []

    for game in games:
        # Safe read with fallback
        venue = game.get("venue", "").strip() or "Unknown Venue"
        start = game.get("start", "Unknown")
        end = game.get("end", "Unknown")
        players = game.get("players", "0/0")
        host = game.get("host", "Unknown")
        link = game.get("link", "")
        distance = game.get("distance", None)

        # Only show games with available slots
        try:
            current, total = map(int, players.split("/"))
            if total <= 0 or current >= total:
                continue  # full or invalid match
        except Exception:
            continue  # invalid player format

        distance_str = f"📍 {round(distance, 1)} km away" if distance else ""

        match_text = (
            f"🏟️ *{venue}*\n"
            f"🕔 {start} – {end}\n"
            f"👥 {players} | 👤 {host} {distance_str}\n"
            f"[👉 Join Match]({link})"
        )

        messages.append(match_text)

    if not messages:
        return "😔 No open football matches found today between 6PM and 10PM."

    return "\n\n".join(messages)
