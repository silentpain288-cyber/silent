# bot.py - ربات فانتوم نسخه نهایی (تک فایل)
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import json
import os
import random
from datetime import datetime, timedelta
import time

# ==================== تنظیمات ====================
TOKEN = "8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU"
CHANNEL_ID = "@Phantomupdatess"
ADMIN_IDS = [8831703400]

# ==================== دیتابیس ====================
DATA_FILE = "user_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"users": {}, "stats": {"total": 0}}
    return {"users": {}, "stats": {"total": 0}}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ==================== ربات ====================
bot = telebot.TeleBot(TOKEN)

# ==================== بررسی عضویت ====================
def check_membership(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"❌ خطا در بررسی عضویت: {e}")
        return False

# ==================== منوی اصلی ====================
def main_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton("👤 پروفایل")
    btn2 = KeyboardButton("💎 الماس")
    btn3 = KeyboardButton("⭐ اشتراک")
    btn4 = KeyboardButton("💰 پرداخت")
    btn5 = KeyboardButton("📞 پشتیبانی")
    btn6 = KeyboardButton("⚙️ تنظیمات")
    keyboard.add(btn1, btn2)
    keyboard.add(btn3, btn4)
    keyboard.add(btn5, btn6)
    return keyboard

# ==================== دستور /start ====================
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    print(f"✅ کاربر {user_id} استارت زد")
    
    # بررسی عضویت در کانال
    is_member = check_membership(user_id)
    print(f"📌 وضعیت عضویت: {is_member}")
    
    if not is_member:
        keyboard = InlineKeyboardMarkup(row_width=1)
        btn_channel = InlineKeyboardButton("🔗 عضویت در کانال", url="https://t.me/Phantomupdatess")
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
    if str(user_id) not in data["users"]:
        data["users"][str(user_id)] = {
            "name": message.from_user.first_name,
            "username": message.from_user.username,
            "join_date": datetime.now().isoformat(),
            "diamonds": 31,  # هدیه ثبت‌نام
            "score": 0,
            "is_premium": False,
            "premium_expire": None
        }
        data["stats"]["total"] = data["stats"].get("total", 0) + 1
        save_data(data)
        print(f"✅ کاربر جدید ثبت شد: {user_id}")
    
    # پیام خوش‌آمدگویی
    welcome = (
        "🎉 **به ربات فانتوم خوش آمدی!**\n\n"
        f"🎁 **هدیه ثبت‌نام:** ۳۱ 💎 الماس\n"
        "⚡ از دکمه‌های زیر استفاده کن:\n"
        "━━━━━━━━━━━━━━━\n"
        "👤 پروفایل - اطلاعات کاربری\n"
        "💎 الماس - مدیریت الماس\n"
        "⭐ اشتراک - خرید اشتراک\n"
        "💰 پرداخت - پرداخت‌ها\n"
        "📞 پشتیبانی - ارتباط با ما\n"
        "⚙️ تنظیمات - تنظیمات شخصی"
    )
    bot.send_message(chat_id, welcome, reply_markup=main_keyboard(), parse_mode='Markdown')

# ==================== دکمه عضو شدم ====================
@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def check_callback(call):
    user_id = call.from_user.id
    print(f"✅ کاربر {user_id} دکمه عضو شدم رو زد")
    
    if check_membership(user_id):
        bot.edit_message_text(
            "✅ **عضویت تأیید شد!**\n"
            "اکنون می‌توانی از ربات استفاده کنی.",
            call.message.chat.id,
            call.message.message_id
        )
        bot.answer_callback_query(call.id, "🎉 عضویت شما تأیید شد!")
        # ارسال مجدد پیام شروع
        start_command(call.message)
    else:
        bot.answer_callback_query(
            call.id,
            "❌ هنوز عضو کانال نشدی!\nلطفاً اول عضو شو بعد دکمه رو بزن.",
            show_alert=True
        )

# ==================== پروفایل ====================
@bot.message_handler(func=lambda message: message.text == "👤 پروفایل")
def profile_command(message):
    user_id = message.from_user.id
    data = load_data()
    user_data = data["users"].get(str(user_id), {})
    
    if not user_data:
        bot.reply_to(message, "❌ لطفاً ابتدا /start را بزنید.")
        return
    
    text = (
        "👤 **پروفایل کاربری**\n"
        "━━━━━━━━━━━━━━━\n"
        f"🆔 آیدی: `{user_id}`\n"
        f"👤 نام: {user_data.get('name', 'نامشخص')}\n"
        f"📛 یوزرنیم: @{user_data.get('username', 'ندارد')}\n"
        f"📅 تاریخ ثبت: {user_data.get('join_date', '')[:10]}\n"
        "━━━━━━━━━━━━━━━\n"
        f"💎 الماس: {user_data.get('diamonds', 0)}\n"
        f"⭐ امتیاز: {user_data.get('score', 0)}\n"
        "━━━━━━━━━━━━━━━\n"
        f"⭐ وضعیت: {'✅ Premium' if user_data.get('is_premium') else '❌ رایگان'}"
    )
    bot.reply_to(message, text, parse_mode='Markdown')

# ==================== الماس ====================
@bot.message_handler(func=lambda message: message.text == "💎 الماس")
def diamonds_command(message):
    user_id = message.from_user.id
    data = load_data()
    user_data = data["users"].get(str(user_id), {})
    diamonds = user_data.get('diamonds', 0)
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    amounts = [5, 10, 20, 50, 100]
    for amount in amounts:
        price = amount * 8000
        keyboard.add(InlineKeyboardButton(f"{amount}💎 = {price:,}ت", callback_data=f"buy_{amount}"))
    
    text = (
        "💎 **مدیریت الماس**\n"
        "━━━━━━━━━━━━━━━\n"
        f"💎 الماس شما: {diamonds}\n"
        f"💰 قیمت هر الماس: ۸,۰۰۰ تومان\n"
        "━━━━━━━━━━━━━━━\n"
        "تعداد الماس مورد نظر را انتخاب کنید:"
    )
    bot.reply_to(message, text, reply_markup=keyboard, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def buy_diamonds(call):
    amount = int(call.data.split("_")[1])
    price = amount * 8000
    
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
    amount = int(call.data.split("_")[1])
    price = amount * 8000
    
    text = (
        "💰 **پرداخت**\n"
        "━━━━━━━━━━━━━━━\n"
        f"مبلغ: {price:,} تومان\n"
        f"تعداد: {amount} 💎\n\n"
        "📌 **شماره کارت:**\n"
        "`6037 9975 1234 5678`\n\n"
        "🆔 **به نام:** شرکت فانتوم\n\n"
        "📸 بعد از واریز، رسید را ارسال کنید.\n\n"
        "✅ پس از تایید، الماس به حساب شما اضافه می‌شود."
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

# ==================== اشتراک ====================
@bot.message_handler(func=lambda message: message.text == "⭐ اشتراک")
def premium_command(message):
    user_id = message.from_user.id
    data = load_data()
    user_data = data["users"].get(str(user_id), {})
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    plans = [
        ("1 ماه", "40", "30"),
        ("2 ماه", "60", "60"),
        ("4 ماه", "100", "120"),
        ("8 ماه", "130", "240"),
        ("1 سال", "180", "365")
    ]
    for label, price, days in plans:
        keyboard.add(InlineKeyboardButton(f"{label} {price}💎", callback_data=f"premium_{price}_{days}"))
    
    text = (
        "⭐ **خرید اشتراک Premium**\n"
        "━━━━━━━━━━━━━━━\n"
        "پلن‌های موجود:\n\n"
        "🗓 1 ماه = 40 💎\n"
        "🗓 2 ماه = 60 💎\n"
        "🗓 4 ماه = 100 💎\n"
        "🗓 8 ماه = 130 💎\n"
        "🗓 1 سال = 180 💎\n"
        "━━━━━━━━━━━━━━━\n"
        f"💎 الماس شما: {user_data.get('diamonds', 0)}\n\n"
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
    diamonds = user_data.get('diamonds', 0)
    
    if diamonds < price:
        bot.answer_callback_query(
            call.id,
            f"❌ الماس کافی نیست! نیاز به {price} 💎 دارید.",
            show_alert=True
        )
        return
    
    # کسر الماس
    user_data["diamonds"] = diamonds - price
    user_data["is_premium"] = True
    
    # محاسبه تاریخ انقضا
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
    data["users"][str(user_id)] = user_data
    save_data(data)
    
    bot.edit_message_text(
        f"✅ **اشتراک Premium فعال شد!**\n\n"
        f"🗓 مدت: {days} روز\n"
        f"💰 کسر شده: {price} 💎\n"
        f"📅 تاریخ انقضا: {new_end.strftime('%Y/%m/%d')}\n\n"
        "🎉 از امکانات ویژه استفاده کنید!",
        call.message.chat.id,
        call.message.message_id
    )
    bot.answer_callback_query(call.id, "🎉 اشتراک شما فعال شد!")

# ==================== پرداخت ====================
@bot.message_handler(func=lambda message: message.text == "💰 پرداخت")
def payment_command(message):
    text = (
        "💰 **پرداخت**\n"
        "━━━━━━━━━━━━━━━\n"
        "📌 **شماره کارت:**\n"
        "`6037 9975 1234 5678`\n\n"
        "🆔 **به نام:** شرکت فانتوم\n\n"
        "📸 پس از واریز، رسید را برای پشتیبانی ارسال کنید.\n\n"
        "📞 پشتیبانی: @PhantomSupport"
    )
    bot.reply_to(message, text, parse_mode='Markdown')

# ==================== پشتیبانی ====================
@bot.message_handler(func=lambda message: message.text == "📞 پشتیبانی")
def support_command(message):
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
def settings_command(message):
    text = (
        "⚙️ **تنظیمات**\n"
        "━━━━━━━━━━━━━━━\n"
        "🔔 اعلان‌ها: فعال ✅\n"
        "🕐 منطقه زمانی: +3:30\n"
        "🌍 زبان: فارسی\n"
        "━━━━━━━━━━━━━━━\n"
        "تنظیمات بیشتر به زودی..."
    )
    bot.reply_to(message, text, parse_mode='Markdown')

# ==================== دستور help ====================
@bot.message_handler(commands=['help'])
def help_command(message):
    text = (
        "🤖 **راهنمای ربات فانتوم**\n"
        "━━━━━━━━━━━━━━━\n"
        "📌 **دستورات:**\n"
        "/start - شروع مجدد\n"
        "/help - نمایش راهنما\n"
        "/profile - نمایش پروفایل\n"
        "/diamond - مدیریت الماس\n"
        "/premium - خرید اشتراک\n"
        "━━━━━━━━━━━━━━━\n"
        "🔗 **کانال:** @Phantomupdatess"
    )
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['profile'])
def profile_shortcut(message):
    profile_command(message)

@bot.message_handler(commands=['diamond'])
def diamond_shortcut(message):
    diamonds_command(message)

@bot.message_handler(commands=['premium'])
def premium_shortcut(message):
    premium_command(message)

# ==================== پیام‌های دیگر ====================
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text:
        bot.reply_to(
            message,
            "❓ **دستور نامعتبر!**\n\n"
            "از دکمه‌های منو استفاده کنید یا /help را بزنید.",
            parse_mode='Markdown'
        )

# ==================== اجرا ====================
if __name__ == "__main__":
    print("=" * 60)
    print("🤖 ربات فانتوم فعال شد!")
    print(f"📌 کانال: {CHANNEL_ID}")
    print(f"👑 ادمین‌ها: {ADMIN_IDS}")
    print("=" * 60)
    print("⏳ منتظر پیام‌ها هستم...")
    print("📱 به ربات بروید و /start بزنید")
    print("=" * 60)
    
    try:
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        print(f"❌ خطا: {e}")
        import traceback
        traceback.print_exc()
