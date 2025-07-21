import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

# ----------------------------------------
# 👋 WELCOME MESSAGE HANDLER
# ----------------------------------------

async def send_welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_members = getattr(update.message, "new_chat_members", [])
    chat_id = update.effective_chat.id if update.effective_chat else None

    for member in new_members:
        # Fallback to a generic name if user info is missing or incomplete
        name = getattr(member, "full_name", "") or getattr(member, "name", "") or "friend"

        welcome_text = (
            f"👋 Welcome, *{name}*!\n\n"
            "📌 *Group Rules:*\n"
            "1. Be respectful 🌟\n"
            "2. Only football-related content ⚽\n"
            "3. No spam or self-promotion 🚫\n\n"
            "➖➖➖\n"
            "🤖 This bot runs on free cloud ☁️\n"
            "😴 If no matches show up, it’s not the bot’s fault — Playo’s just quiet.\n"
            
        )

        try:
            logger.info(f"➡️ Sending welcome message to '{name}' in chat {chat_id}...")
            sent = await context.bot.send_message(
                chat_id=chat_id,
                text=welcome_text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            logger.info(f"✅ Welcome message sent to '{name}' (message_id={sent.message_id})")
        except Exception as e:
            logger.error(f"❌ Failed to send welcome to '{name}': {e}", exc_info=True)
            try:
                fallback = f"👋 Welcome, *{name}*! Please check the group rules above 😊"
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=fallback,
                    parse_mode=ParseMode.MARKDOWN
                )
                logger.info(f"🔁 Sent fallback welcome to '{name}'.")
            except Exception as fallback_e:
                logger.error(f"❌ Failed to send fallback welcome to '{name}': {fallback_e}", exc_info=True)

# ----------------------------------------
# ⚽ PLAYO MATCH FORMATTER
# ----------------------------------------

def format_games_for_telegram(games: list) -> str:
    if not games:
        return "😴 No football matches found today between 6PM and 10PM!"

    messages = []

    for i, game in enumerate(games, start=1):
        venue = game.get("venue", "").strip()
        start = game.get("start", "").strip()
        end = game.get("end", "").strip()
        players = game.get("players", "0/0").strip()
        host = game.get("host", "Unknown").strip()
        link = game.get("link", "").strip()
        distance = game.get("distance", None)

        # Skip full games
        try:
            current, total = map(int, players.split("/"))
            if total <= 0 or current >= total:
                continue
        except Exception:
            continue

        lines = []

        # Match title with numbering and optional venue
        if venue:
            lines.append(f"{i}. 🏟️ *{venue}*")
        else:
            lines.append(f"{i}.")

        # Add start–end time
        if start and end:
            lines.append(f"🕔 {start} – {end}")

        # Players
        lines.append(f"👥 {players}")

        # Host
        if host:
            lines.append(f"👤 Host: {host}")

        # Distance
        if distance:
            lines.append(f"📍 {round(distance, 1)} km away")

        # Link
        if link:
            lines.append(f"[👉 Join Match]({link})")

        match_block = "\n".join(lines)
        messages.append(match_block)

    if not messages:
        return "😔 No open football matches found today between 6PM and 10PM."

    return "\n\n".join(messages)
