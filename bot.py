# bot.py - ربات فانتوم نسخه نهایی
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import json
import os
import random
from datetime import datetime, timedelta
import re
import hashlib
import uuid
import time

# ==================== تنظیمات ====================
TOKEN = "8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU"
CHANNEL_ID = "@Phantomupdatess"
DIAMOND_PRICE = 8000
REGISTRATION_GIFT = 31
TRIAL_DAYS = 14
ADMIN_IDS = [8831703400]  # آیدی ادمین‌ها

# ==================== دیتابیس ====================
DATA_FILE = "user_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"users": {}, "stats": {"total": 0}}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_id():
    return str(uuid.uuid4())[:8].upper()

def get_time():
    return datetime.now().isoformat()

# ==================== ربات ====================
bot = telebot.TeleBot(TOKEN)

# ==================== بررسی عضویت ====================
def check_membership(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

def membership_required(func):
    def wrapper(message):
        user_id = message.from_user.id
        if not check_membership(user_id):
            text = (
                "⫸◄◂\n"
                "❈ **لطفاً ابتدا عضو کانال شوید!** ❈\n\n"
                "برای استفاده از خدمات ما،\n"
                "ابتدا در کانال زیر عضو شوید:\n\n"
                f"🔗 {CHANNEL_ID}"
            )
            bot.reply_to(message, text, parse_mode='Markdown')
            return
        return func(message)
    return wrapper

# ==================== صفحه کلید اصلی ====================
def main_keyboard(user_id):
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_profile = KeyboardButton("👤 پروفایل")
    btn_wallet = KeyboardButton("💳 کیف پول")
    btn_diamonds = KeyboardButton("💎 الماس")
    btn_premium = KeyboardButton("⭐ اشتراک")
    btn_payment = KeyboardButton("💰 پرداخت")
    btn_settings = KeyboardButton("⚙️ تنظیمات")
    btn_support = KeyboardButton("📞 پشتیبانی")
    btn_ads = KeyboardButton("📢 تبلیغات")
    
    if user_id in ADMIN_IDS:
        btn_admin = KeyboardButton("👑 پنل مدیریت")
        keyboard.add(btn_admin)
    
    keyboard.add(btn_profile, btn_wallet)
    keyboard.add(btn_diamonds, btn_premium)
    keyboard.add(btn_payment, btn_ads)
    keyboard.add(btn_settings, btn_support)
    return keyboard

# ==================== دکمه‌های الماس ====================
def diamonds_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=3)
    amounts = [5, 10, 20, 50, 100]
    for amount in amounts:
        price = amount * DIAMOND_PRICE
        keyboard.add(InlineKeyboardButton(f"{amount}💎 = {price:,}ت", callback_data=f"buy_{amount}"))
    keyboard.add(InlineKeyboardButton("🔙 بازگشت", callback_data="back_menu"))
    return keyboard

# ==================== دستور /start ====================
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    if not check_membership(user_id):
        keyboard = InlineKeyboardMarkup(row_width=1)
        btn_channel = InlineKeyboardButton("🔗 عضویت در کانال", url=f"https://t.me/{CHANNEL_ID[1:]}")
        btn_check = InlineKeyboardButton("✅ عضو شدم", callback_data="check_membership")
        keyboard.add(btn_channel, btn_check)
        
        text = (
            "⫸◄◂\n"
            "❈ **خوش آمدی رفیق!** ❈\n"
            "برای قدم‌گذاشتن در دنیای **فانتوم**،\n"
            "یک شرط ساده داریم:\n\n"
            "◄ عضویت در کانال اختصاصی ما\n"
            "◄ تا از آخرین رازها و آپدیت‌ها جا نمونی\n\n"
            "⫸ پس همین حالا عضو شو،\n"
            "سپس دکمه‌ی **«عضو شدم»** رو بزن تا مسیر برات هموار بشه!\n\n"
            "⫸◄◂"
        )
        bot.send_message(chat_id, text, reply_markup=keyboard, parse_mode='Markdown')
        return
    
    # ثبت کاربر جدید
    data = load_data()
    user_str = str(user_id)
    
    if user_str not in data["users"]:
        data["users"][user_str] = {
            "phone": None,
            "phone_verified": False,
            "register_date": get_time(),
            "trial_end": (datetime.now() + timedelta(days=TRIAL_DAYS)).isoformat(),
            "is_premium": False,
            "premium_expire": None,
            "diamonds": {"gift": REGISTRATION_GIFT, "purchased": 0, "total": REGISTRATION_GIFT},
            "wallet": {"balance": 0, "transactions": []},
            "settings": {"timezone": "+3:30", "notifications": True},
            "last_activity": get_time(),
            "name": message.from_user.first_name,
            "username": message.from_user.username
        }
        data["stats"]["total"] = data["stats"].get("total", 0) + 1
        save_data(data)
        
        # پیام خوش‌آمدگویی با هدیه
        welcome_text = (
            "🎉 **به Ghost Assistant خوش آمدی!**\n\n"
            f"🎁 **هدیه ثبت‌نام:** {REGISTRATION_GIFT} 💎 الماس\n"
            f"⏳ **{TRIAL_DAYS} روز Trial رایگان**\n\n"
            "⚡ از دکمه‌های زیر استفاده کن:"
        )
        bot.send_message(chat_id, welcome_text, reply_markup=main_keyboard(user_id), parse_mode='Markdown')
    else:
        # کاربر قدیمی
        welcome_back = (
            "👋 **خوش برگشتی!**\n\n"
            "⚡ از دکمه‌های زیر استفاده کن:"
        )
        bot.send_message(chat_id, welcome_back, reply_markup=main_keyboard(user_id), parse_mode='Markdown')

# ==================== دکمه عضو شدم ====================
@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def check_callback(call):
    user_id = call.from_user.id
    
    if check_membership(user_id):
        bot.edit_message_text(
            "✅ **عضویت تأیید شد!**\n"
            "اکنون می‌توانی ثبت‌نام کنی.\n\n"
            "🔗 کانال: @Phantomupdatess",
            call.message.chat.id,
            call.message.message_id
        )
        bot.answer_callback_query(call.id, "🎉 عضویت شما تأیید شد!")
        start_command(call.message)
    else:
        bot.answer_callback_query(
            call.id,
            "❌ هنوز عضو کانال نشدی!\nلطفاً اول عضو شو بعد دکمه رو بزن.",
            show_alert=True
        )

# ==================== پروفایل ====================
@bot.message_handler(func=lambda message: message.text == "👤 پروفایل")
@membership_required
def profile_menu(message):
    user_id = message.from_user.id
    data = load_data()
    user_data = data["users"].get(str(user_id), {})
    
    if not user_data:
        bot.reply_to(message, "❌ لطفاً ابتدا /start را بزنید.")
        return
    
    # محاسبه روزهای باقی‌مانده
    trial_end = user_data.get("trial_end")
    trial_days_left = 0
    if trial_end:
        try:
            end = datetime.fromisoformat(trial_end)
            if datetime.now() < end:
                trial_days_left = (end - datetime.now()).days
        except:
            pass
    
    premium_expire = user_data.get("premium_expire")
    premium_days_left = 0
    is_premium = user_data.get("is_premium", False)
    if premium_expire and is_premium:
        try:
            end = datetime.fromisoformat(premium_expire)
            if datetime.now() < end:
                premium_days_left = (end - datetime.now()).days
            else:
                is_premium = False
        except:
            pass
    
    # وضعیت اشتراک
    if is_premium and premium_days_left > 0:
        status = f"✅ **Premium** ({premium_days_left} روز)"
    elif trial_days_left > 0:
        status = f"⏳ **Trial** ({trial_days_left} روز)"
    else:
        status = "❌ **رایگان**"
    
    diamonds = user_data.get("diamonds", {})
    
    profile_text = (
        "👤 **پروفایل کاربری**\n"
        "━━━━━━━━━━━━━━━\n"
        f"🆔 **آیدی:** `{user_id}`\n"
        f"👤 **نام:** {user_data.get('name', 'نامشخص')}\n"
        f"📛 **یوزرنیم:** @{user_data.get('username', 'ندارد')}\n"
        f"📅 **تاریخ ثبت:** {user_data.get('register_date', '')[:10]}\n"
        "━━━━━━━━━━━━━━━\n"
        f"💎 **الماس:** {diamonds.get('total', 0)}\n"
        f"🎁 **هدیه:** {diamonds.get('gift', 0)}\n"
        f"🛒 **خریداری:** {diamonds.get('purchased', 0)}\n"
        f"💰 **موجودی:** {user_data.get('wallet', {}).get('balance', 0):,} تومان\n"
        "━━━━━━━━━━━━━━━\n"
        f"⭐ **وضعیت:** {status}"
    )
    bot.reply_to(message, profile_text, parse_mode='Markdown')

# ==================== الماس ====================
@bot.message_handler(func=lambda message: message.text == "💎 الماس")
@membership_required
def diamonds_menu(message):
    user_id = message.from_user.id
    data = load_data()
    user_data = data["users"].get(str(user_id), {})
    diamonds = user_data.get("diamonds", {})
    
    text = (
        "💎 **مدیریت الماس**\n"
        "━━━━━━━━━━━━━━━\n"
        f"💎 مجموع: {diamonds.get('total', 0)}\n"
        f"🎁 هدیه: {diamonds.get('gift', 0)}\n"
        f"🛒 خریداری: {diamonds.get('purchased', 0)}\n"
        "━━━━━━━━━━━━━━━\n"
        f"💰 قیمت هر الماس: {DIAMOND_PRICE:,} تومان\n\n"
        "تعداد الماس مورد نظر را انتخاب کنید:"
    )
    bot.reply_to(message, text, reply_markup=diamonds_keyboard(), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def buy_diamonds(call):
    user_id = call.from_user.id
    amount = int(call.data.split("_")[1])
    price = amount * DIAMOND_PRICE
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_confirm = InlineKeyboardButton("✅ تایید", callback_data=f"confirm_{amount}")
    btn_cancel = InlineKeyboardButton("❌ انصراف", callback_data="cancel_buy")
    keyboard.add(btn_confirm, btn_cancel)
    
    bot.edit_message_text(
        f"🛒 **تایید خرید**\n\n"
        f"تعداد: {amount} 💎\n"
        f"مبلغ: {price:,} تومان\n\n"
        "آیا از خرید خود مطمئن هستید؟",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_"))
def confirm_buy(call):
    user_id = call.from_user.id
    amount = int(call.data.split("_")[1])
    price = amount * DIAMOND_PRICE
    
    # ارسال اطلاعات کارت برای پرداخت
    text = (
        "💰 **پرداخت**\n"
        "━━━━━━━━━━━━━━━\n"
        f"مبلغ: {price:,} تومان\n"
        f"تعداد: {amount} 💎\n\n"
        "📌 **شماره کارت:**\n"
        "`6037 9975 1234 5678`\n\n"
        "🆔 **به نام:** شرکت فانتوم\n\n"
        "📸 بعد از واریز، رسید را ارسال کنید."
    )
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id, "💳 اطلاعات پرداخت ارسال شد!")

@bot.callback_query_handler(func=lambda call: call.data == "cancel_buy")
def cancel_buy(call):
    bot.edit_message_text(
        "❌ خرید لغو شد.",
        call.message.chat.id,
        call.message.message_id
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "back_menu")
def back_to_menu(call):
    user_id = call.from_user.id
    bot.edit_message_text(
        "⚡ بازگشت به منوی اصلی",
        call.message.chat.id,
        call.message.message_id
    )
    bot.answer_callback_query(call.id)

# ==================== کیف پول ====================
@bot.message_handler(func=lambda message: message.text == "💳 کیف پول")
@membership_required
def wallet_menu(message):
    user_id = message.from_user.id
    data = load_data()
    user_data = data["users"].get(str(user_id), {})
    wallet = user_data.get("wallet", {})
    
    # نمایش ۵ تراکنش آخر
    transactions = wallet.get("transactions", [])[-5:]
    trans_text = ""
    for t in transactions:
        trans_text += f"• {t.get('date', '')[:10]} - {t.get('type', '')} {t.get('amount', 0)} 💎\n"
    
    if not trans_text:
        trans_text = "هیچ تراکنشی وجود ندارد."
    
    text = (
        "💳 **کیف پول**\n"
        "━━━━━━━━━━━━━━━\n"
        f"💰 موجودی: {wallet.get('balance', 0):,} تومان\n"
        "━━━━━━━━━━━━━━━\n"
        "📊 **گردش حساب (آخرین):**\n"
        f"{trans_text}"
    )
    bot.reply_to(message, text, parse_mode='Markdown')

# ==================== اشتراک ====================
@bot.message_handler(func=lambda message: message.text == "⭐ اشتراک")
@membership_required
def premium_menu(message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    plans = [
        ("1 ماهه", 40, "30"),
        ("2 ماهه", 60, "60"),
        ("4 ماهه", 100, "120"),
        ("8 ماهه", 130, "240"),
        ("1 ساله", 180, "365")
    ]
    for label, price, days in plans:
        keyboard.add(InlineKeyboardButton(f"{label} {price}💎", callback_data=f"premium_{price}_{days}"))
    keyboard.add(InlineKeyboardButton("🔙 بازگشت", callback_data="back_menu"))
    
    text = (
        "⭐ **خرید اشتراک Premium**\n"
        "━━━━━━━━━━━━━━━\n"
        "پلن‌های موجود:\n\n"
        "🗓 **1 ماه** = 40 💎\n"
        "🗓 **2 ماه** = 60 💎\n"
        "🗓 **4 ماه** = 100 💎\n"
        "🗓 **8 ماه** = 130 💎\n"
        "🗓 **1 سال** = 180 💎\n\n"
        "یک پلن را انتخاب کنید:"
    )
    bot.reply_to(message, text, reply_markup=keyboard, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith("premium_"))
def buy_premium(call):
    user_id = call.from_user.id
    parts = call.data.split("_")
    price = int(parts[1])
    days = int(parts[2])
    
    data = load_data()
    user_data = data["users"].get(str(user_id), {})
    diamonds = user_data.get("diamonds", {}).get("total", 0)
    
    if diamonds < price:
        bot.answer_callback_query(
            call.id,
            f"❌ الماس کافی نیست! نیاز به {price} 💎 دارید.",
            show_alert=True
        )
        return
    
    # کسر الماس
    user_data["diamonds"]["total"] -= price
    # کسر از الماس خریداری شده اولویت با خریداری است
    purchased = user_data["diamonds"].get("purchased", 0)
    if purchased >= price:
        user_data["diamonds"]["purchased"] -= price
    else:
        remaining = price - purchased
        user_data["diamonds"]["purchased"] = 0
        user_data["diamonds"]["gift"] -= remaining
    
    # فعال‌سازی پریمیوم
    user_data["is_premium"] = True
    if user_data.get("premium_expire"):
        try:
            old_end = datetime.fromisoformat(user_data["premium_expire"])
            if old_end > datetime.now():
                new_end = old_end + timedelta(days=days)
            else:
                new_end = datetime.now() + timedelta(days=days)
        except:
            new_end = datetime.now() + timedelta(days=days)
    else:
        new_end = datetime.now() + timedelta(days=days)
    
    user_data["premium_expire"] = new_end.isoformat()
    
    # ثبت تراکنش
    user_data["wallet"]["transactions"].append({
        "id": generate_id(),
        "type": "premium",
        "amount": price,
        "description": f"خرید اشتراک {days} روزه",
        "date": get_time(),
        "status": "completed"
    })
    
    data["users"][str(user_id)] = user_data
    save_data(data)
    
    bot.edit_message_text(
        f"✅ **اشتراک Premium فعال شد!**\n\n"
        f"🗓 {days} روز اعتبار\n"
        f"💰 {price} 💎 کسر شد\n\n"
        f"📅 تاریخ انقضا: {new_end.strftime('%Y/%m/%d')}",
        call.message.chat.id,
        call.message.message_id
    )
    bot.answer_callback_query(call.id, "🎉 اشتراک شما فعال شد!")

# ==================== پشتیبانی ====================
@bot.message_handler(func=lambda message: message.text == "📞 پشتیبانی")
@membership_required
def support_menu(message):
    text = (
        "📞 **پشتیبانی فانتوم**\n"
        "━━━━━━━━━━━━━━━\n"
        "💬 ارتباط با ما:\n\n"
        "🆔 پشتیبانی: @PhantomSupport\n"
        "📧 ایمیل: support@phantom.ir\n"
        "━━━━━━━━━━━━━━━\n"
        "⏰ ساعت پاسخگویی: ۱۰ صبح تا ۱۰ شب"
    )
    bot.reply_to(message, text, parse_mode='Markdown')

# ==================== تنظیمات ====================
@bot.message_handler(func=lambda message: message.text == "⚙️ تنظیمات")
@membership_required
def settings_menu(message):
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_lang = KeyboardButton("🌍 تغییر زبان")
    btn_notif = KeyboardButton("🔔 اعلان‌ها")
    btn_time = KeyboardButton("🕐 منطقه زمانی")
    btn_back = KeyboardButton("🔙 بازگشت")
    keyboard.add(btn_lang, btn_notif, btn_time, btn_back)
    
    bot.reply_to(message, "⚙️ **تنظیمات**\nلطفاً گزینه مورد نظر را انتخاب کنید:", reply_markup=keyboard, parse_mode='Markdown')

# ==================== پنل ادمین ====================
@bot.message_handler(func=lambda message: message.text == "👑 پنل مدیریت")
def admin_panel(message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ شما دسترسی به این بخش ندارید!")
        return
    
    data = load_data()
    stats = data.get("stats", {})
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("👤 کاربران", callback_data="admin_users"),
        InlineKeyboardButton("💰 پرداخت‌ها", callback_data="admin_payments"),
        InlineKeyboardButton("📊 آمار", callback_data="admin_stats"),
        InlineKeyboardButton("📣 Broadcast", callback_data="admin_broadcast")
    )
    
    text = (
        "👑 **پنل مدیریت**\n"
        "━━━━━━━━━━━━━━━\n"
        f"👤 کل کاربران: {stats.get('total', 0)}\n"
        f"💎 کل الماس: {stats.get('total_diamonds', 0)}\n"
        f"💰 درآمد کل: {stats.get('total_revenue', 0):,} تومان\n"
        "━━━━━━━━━━━━━━━\n"
        "یک گزینه را انتخاب کنید:"
    )
    bot.reply_to(message, text, reply_markup=keyboard, parse_mode='Markdown')

# ==================== پیام‌های متنی ====================
@bot.message_handler(func=lambda message: True)
@membership_required
def echo_all(message):
    if message.text == "🔙 بازگشت":
        bot.reply_to(message, "⚡ بازگشت به منوی اصلی", reply_markup=main_keyboard(message.from_user.id))
    elif message.text == "🌍 تغییر زبان":
        bot.reply_to(message, "🌍 زبان به انگلیسی تغییر یافت!\nLanguage changed to English!")
    elif message.text == "🔔 اعلان‌ها":
        bot.reply_to(message, "🔔 تنظیمات اعلان‌ها:\nوضعیت: فعال ✅")
    elif message.text == "🕐 منطقه زمانی":
        bot.reply_to(message, "🕐 منطقه زمانی فعلی: +3:30 (ایران)")
    elif message.text == "📢 تبلیغات":
        bot.reply_to(message, "📢 **تبلیغات**\n\nبرای ثبت تبلیغ با پشتیبانی تماس بگیرید:\n@PhantomSupport")
    elif message.text == "💰 پرداخت":
        bot.reply_to(message, "💰 **پرداخت**\n\nشماره کارت:\n`6037 9975 1234 5678`\n\n🆔 به نام: شرکت فانتوم")
    else:
        bot.reply_to(message, "❓ دستور نامعتبر!\nاز دکمه‌های منو استفاده کنید یا /help را بزنید.")

# ==================== راهنما ====================
@bot.message_handler(commands=['help'])
def help_command(message):
    text = (
        "🤖 **راهنمای ربات فانتوم**\n"
        "━━━━━━━━━━━━━━━\n"
        "📌 **دستورات:**\n"
        "/start - شروع مجدد\n"
        "/help - نمایش راهنما\n"
        "/profile - مشاهده پروفایل\n"
        "/diamond - الماس\n"
        "/premium - اشتراک\n"
        "━━━━━━━━━━━━━━━\n"
        "🔗 **کانال:** @Phantomupdatess"
    )
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['profile'])
@membership_required
def profile_command(message):
    profile_menu(message)

@bot.message_handler(commands=['diamond'])
@membership_required
def diamond_command(message):
    diamonds_menu(message)

@bot.message_handler(commands=['premium'])
@membership_required
def premium_command(message):
    premium_menu(message)

# ==================== اجرا ====================
if __name__ == "__main__":
    print("=" * 60)
    print("🤖 ربات فانتوم فعال شد!")
    print(f"📌 کانال: {CHANNEL_ID}")
    print(f"👑 ادمین‌ها: {ADMIN_IDS}")
    print("=" * 60)
    print("⏳ منتظر پیام‌ها هستم...")
    
    try:
        bot.infinity_polling(skip_pending=True)
    except KeyboardInterrupt:
        print("\n⏹️ ربات متوقف شد.")
    except Exception as e:
        print(f"❌ خطا: {e}")
