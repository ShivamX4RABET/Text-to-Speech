from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from config import BOT_TOKEN, ADMIN_IDS
from tts import text_to_speech
from database import init_db, can_convert, update_words

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send your script (Hindi/English/Hinglish) and I'll convert it to voice!")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()
    word_count = len(text.split())
    is_admin = user_id in ADMIN_IDS

    if not can_convert(user_id, word_count, is_admin):
        await update.message.reply_text("⚠️ Word limit exceeded. Please wait till next month or contact admin.")
        return

    await update.message.reply_text("🗣️ Generating audio... please wait.")
    file_path = text_to_speech(text)
    await update.message.reply_voice(voice=open(file_path, "rb"))
    update_words(user_id, word_count)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Optional: Implement monthly reset or reset for all
    pass

def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
