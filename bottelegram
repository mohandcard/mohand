
import logging
from telegram import Update, ChatMember
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# تكوين التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# الكلمات الممنوعة
BANNED_WORDS = ["ارسيل", "واتساب", "تلغرام"]  # استبدل هذه بالكلمات التي تريد مراقبتها

def start(update: Update, context: CallbackContext):
    update.message.reply_text('مرحبًا! أنا بوت إدارة المجموعات. سأقوم بإعلام المشرفين عند اكتشاف كلمات ممنوعة.')

def check_message(update: Update, context: CallbackContext):
    message = update.message
    chat_id = message.chat_id
    
    # التحقق من أن الرسالة في مجموعة
    if message.chat.type in ['group', 'supergroup']:
        text = message.text.lower() if message.text else ""
        
        # البحث عن الكلمات الممنوعة
        found_words = [word for word in BANNED_WORDS if word.lower() in text]
        
        if found_words:
            # الحصول على قائمة المشرفين
            admins = context.bot.get_chat_administrators(chat_id)
            
            # إرسال تنبيه لكل مشرف
            for admin in admins:
                try:
                    context.bot.send_message(
                        chat_id=admin.user.id,
                        text=f"⚠️ تنبيه: تم اكتشاف كلمة ممنوعة في المجموعة {message.chat.title}\n\n"
                             f"المستخدم: {message.from_user.mention_html()}\n"
                             f"الكلمات: {', '.join(found_words)}\n"
                             f"الرسالة: {message.text}\n\n"
                             f"رابط الرسالة: {message.link}"
                    )
                except Exception as e:
                    logger.error(f"فشل في إرسال التنبيه للمشرف {admin.user.id}: {e}")

def error(update: Update, context: CallbackContext):
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    # استبدل 'TOKEN' ب token البوت الخاص بك
    updater = Updater("7525090362:AAHXJptSLUjMBcAOXA6mn88X44BNlSMUyyE", use_context=True)
    dp = updater.dispatcher

    # معالجات الأوامر
    dp.add_handler(CommandHandler("start", start))
    
    # معالج الرسائل
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_message))
    
    # معالج الأخطاء
    dp.add_error_handler(error)

    # بدأ البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
