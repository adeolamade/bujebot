
import logging
from datetime import datetime

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

from config import BOT_TOKEN, OWNER_TELEGRAM_ID
from keywords import KEYWORDS
from utils import find_matches
from translator import translate_text

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Monitoring bot is active.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text:
        return
    text = msg.text
    matches = find_matches(text, KEYWORDS)
    if not matches:
        return

    user = msg.from_user
    chat = msg.chat

    sender = f"@{user.username}" if user and user.username else (user.full_name if user else "Unknown")
    group_name = chat.title if chat else "Unknown Group"
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    translated = await translate_text(text)

    alert = f"🚨 Keyword Alert\n\n👤 {sender}\n👥 {group_name}\n⏰ {timestamp}\n\n{text}\n\n{translated}\n\nMatched: {', '.join(matches)}"

    await context.bot.send_message(chat_id=OWNER_TELEGRAM_ID, text=alert)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
