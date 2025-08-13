"""
ملف إعداد خاص لـ Replit
هذا الملف يساعد في تشغيل البوت على Replit بسهولة
"""

import os
import sys

def check_replit_environment():
    """التحقق من بيئة Replit"""
    if 'REPL_ID' in os.environ:
        print("✅ تم اكتشاف بيئة Replit")
        return True
    else:
        print("⚠️ لم يتم اكتشاف بيئة Replit")
        return False

def setup_for_replit():
    """إعداد البوت للعمل على Replit"""
    print("🔧 إعداد البوت لـ Replit...")
    
    # التحقق من وجود توكن البوت
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        print("❌ لم يتم العثور على BOT_TOKEN في Secrets")
        print("💡 تأكد من إضافة BOT_TOKEN في قسم Secrets في Replit")
        return False
    
    print("✅ تم العثور على BOT_TOKEN")
    
    # التحقق من وجود الملفات المطلوبة
    required_files = ['main.py', 'config.py', 'handlers.py', 'telegram_functions.py', 'requirements.txt']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ ملفات مفقودة: {', '.join(missing_files)}")
        return False
    
    print("✅ جميع الملفات المطلوبة موجودة")
    
    # التحقق من مجلد الصور
    if os.path.exists('images'):
        image_count = len([f for f in os.listdir('images') if f.endswith('.jpg')])
        print(f"✅ تم العثور على {image_count} صورة")
    else:
        print("⚠️ مجلد الصور غير موجود")
    
    return True

def install_requirements():
    """تثبيت المتطلبات"""
    print("📦 تثبيت المكتبات المطلوبة...")
    os.system("pip install -r requirements.txt")
    print("✅ تم تثبيت المكتبات")

def main():
    """الدالة الرئيسية للإعداد"""
    print("🚀 بدء إعداد البوت لـ Replit")
    print("=" * 40)
    
    # التحقق من بيئة Replit
    if not check_replit_environment():
        print("💡 هذا الملف مصمم للعمل على Replit")
    
    # إعداد البوت
    if setup_for_replit():
        print("=" * 40)
        print("✅ تم إعداد البوت بنجاح!")
        print("🎉 يمكنك الآن تشغيل البوت باستخدام: python main.py")
        
        # تشغيل البوت تلقائياً
        print("🚀 بدء تشغيل البوت...")
        os.system("python main.py")
    else:
        print("=" * 40)
        print("❌ فشل في إعداد البوت")
        print("💡 تأكد من:")
        print("   - إضافة BOT_TOKEN في Secrets")
        print("   - رفع جميع ملفات البوت")
        print("   - الاتصال بالإنترنت")

if __name__ == "__main__":
    main()

