"""
معالجات أوامر ورسائل البوت
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_functions import TelegramGroupManager
from config import DEFAULT_TEXTS, DEFAULT_PHOTOS, DEFAULT_NAMES, DEFAULT_BOT_USERNAME, DEFAULT_GROUP_COUNT
import asyncio
import logging

# إعداد السجلات
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# متغيرات لحفظ بيانات المستخدم مؤقتاً
user_data = {}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /start"""
    user_id = update.effective_user.id
    
    welcome_text = """
🤖 مرحباً بك في بوت إنشاء المجموعات!

هذا البوت يساعدك في إنشاء مجموعات تيليجرام بشكل تلقائي ويرسل لك روابط المجموعات فور إنشائها.

📋 الأوامر المتاحة:
/start - بدء التفاعل مع البوت
/help - عرض المساعدة
/setup - إعداد بيانات الحساب
/run - بدء إنشاء المجموعات
/status - عرض الحالة الحالية
/links - عرض روابط المجموعات المنشأة
/cancel - إلغاء العملية الجارية

⚠️ تحذير: استخدم هذا البوت بمسؤولية وتأكد من امتلاكك للصلاحيات اللازمة.
    """
    
    keyboard = [
        [InlineKeyboardButton("📝 إعداد البيانات", callback_data='setup')],
        [InlineKeyboardButton("❓ المساعدة", callback_data='help')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /help"""
    help_text = """
📖 دليل الاستخدام:

1️⃣ **إعداد البيانات** (/setup):
   - أدخل API ID الخاص بك
   - أدخل API Hash الخاص بك  
   - أدخل String Session(s)

2️⃣ **تشغيل البوت** (/run):
   - بعد إعداد البيانات، استخدم هذا الأمر لبدء إنشاء المجموعات

3️⃣ **مراقبة التقدم** (/status):
   - لمعرفة حالة العمليات الجارية

4️⃣ **عرض الروابط** (/links):
   - لعرض روابط جميع المجموعات المنشأة

❗ **ملاحظات مهمة**:
- تأكد من صحة البيانات المدخلة
- البوت سينشئ 50 مجموعة افتراضياً لكل جلسة
- سيتم إرسال روابط المجموعات فور إنشائها
- يمكنك إلغاء العملية في أي وقت باستخدام /cancel

🔒 **الأمان**:
- بياناتك محفوظة مؤقتاً فقط
- يتم حذف البيانات بعد انتهاء العملية
    """
    
    await update.message.reply_text(help_text)

async def setup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /setup"""
    user_id = update.effective_user.id
    
    # تهيئة بيانات المستخدم
    user_data[user_id] = {
        'step': 'api_id',
        'api_id': None,
        'api_hash': None,
        'string_sessions': [],
        'is_running': False
    }
    
    setup_text = """
🔧 **إعداد بيانات الحساب**

الخطوة 1/3: أرسل API ID الخاص بك

💡 يمكنك الحصول على API ID و API Hash من:
https://my.telegram.org/apps

⚠️ تأكد من إدخال البيانات بشكل صحيح.
    """
    
    await update.message.reply_text(setup_text)

async def run_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /run"""
    user_id = update.effective_user.id
    
    if user_id not in user_data:
        await update.message.reply_text("❌ يجب إعداد البيانات أولاً. استخدم /setup")
        return
    
    user_info = user_data[user_id]
    
    if not all([user_info.get('api_id'), user_info.get('api_hash'), user_info.get('string_sessions')]):
        await update.message.reply_text("❌ البيانات غير مكتملة. استخدم /setup لإعداد البيانات")
        return
    
    if user_info.get('is_running'):
        await update.message.reply_text("⚠️ العملية قيد التشغيل بالفعل. استخدم /status لمعرفة التقدم")
        return
    
    # بدء العملية
    user_info['is_running'] = True
    
    keyboard = [[InlineKeyboardButton("إلغاء الإنشاء", callback_data='cancel_creation')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🚀 بدء إنشاء المجموعات... سيتم إرسال تحديثات التقدم.", reply_markup=reply_markup)
    
    # إنشاء مدير المجموعات
    manager = TelegramGroupManager(
        api_id=user_info["api_id"],
        api_hash=user_info["api_hash"],
        string_sessions=user_info["string_sessions"],
        texts=DEFAULT_TEXTS,
        photos=DEFAULT_PHOTOS,
        names=DEFAULT_NAMES,
        bot_username=DEFAULT_BOT_USERNAME,
        user_data=user_data,
        user_id=user_id
    )
    
    # تعيين دالة التقدم
    async def progress_callback(message):
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            logger.error(f"خطأ في إرسال تحديث التقدم: {e}")
    
    manager.set_progress_callback(progress_callback)
    
    # تشغيل العملية في الخلفية
    try:
        await manager.run_all_sessions(DEFAULT_GROUP_COUNT)
        user_info['is_running'] = False
        
        # حفظ روابط المجموعات في بيانات المستخدم
        user_info['created_groups'] = manager.created_groups
        
        await context.bot.send_message(chat_id=user_id, text="✅ تم الانتهاء من جميع العمليات!")
    except Exception as e:
        user_info['is_running'] = False
        await context.bot.send_message(chat_id=user_id, text=f"❌ حدث خطأ: {e}")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /status"""
    user_id = update.effective_user.id
    
    if user_id not in user_data:
        await update.message.reply_text("❌ لا توجد بيانات. استخدم /setup لإعداد البيانات")
        return
    
    user_info = user_data[user_id]
    created_groups_count = len(user_info.get('created_groups', []))
    
    status_text = f"""
📊 **حالة الحساب**:

🆔 API ID: {'✅ محدد' if user_info.get('api_id') else '❌ غير محدد'}
🔑 API Hash: {'✅ محدد' if user_info.get('api_hash') else '❌ غير محدد'}
📱 عدد الجلسات: {len(user_info.get('string_sessions', []))}
🔄 حالة التشغيل: {'🟢 قيد التشغيل' if user_info.get('is_running') else '🔴 متوقف'}
🔗 المجموعات المنشأة: {created_groups_count}

💡 استخدم /links لعرض روابط المجموعات المنشأة
    """
    
    await update.message.reply_text(status_text)

async def links_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /links لعرض روابط المجموعات المنشأة"""
    user_id = update.effective_user.id
    
    if user_id not in user_data:
        await update.message.reply_text("❌ لا توجد بيانات. استخدم /setup لإعداد البيانات")
        return
    
    user_info = user_data[user_id]
    created_groups = user_info.get('created_groups', [])
    
    if not created_groups:
        await update.message.reply_text("❌ لم يتم إنشاء أي مجموعات بعد. استخدم /run لبدء إنشاء المجموعات")
        return
    
    links_text = f"🔗 **روابط المجموعات المنشأة** ({len(created_groups)} مجموعة):\n\n"
    
    for i, group in enumerate(created_groups, 1):
        links_text += f"{i}. **{group['name']}**\n{group['link']}\n\n"
        
        # إرسال الروابط على دفعات لتجنب الرسائل الطويلة
        if i % 10 == 0:  # كل 10 مجموعات
            await update.message.reply_text(links_text)
            links_text = ""
    
    # إرسال الباقي إن وجد
    if links_text.strip():
        await update.message.reply_text(links_text)

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /cancel"""
    user_id = update.effective_user.id
    
    if user_id in user_data:
        user_data[user_id]['is_running'] = False
        await update.message.reply_text("❌ تم إلغاء العملية الجارية.")
    else:
        await update.message.reply_text("❌ لا توجد عملية جارية للإلغاء.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج الرسائل النصية"""
    user_id = update.effective_user.id
    message_text = update.message.text
    
    if user_id not in user_data:
        await update.message.reply_text("استخدم /start للبدء أو /setup لإعداد البيانات")
        return
    
    user_info = user_data[user_id]
    current_step = user_info.get('step')
    
    if current_step == 'api_id':
        try:
            api_id = int(message_text.strip())
            user_info['api_id'] = api_id
            user_info['step'] = 'api_hash'
            await update.message.reply_text("✅ تم حفظ API ID.\n\nالخطوة 2/3: أرسل API Hash الخاص بك")
        except ValueError:
            await update.message.reply_text("❌ API ID يجب أن يكون رقماً. حاول مرة أخرى.")
    
    elif current_step == 'api_hash':
        api_hash = message_text.strip()
        user_info['api_hash'] = api_hash
        user_info['step'] = 'string_sessions'
        await update.message.reply_text("✅ تم حفظ API Hash.\n\nالخطوة 3/3: أرسل String Session(s)\n\n💡 يمكنك إرسال جلسة واحدة أو عدة جلسات (كل جلسة في رسالة منفصلة)\nأرسل 'تم' عند الانتهاء من إدخال الجلسات")
    
    elif current_step == 'string_sessions':
        if message_text.strip().lower() in ['تم', 'done', 'finish']:
            if user_info['string_sessions']:
                user_info['step'] = 'completed'
                await update.message.reply_text(f"✅ تم حفظ {len(user_info['string_sessions'])} جلسة.\n\n🚀 يمكنك الآن استخدام /run لبدء إنشاء المجموعات!")
            else:
                await update.message.reply_text("❌ يجب إدخال جلسة واحدة على الأقل.")
        else:
            session = message_text.strip()
            user_info['string_sessions'].append(session)
            await update.message.reply_text(f"✅ تم حفظ الجلسة رقم {len(user_info['string_sessions'])}.\n\nأرسل جلسة أخرى أو أرسل 'تم' للانتهاء.")
    
    else:
        await update.message.reply_text("استخدم الأوامر المتاحة: /start, /help, /setup, /run, /status, /cancel")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج الأزرار التفاعلية"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'setup':
        await setup_command(update, context)
    elif query.data == 'help':
        await help_command(update, context)
    elif query.data == 'cancel_creation':
        await cancel_creation_callback(update, context)

async def cancel_creation_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج زر إلغاء الإنشاء"""
    user_id = update.effective_user.id
    
    if user_id in user_data and user_data[user_id].get("is_running"):
        user_data[user_id]["is_running"] = False
        await update.callback_query.edit_message_text("❌ تم إلغاء عملية إنشاء المجموعات.")
    else:
        await update.callback_query.edit_message_text("❌ لا توجد عملية إنشاء مجموعات جارية للإلغاء.")


