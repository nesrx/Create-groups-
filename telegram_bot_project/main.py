"""
الملف الرئيسي لبوت تيليجرام
"""
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from handlers import (
    start_command, help_command, setup_command, run_command, 
    status_command, links_command, cancel_command, handle_message, handle_callback
)
from config import BOT_TOKEN

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """الدالة الرئيسية لتشغيل البوت"""
    
    # التحقق من وجود توكن البوت
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        logger.error("❌ يجب تعيين توكن البوت في متغير البيئة BOT_TOKEN أو في ملف config.py")
        return
    
    # إنشاء التطبيق
    application = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة معالجات الأوامر
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("setup", setup_command))
    application.add_handler(CommandHandler("run", run_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("links", links_command))
    application.add_handler(CommandHandler("cancel", cancel_command))
    
    # إضافة معالج الرسائل النصية
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # إضافة معالج الأزرار التفاعلية
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    # بدء تشغيل البوت
    logger.info("🚀 بدء تشغيل البوت...")
    application.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == '__main__':
    main()

