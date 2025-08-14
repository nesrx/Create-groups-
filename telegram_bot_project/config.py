import os

TOKEN_FILE = "bot_token.txt"

# إذا كان الملف موجود نقرأ التوكن منه
if os.path.exists(TOKEN_FILE):
    with open(TOKEN_FILE, "r") as f:
        BOT_TOKEN = f.read().strip()
else:
    # أول مرة نطلب من المستخدم
    BOT_TOKEN = input("📌 ادخل توكن البوت: ").strip()
    # نحفظه في الملف
    with open(TOKEN_FILE, "w") as f:
        f.write(BOT_TOKEN)

# النصوص والصور الافتراضية
DEFAULT_TEXTS = [
    "‏ويَبقىٰ أنِيسُكَ في متاهاتِ العُمرِ القُرآن .",
    "اللهم يسر لنا أمورنا ، و اشرح لنا صدورنا .",
    "فباللهِ الصَبر ، وباللهِ اليُسر ، وباللهِ العون .",
    "لَن يضُرَّ قلبك شَيء مَادام الله ساكُناً فيه .",
    "فانية ياللّٰه، فلا تّجعلها تشقينا",
    "لَا إِلَهَ إِلَّا أَنْتَ سُبْحَانَكَ إِنِّي كُنْتُ مِنَ الظَّالِمِين",
    """
    قال ﷺ : اكثروا من الصلاة عليّ #ليلة_الجمعة ويوم الجمعة فإن صلاتكم معروضة عليّ .
    - اللهم صلِ وسلّم وبارك على نبيِّنا مُحمد .
    """
]

DEFAULT_PHOTOS = [
    "images/islamic_1.jpg", "images/islamic_2.jpg", "images/islamic_3.jpg", 
    "images/islamic_4.jpg", "images/islamic_5.jpg", "images/islamic_6.jpg"
]

DEFAULT_NAMES = [
    "الى ما الا نهائية", "بدبد", "في المستقبل", "يا انا يا انا",
    "حومصصص", "عشوائيات", "وذكر ربك", "استغفر الله", "الحجي", "25 الى المستقبل"
]

DEFAULT_BOT_USERNAME = 'D7Bot'
DEFAULT_GROUP_COUNT = 50
DEFAULT_MESSAGE_COUNT = 10

