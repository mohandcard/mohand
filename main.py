from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram import Update
import logging

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# الكلمات الممنوعة
BANNED_WORDS = ["ارسيل", "واتساب"]

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('مرحبًا! أنا بوت إدارة المجموعات.')

async def check_message(update: Update, context: CallbackContext):
    if update.message.chat.type in ['group', 'supergroup']:
        text = update.message.text.lower() if update.message.text else ""
        found_words = [word for word in BANNED_WORDS if word.lower() in text]
        
        if found_words:
            admins = await update.effective_chat.get_administrators()
            for admin in admins:
                try:
                    await context.bot.send_message(
                        chat_id=admin.user.id,
                        text=f"⚠️ تنبيه: تم اكتشاف كلمة ممنوعة\n\nالمستخدم: {update.message.from_user.mention_html()}\nالكلمات: {', '.join(found_words)}"
                    )
                except Exception as e:
                    logger.error(f"فشل في إرسال التنبيه: {e}")

def main():
    # استبدل TOKEN بمتغير البيئة
    application = Application.builder().token("7525090362:AAHXJptSLUjMBcAOXA6mn88X44BNlSMUyyE").build()
    
    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))
    
    # بدء البوت
    application.run_polling()

if __name__ == '__main__':
    main()
