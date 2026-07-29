# bot.py - ربات فانتوم نسخه نهایی برای هاست
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import json
import os
import random
from datetime import datetime, timedelta
import time
import logging

# ==================== تنظیمات ====================
TOKEN = "8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU"
CHANNEL_ID = "@Phantomupdatess"
ADMIN_IDS = [8831703400]
DIAMOND_PRICE = 8000
REGISTRATION_GIFT = 31
TRIAL_DAYS = 14

# ==================== لاگ ====================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==================== دیتابیس ====================
DATA_FILE = "user_data.json"

def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"خطا در خواندن دیتابیس: {e}")
    return {"users": {}, "stats": {"total": 0, "total_diamonds": 0, "total_revenue": 0}}

def save_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"خطا در ذخیره دیتابیس: {e}")

def generate_id():
    import uuid
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
    except Exception as e:
        logger.error(f"خطا در بررسی عضویت {user_id}: {e}")
        return False

# ==================== منوی اصلی ====================
def main_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_profile = KeyboardButton("👤 پروفایل")
    btn_wallet = KeyboardButton("💳 کیف پول")
    btn_diamonds = KeyboardButton("💎 الماس")
    btn_premium = KeyboardButton("⭐ اشتراک")
    btn_payment = KeyboardButton("💰 پرداخت")
    btn_settings = KeyboardButton("⚙️ تنظیمات")
    btn_support = KeyboardButton("📞 پشتیبانی")
    btn_ads = KeyboardButton("📢 تبلیغات")
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
    return keyboard

# ==================== دستور /start ====================
@bot.message_handler(commands=['start'])
def start_command(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        
        logger.info(f"کاربر {user_id} استارت زد")
        
        if not check_membership(user_id):
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
        
        data = load_data()
        user_str = str(user_id)
        
        if user_str not in data["users"]:
            data["users"][user_str] = {
                "name": message.from_user.first_name,
                "username": message.from_user.username,
                "register_date": get_time(),
                "trial_end": (datetime.now() + timedelta(days=TRIAL_DAYS)).isoformat(),
                "is_premium": False,
                "premium_expire": None,
                "diamonds": {"gift": REGISTRATION_GIFT, "purchased": 0, "total": REGISTRATION_GIFT},
                "wallet": {"balance": 0, "transactions": []},
                "settings": {"timezone": "+3:30", "notifications": True},
                "last_activity": get_time()
            }
            data["stats"]["total"] = data["stats"].get("total", 0) + 1
            save_data(data)
            logger.info(f"کاربر جدید ثبت شد: {user_id}")
            
            welcome = (
                "🎉 **به ربات فانتوم خوش آمدی!**\n\n"
                f"🎁 **هدیه ثبت‌نام:** {REGISTRATION_GIFT} 💎 الماس\n"
                f"⏳ **{TRIAL_DAYS} روز Trial رایگان**\n\n"
                "⚡ از دکمه‌های زیر استفاده کن:"
            )
            bot.send_message(chat_id, welcome, reply_markup=main_keyboard(), parse_mode='Markdown')
        else:
            welcome_back = (
                "👋 **خوش برگشتی!**\n\n"
                "⚡ از دکمه‌های زیر استفاده کن:"
            )
            bot.send_message(chat_id, welcome_back, reply_markup=main_keyboard(), parse_mode='Markdown')
            
    except Exception as e:
        logger.error(f"خطا در start_command: {e}")
        bot.send_message(message.chat.id, "⚠️ خطایی رخ داد. لطفاً دوباره تلاش کن.")

# ==================== دکمه عضو شدم ====================
@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def check_callback(call):
    try:
        user_id = call.from_user.id
        
        if check_membership(user_id):
            bot.edit_message_text(
                "✅ **عضویت تأیید شد!**\n\n"
                "اکنون می‌توانی ثبت‌نام کنی.",
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
    except Exception as e:
        logger.error(f"خطا در check_callback: {e}")

# ==================== پروفایل ====================
@bot.message_handler(func=lambda message: message.text == "👤 پروفایل")
def profile_menu(message):
    try:
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
        
        if is_premium and premium_days_left > 0:
            status = f"✅ **Premium** ({premium_days_left} روز)"
        elif trial_days_left > 0:
            status = f"⏳ **Trial** ({trial_days_left} روز)"
        else:
            status = "❌ **رایگان**"
        
        diamonds = user_data.get("diamonds", {})
        
        text = (
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
        bot.reply_to(message, text, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"خطا در profile_menu: {e}")
        bot.reply_to(message, "⚠️ خطایی رخ داد. لطفاً دوباره تلاش کن.")

# ==================== الماس ====================
@bot.message_handler(func=lambda message: message.text == "💎 الماس")
def diamonds_menu(message):
    try:
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
        
    except Exception as e:
        logger.error(f"خطا در diamonds_menu: {e}")
        bot.reply_to(message, "⚠️ خطایی رخ داد. لطفاً دوباره تلاش کن.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def buy_diamonds(call):
    try:
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
        
    except Exception as e:
        logger.error(f"خطا در buy_diamonds: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_"))
def confirm_buy(call):
    try:
        amount = int(call.data.split("_")[1])
        price = amount * DIAMOND_PRICE
        
        text = (
            "💰 **پرداخت**\n"
            "━━━━━━━━━━━━━━━\n"
            f"مبلغ: {price:,} تومان\n"
            f"تعداد: {amount} 💎\n\n"
            "📌 **شماره کارت:**\n"
            "`6037 9975 1234 5678`\n\n"
            "🆔 **به نام:** شرکت فانتوم\n\n"
            "📸 بعد از واریز، رسید را برای پشتیبانی ارسال کنید.\n\n"
            "📞 پشتیبانی: @PhantomSupport"
        )
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "💳 اطلاعات پرداخت ارسال شد!")
        
    except Exception as e:
        logger.error(f"خطا در confirm_buy: {e}")

@bot.callback_query_handler(func=lambda call: call.data == "cancel_buy")
def cancel_buy(call):
    try:
        bot.edit_message_text(
            "❌ خرید لغو شد.",
            call.message.chat.id,
            call.message.message_id
        )
        bot.answer_callback_query(call.id)
    except Exception as e:
        logger.error(f"خطا در cancel_buy: {e}")

# ==================== اشتراک ====================
@bot.message_handler(func=lambda message: message.text == "⭐ اشتراک")
def premium_menu(message):
    try:
        keyboard = InlineKeyboardMarkup(row_width=2)
        plans = [
            ("1 ماهه", "40", "30"),
            ("2 ماهه", "60", "60"),
            ("4 ماهه", "100", "120"),
            ("8 ماهه", "130", "240"),
            ("1 ساله", "180", "365")
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
            "🗓 1 سال = 180 💎\n\n"
            "یک پلن را انتخاب کنید:"
        )
        bot.reply_to(message, text, reply_markup=keyboard, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"خطا در premium_menu: {e}")
        bot.reply_to(message, "⚠️ خطایی رخ داد. لطفاً دوباره تلاش کن.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("premium_"))
def buy_premium(call):
    try:
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
        
    except Exception as e:
        logger.error(f"خطا در buy_premium: {e}")

# ==================== کیف پول ====================
@bot.message_handler(func=lambda message: message.text == "💳 کیف پول")
def wallet_menu(message):
    try:
        user_id = message.from_user.id
        data = load_data()
        user_data = data["users"].get(str(user_id), {})
        wallet = user_data.get("wallet", {})
        
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
        
    except Exception as e:
        logger.error(f"خطا در wallet_menu: {e}")
        bot.reply_to(message, "⚠️ خطایی رخ داد. لطفاً دوباره تلاش کن.")

# ==================== پرداخت ====================
@bot.message_handler(func=lambda message: message.text == "💰 پرداخت")
def payment_menu(message):
    try:
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
        
    except Exception as e:
        logger.error(f"خطا در payment_menu: {e}")
        bot.reply_to(message, "⚠️ خطایی رخ داد. لطفاً دوباره تلاش کن.")

# ==================== تنظیمات ====================
@bot.message_handler(func=lambda message: message.text == "⚙️ تنظیمات")
def settings_menu(message):
    try:
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
        
    except Exception as e:
        logger.error(f"خطا در settings_menu: {e}")
        bot.reply_to(message, "⚠️ خطایی رخ داد. لطفاً دوباره تلاش کن.")

# ==================== پشتیبانی ====================
@bot.message_handler(func=lambda message: message.text == "📞 پشتیبانی")
def support_menu(message):
    try:
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
        
    except Exception as e:
        logger.error(f"خطا در support_menu: {e}")
        bot.reply_to(message, "⚠️ خطایی رخ داد. لطفاً دوباره تلاش کن.")

# ==================== تبلیغات ====================
@bot.message_handler(func=lambda message: message.text == "📢 تبلیغات")
def ads_menu(message):
    try:
        text = (
            "📢 **تبلیغات**\n"
            "━━━━━━━━━━━━━━━\n"
            "💰 **تعرفه تبلیغات:**\n"
            "🗓 ماهانه: ۲۵۰,۰۰۰ تومان\n\n"
            "📊 **آمار تبلیغ:**\n"
            "🔹 کلیک: ۰\n"
            "🔹 بازدید: ۰\n\n"
            "برای ثبت تبلیغ با پشتیبانی تماس بگیرید:\n"
            "📞 @PhantomSupport"
        )
        bot.reply_to(message, text, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"خطا در ads_menu: {e}")
        bot.reply_to(message, "⚠️ خطایی رخ داد. لطفاً دوباره تلاش کن.")

# ==================== راهنما ====================
@bot.message_handler(commands=['help'])
def help_command(message):
    try:
        text = (
            "🤖 **راهنمای ربات فانتوم**\n"
            "━━━━━━━━━━━━━━━\n"
            "📌 **دستورات:**\n"
            "/start - شروع مجدد\n"
            "/help - نمایش راهنما\n"
            "/profile - مشاهده پروفایل\n"
            "/diamond - مدیریت الماس\n"
            "/premium - خرید اشتراک\n"
            "━━━━━━━━━━━━━━━\n"
            "🔗 **کانال:** @Phantomupdatess"
        )
        bot.reply_to(message, text, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"خطا در help_command: {e}")

@bot.message_handler(commands=['profile'])
def profile_shortcut(message):
    profile_menu(message)

@bot.message_handler(commands=['diamond'])
def diamond_shortcut(message):
    diamonds_menu(message)

@bot.message_handler(commands=['premium'])
def premium_shortcut(message):
    premium_menu(message)

# ==================== پیام‌های دیگر ====================
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        bot.reply_to(
            message,
            "❓ **دستور نامعتبر!**\n\n"
            "از دکمه‌های منو استفاده کنید یا /help را بزنید.",
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"خطا در echo_all: {e}")

# ==================== اجرا ====================
if __name__ == "__main__":
    print("=" * 60)
    print("🤖 Ghost Assistant (فانتوم) فعال شد!")
    print(f"📌 کانال: {CHANNEL_ID}")
    print(f"👑 ادمین‌ها: {ADMIN_IDS}")
    print(f"💎 قیمت هر الماس: {DIAMOND_PRICE:,} تومان")
    print("=" * 60)
    print("⏳ منتظر پیام‌ها هستم...")
    print("=" * 60)
    
    try:
        bot.infinity_polling(skip_pending=True)
    except KeyboardInterrupt:
        print("\n⏹️ ربات متوقف شد.")
    except Exception as e:
        print(f"❌ خطا: {e}")
        import traceback
        traceback.print_exc()
