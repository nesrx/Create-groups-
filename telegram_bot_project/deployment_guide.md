# دليل نشر بوت تيليجرام

## المتطلبات قبل النشر

### 1. الحصول على توكن البوت
1. تحدث مع [@BotFather](https://t.me/BotFather) على تيليجرام
2. أرسل `/newbot` لإنشاء بوت جديد
3. اختر اسماً للبوت (مثل: "مجموعاتي البوت")
4. اختر معرفاً للبوت (يجب أن ينتهي بـ `bot`)
5. احفظ التوكن الذي سيرسله لك BotFather

### 2. إعداد التوكن في البوت
**الطريقة الأولى: متغير البيئة (الأفضل)**
```bash
export BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
```

**الطريقة الثانية: تعديل ملف config.py**
```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

## طرق النشر

### الطريقة الأولى: التشغيل المحلي
```bash
# تثبيت المتطلبات
pip install -r requirements.txt

# تشغيل البوت
python main.py
```

### الطريقة الثانية: النشر على خادم
1. رفع الملفات إلى الخادم
2. تثبيت Python 3.8+ والمتطلبات
3. تشغيل البوت كخدمة:

```bash
# إنشاء ملف خدمة systemd
sudo nano /etc/systemd/system/telegram-bot.service
```

محتوى الملف:
```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/path/to/telegram_bot_project
Environment=BOT_TOKEN=YOUR_BOT_TOKEN_HERE
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

تفعيل الخدمة:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

### الطريقة الثالثة: النشر على Heroku
1. إنشاء ملف `Procfile`:
```
worker: python main.py
```

2. إنشاء ملف `runtime.txt`:
```
python-3.11.0
```

3. رفع المشروع إلى Heroku وتعيين متغير البيئة `BOT_TOKEN`

### الطريقة الرابعة: النشر باستخدام Docker
إنشاء ملف `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

تشغيل البوت:
```bash
docker build -t telegram-bot .
docker run -e BOT_TOKEN=YOUR_TOKEN_HERE telegram-bot
```

## اختبار البوت بعد النشر

1. ابحث عن البوت في تيليجرام باستخدام المعرف
2. أرسل `/start` للبوت
3. تأكد من ظهور رسالة الترحيب والأزرار
4. جرب أمر `/help` للتأكد من عمل جميع الأوامر

## مراقبة البوت

### عرض السجلات
```bash
# إذا كان يعمل كخدمة systemd
sudo journalctl -u telegram-bot -f

# إذا كان يعمل مباشرة
tail -f bot.log
```

### إعادة تشغيل البوت
```bash
# إذا كان يعمل كخدمة systemd
sudo systemctl restart telegram-bot

# إذا كان يعمل مباشرة
pkill -f "python main.py"
python main.py
```

## نصائح الأمان

1. **لا تشارك توكن البوت** مع أي شخص
2. **استخدم متغيرات البيئة** لحفظ التوكن بدلاً من كتابته في الكود
3. **راقب استخدام البوت** بانتظام
4. **احتفظ بنسخة احتياطية** من الكود والإعدادات
5. **حدث المكتبات** بانتظام لضمان الأمان

## استكشاف الأخطاء

### مشاكل شائعة:
1. **"Invalid token"**: تأكد من صحة توكن البوت
2. **"Module not found"**: تأكد من تثبيت جميع المتطلبات
3. **"Permission denied"**: تأكد من صلاحيات الملفات والمجلدات
4. **البوت لا يستجيب**: تحقق من السجلات وحالة الاتصال بالإنترنت

### الحلول:
- راجع ملف `bot.log` للحصول على تفاصيل الأخطاء
- تأكد من استقرار الاتصال بالإنترنت
- تحقق من صحة جميع المتطلبات والإعدادات

