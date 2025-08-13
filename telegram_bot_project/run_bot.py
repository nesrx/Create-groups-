"""
ملف تشغيل البوت مع إعدادات للنشر
"""
import os
import sys
import logging
from main import main

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    try:
        logger.info("🚀 بدء تشغيل بوت تيليجرام...")
        
        # التحقق من متغيرات البيئة
        bot_token = os.getenv('BOT_TOKEN')
        if not bot_token:
            logger.warning("⚠️ لم يتم العثور على BOT_TOKEN في متغيرات البيئة")
            logger.info("💡 يمكنك تعيين التوكن باستخدام: export BOT_TOKEN='your_token_here'")
        
        # تشغيل البوت
        main()
        
    except KeyboardInterrupt:
        logger.info("⏹️ تم إيقاف البوت بواسطة المستخدم")
    except Exception as e:
        logger.error(f"❌ خطأ في تشغيل البوت: {e}")
        sys.exit(1)

