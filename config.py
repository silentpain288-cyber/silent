# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# توکن ربات
BOT_TOKEN = os.getenv("BOT_TOKEN", "8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU")

# کانال اجباری
CHANNEL_ID = os.getenv("CHANNEL_ID", "@Phantomupdatess")

# تنظیمات الماس
DIAMOND_PRICE = 8000  # قیمت هر الماس به تومان
REGISTRATION_GIFT = 31  # هدیه ثبت‌نام

# تعرفه‌های اشتراک (به الماس)
PREMIUM_PLANS = {
    "1_month": {"price": 40, "days": 30, "label": "1 ماه"},
    "2_months": {"price": 60, "days": 60, "label": "2 ماه"},
    "4_months": {"price": 100, "days": 120, "label": "4 ماه"},
    "8_months": {"price": 130, "days": 240, "label": "8 ماه"},
    "12_months": {"price": 180, "days": 365, "label": "1 سال"},
}

# تعرفه تبلیغات
ADS_PRICE = 250000  # تومان در ماه

# تنظیمات امنیتی
MAX_WITHDRAW_PER_DAY = 3
MAX_INVOICES_OPEN = 5
RATE_LIMIT = 5  # درخواست در دقیقه

# پشتیبانی
SUPPORT_ID = "@PhantomSupport"

# زمان‌ها
TRIAL_DAYS = 14
