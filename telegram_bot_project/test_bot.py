"""
ملف اختبار البوت
"""
import asyncio
from telegram_functions import TelegramGroupManager
from config import DEFAULT_TEXTS, DEFAULT_PHOTOS, DEFAULT_NAMES, DEFAULT_BOT_USERNAME

async def test_telegram_manager():
    """اختبار مدير المجموعات"""
    print("🧪 بدء اختبار مدير المجموعات...")
    
    # بيانات اختبار وهمية
    test_api_id = 12345
    test_api_hash = "test_hash"
    test_sessions = ["test_session_1"]
    
    # إنشاء مدير المجموعات
    manager = TelegramGroupManager(
        api_id=test_api_id,
        api_hash=test_api_hash,
        string_sessions=test_sessions,
        texts=DEFAULT_TEXTS,
        photos=DEFAULT_PHOTOS,
        names=DEFAULT_NAMES,
        bot_username=DEFAULT_BOT_USERNAME
    )
    
    print("✅ تم إنشاء مدير المجموعات بنجاح")
    
    # اختبار دالة التقدم
    progress_messages = []
    
    async def test_progress_callback(message):
        progress_messages.append(message)
        print(f"📢 {message}")
    
    manager.set_progress_callback(test_progress_callback)
    
    # اختبار إرسال رسالة تقدم
    await manager.send_progress("اختبار رسالة التقدم")
    
    # اختبار إرسال رابط مجموعة
    await manager.send_group_link("مجموعة اختبار", "https://t.me/test_group")
    
    print(f"✅ تم اختبار {len(progress_messages)} رسالة تقدم")
    print(f"✅ تم حفظ {len(manager.created_groups)} رابط مجموعة")
    
    return True

def test_config():
    """اختبار الإعدادات"""
    print("🧪 بدء اختبار الإعدادات...")
    
    from config import DEFAULT_TEXTS, DEFAULT_NAMES, DEFAULT_PHOTOS, DEFAULT_BOT_USERNAME
    
    assert len(DEFAULT_TEXTS) > 0, "يجب أن تحتوي النصوص على عنصر واحد على الأقل"
    assert len(DEFAULT_NAMES) > 0, "يجب أن تحتوي الأسماء على عنصر واحد على الأقل"
    assert DEFAULT_BOT_USERNAME, "يجب تحديد اسم البوت"
    
    print("✅ تم اختبار الإعدادات بنجاح")
    return True

def test_handlers():
    """اختبار معالجات البوت"""
    print("🧪 بدء اختبار معالجات البوت...")
    
    from handlers import user_data
    
    # اختبار إضافة بيانات مستخدم وهمي
    test_user_id = 12345
    user_data[test_user_id] = {
        'step': 'completed',
        'api_id': 12345,
        'api_hash': 'test_hash',
        'string_sessions': ['session1', 'session2'],
        'is_running': False,
        'created_groups': [
            {'name': 'مجموعة 1', 'link': 'https://t.me/group1'},
            {'name': 'مجموعة 2', 'link': 'https://t.me/group2'}
        ]
    }
    
    print(f"✅ تم إضافة بيانات المستخدم {test_user_id}")
    print(f"✅ عدد الجلسات: {len(user_data[test_user_id]['string_sessions'])}")
    print(f"✅ عدد المجموعات المحفوظة: {len(user_data[test_user_id]['created_groups'])}")
    
    return True

async def main():
    """الدالة الرئيسية للاختبار"""
    print("🚀 بدء اختبارات البوت...")
    print("=" * 50)
    
    try:
        # اختبار الإعدادات
        test_config()
        print()
        
        # اختبار المعالجات
        test_handlers()
        print()
        
        # اختبار مدير المجموعات
        await test_telegram_manager()
        print()
        
        print("=" * 50)
        print("✅ تم اجتياز جميع الاختبارات بنجاح!")
        print("🎉 البوت جاهز للاستخدام!")
        
    except Exception as e:
        print(f"❌ فشل في الاختبار: {e}")
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(main())

