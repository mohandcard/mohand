import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext
)
from flask import Flask

# --- إعداد خادم ويب لإبقاء البوت نشطًا ---
server = Flask(__name__)

@server.route('/')
def ping():
    return "Bot is running!"

def keep_alive():
    import threading
    threading.Thread(target=lambda: server.run(host='0.0.0.0', port=8080)).start()

# --- إعداد البوت ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BANNED_WORDS = ["سب", "قذف", "إهانة"]  # الكلمات الممنوعة (يمكنك تعديلها)

async def alert_admins(update: Update, context: CallbackContext, word: str):
    chat = await update.effective_chat.get_administrators()
    for admin in chat:
        try:
            await context.bot.send_message(
                chat_id=admin.user.id,
                text=f"⚠️ تنبيه: كلمة ممنوعة\n\nالمستخدم: {update.message.from_user.mention_html()}\nالكلمة: {word}\nرابط الرسالة: {update.message.link}"
            )
        except Exception as e:
            logging.error(f"فشل في إرسال التنبيه: {e}")

async def handle_message(update: Update, context: CallbackContext):
    if update.message.chat.type in ["group", "supergroup"]:
        text = update.message.text.lower() if update.message.text else ""
        for word in BANNED_WORDS:
            if word in text:
                await alert_admins(update, context, word)
                break

def main():
    keep_alive()  # بدء خادم الويب
    
    token = os.getenv("TOKEN")
    if not token:
        logging.error("لم يتم تعيين TOKEN!")
        return

    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CommandHandler("start", lambda u,c: u.message.reply_text("✅ البوت يعمل!")))
    
    application.run_polling()

if __name__ == '__main__':
    main()
