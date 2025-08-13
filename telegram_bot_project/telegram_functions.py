"""
وظائف تيليجرام المحولة من النص البرمجي الأصلي
"""
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest, EditAdminRequest
from telethon.tl.types import ChatAdminRights
from random import choice
from asyncio import gather, sleep
import asyncio
import logging

# إعداد السجلات
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramGroupManager:
    def __init__(self, api_id, api_hash, string_sessions, texts, photos, names, bot_username, user_data, user_id):
        self.api_id = api_id
        self.api_hash = api_hash
        self.string_sessions = string_sessions
        self.texts = texts
        self.photos = photos
        self.names = names
        self.bot_username = bot_username
        self.progress_callback = None
        self.created_groups = []
        self.user_data = user_data
        self.user_id = user_id
    def set_progress_callback(self, callback):
        """تعيين دالة لإرسال تحديثات التقدم"""
        self.progress_callback = callback
        
    async def send_progress(self, message):
        """إرسال تحديث التقدم"""
        if self.progress_callback:
            await self.progress_callback(message)
        logger.info(message)
    
    async def send_group_link(self, group_name, group_link):
        """إرسال رابط المجموعة"""
        link_message = f"🔗 **رابط المجموعة**: {group_name}\n{group_link}"
        if self.progress_callback:
            await self.progress_callback(link_message)
        
        # حفظ الرابط في القائمة
        self.created_groups.append({
            'name': group_name,
            'link': group_link
        })
    
    async def send_messages(self, client, chat):
        """إرسال الرسائل والصور للمجموعة"""
        try:
            for _ in range(10):
                if choice([True, False]):
                    await client.send_message(chat, choice(self.texts))
                else:
                    # في حالة عدم وجود الصور، نرسل نص فقط
                    try:
                        await client.send_file(chat, choice(self.photos))
                    except:
                        await client.send_message(chat, choice(self.texts))
                await sleep(1)  # تأخير قصير بين الرسائل
        except Exception as e:
            await self.send_progress(f"خطأ في إرسال الرسائل: {e}")
            
    async def run_session(self, string_session, group_count=50):
        """تشغيل جلسة واحدة"""
        try:
            async with TelegramClient(StringSession(string_session), self.api_id, self.api_hash) as client:
                await self.send_progress(f"🚀 بدء الجلسة: {string_session[:10]}...")
                
                for i in range(group_count):
                    if not self.user_data[self.user_id].get("is_running"):
                        await self.send_progress("❌ تم إلغاء عملية إنشاء المجموعات.")
                        break
                    retries = 3
                    while retries > 0:
                        try:
                            name = choice(self.names)
                            await self.send_progress(f"🚀 إنشاء المجموعة رقم {i+1} في الجلسة: {string_session[:10]}...")
                            
                            # إنشاء المجموعة
                            result = await client(CreateChannelRequest(
                                title=name, 
                                about="وذكر ربك اذا نسيت", 
                                megagroup=True
                            ))
                            chat = result.chats[0]
                            
                            # الحصول على رابط المجموعة
                            try:
                                # إنشاء رابط دعوة للمجموعة
                                from telethon.tl.functions.messages import ExportChatInviteRequest
                                invite_result = await client(ExportChatInviteRequest(peer=chat))
                                group_link = invite_result.link
                                
                                # إرسال رابط المجموعة فوراً
                                await self.send_group_link(name, group_link)
                                
                            except Exception as e:
                                await self.send_progress(f"تحذير: لم يتم الحصول على رابط المجموعة {name}: {e}")
                                # محاولة إنشاء رابط بديل
                                group_link = f"https://t.me/c/{chat.id}"
                                await self.send_group_link(name, group_link)
                            
                            # إضافة البوت
                            try:
                                await client(InviteToChannelRequest(channel=chat, users=[self.bot_username]))
                                
                                # إعطاء صلاحيات للبوت
                                rights = ChatAdminRights(
                                    post_messages=True, edit_messages=True, delete_messages=True,
                                    ban_users=True, invite_users=True, pin_messages=True, add_admins=True
                                )
                                entity = await client.get_entity(self.bot_username)
                                await client(EditAdminRequest(
                                    channel=chat, 
                                    user_id=entity, 
                                    admin_rights=rights, 
                                    rank="Bot Admin"
                                ))
                            except Exception as e:
                                await self.send_progress(f"تحذير: لم يتم إضافة البوت للمجموعة {name}: {e}")
                            
                            # إرسال الرسائل
                            await self.send_messages(client, chat)
                            
                            # رسالة الإنجاز
                            await client.send_message(chat, f"✅ تم إنشاء المجموعة رقم {i+1} بعنوان: {name} بواسطة الحجي @xxbxxbL")
                            
                            await self.send_progress(f"📦 تم الإنشاء: {name}")
                            break
                            
                        except Exception as e:
                            await self.send_progress(f"⚠️ خطأ في المجموعة {i+1} ضمن الجلسة '{string_session[:10]}': {e}")
                            retries -= 1
                            if retries > 0:
                                await self.send_progress(f"🔄 إعادة المحاولة ({3 - retries + 1}/3)...")
                                if not self.user_data[self.user_id].get("is_running"):
                                    await self.send_progress("❌ تم إلغاء عملية إنشاء المجموعات.")
                                    break
                                await sleep(5)
                            else:
                                await self.send_progress(f"❌ فشل نهائي في إنشاء المجموعة رقم {i+1}")
                        
                        if not self.user_data[self.user_id].get("is_running"):
                            await self.send_progress("❌ تم إلغاء عملية إنشاء المجموعات.")
                            break
                        await sleep(2)  # تأخير بين المجموعات
                        
        except Exception as e:
            await self.send_progress(f"❌ خطأ في الجلسة {string_session[:10]}: {e}")
    
    async def run_all_sessions(self, group_count=50):
        """تشغيل جميع الجلسات"""
        try:
            await self.send_progress("🚀 بدء تشغيل جميع الجلسات...")
            tasks = [self.run_session(session, group_count) for session in self.string_sessions if self.user_data[self.user_id].get("is_running")]
            if not tasks:
                await self.send_progress("❌ لم يتم بدء أي جلسة بسبب الإلغاء.")
                return
            await gather(*tasks)
            
            await self.send_progress("✅ تم الانتهاء من جميع الجلسات!")
        except Exception as e:
            await self.send_progress(f"❌ خطأ عام: {e}")
    
    async def send_summary(self):
        """إرسال ملخص بجميع روابط المجموعات المنشأة"""
        if not self.created_groups:
            await self.send_progress("❌ لم يتم إنشاء أي مجموعات.")
            return
        
        summary_message = f"📋 **ملخص المجموعات المنشأة** ({len(self.created_groups)} مجموعة):\n\n"
        
        for i, group in enumerate(self.created_groups, 1):
            summary_message += f"{i}. **{group['name']}**\n{group['link']}\n\n"
            
            # إرسال الملخص على دفعات لتجنب الرسائل الطويلة
            if i % 10 == 0:  # كل 10 مجموعات
                await self.send_progress(summary_message)
                summary_message = ""
        
        # إرسال الباقي إن وجد
        if summary_message.strip():
            await self.send_progress(summary_message)

