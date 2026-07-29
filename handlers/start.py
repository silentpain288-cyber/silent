
# handlers/start.py
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta
import random

from config import *
from utils.database import load_data, save_data, generate_id, get_time
from utils.security import check_rate_limit, generate_verification_code, validate_phone
from utils.translations import get_text

# دیکشنری برای ذخیره کدهای تایید موقت
verification_codes = {}

def setup_handlers(bot):
    """تنظیم هندلرهای بخش شروع و ثبت‌نام"""
    
    @bot.message_handler(commands=['start'])
    def start_command(message):
        user_id = message.from_user.id
        chat_id = message.chat.id
        data = load_data("users.json")
        
        # بررسی عضویت در کانال
        try:
            member = bot.get_chat_member(CHANNEL_ID, user_id)
            is_member = member.status in ['member', 'administrator', 'creator']
        except:
            is_member = False
        
        if not is_member:
            keyboard = InlineKeyboardMarkup(row_width=1)
            btn_channel = InlineKeyboardButton("🔗 عضویت در کانال", url=f"https://t.me/{CHANNEL_ID[1:]}")
            btn_check = InlineKeyboardButton("✅ عضو شدم", callback_data="check_membership")
            keyboard.add(btn_channel, btn_check)
            
            text = (
                "⫸◄◂\n"
                "❈ **لطفاً ابتدا عضو کانال شوید!** ❈\n\n"
                "برای استفاده از خدمات Ghost Assistant،\n"
                "ابتدا در کانال زیر عضو شوید:\n\n"
                f"🔗 {CHANNEL_ID}"
            )
            bot.send_message(chat_id, text, reply_markup=keyboard, parse_mode='Markdown')
            return
        
        # بررسی ثبت‌نام
        user_str = str(user_id)
        if user_str in data["users"] and data["users"][user_str].get("phone_verified", False):
            # کاربر ثبت‌نام کرده
            show_main_menu(bot, message)
        else:
            # شروع فرآیند ثبت‌نام
            send_registration_welcome(bot, message)
    
    @bot.callback_query_handler(func=lambda call: call.data == "check_membership")
    def check_membership_callback(call):
        user_id = call.from_user.id
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        
        try:
            member = bot.get_chat_member(CHANNEL_ID, user_id)
            is_member = member.status in ['member', 'administrator', 'creator']
        except:
            is_member = False
        
        if is_member:
            bot.edit_message_text(
                "✅ **عضویت تأیید شد!**\n\n"
                "اکنون می‌توانید ثبت‌نام کنید.",
                chat_id,
                message_id
            )
            bot.answer_callback_query(call.id, "🎉 عضویت شما تأیید شد!")
            
            # ارسال مجدد پیام ثبت‌نام
            send_registration_welcome(bot, call.message)
        else:
            bot.answer_callback_query(
                call.id,
                "❌ هنوز عضو کانال نشدی!\nلطفاً اول عضو شو بعد دکمه رو بزن.",
                show_alert=True
            )
    
    @bot.callback_query_handler(func=lambda call: call.data == "change_lang")
    def change_language(call):
        user_id = call.from_user.id
        data = load_data("users.json")
        
        if str(user_id) not in data["users"]:
            data["users"][str(user_id)] = {}
        
        current_lang = data["users"][str(user_id)].get("language", "fa")
        new_lang = "en" if current_lang == "fa" else "fa"
        data["users"][str(user_id)]["language"] = new_lang
        save_data("users.json", data)
        
        bot.answer_callback_query(
            call.id,
            f"✅ زبان تغییر کرد / Language changed to {new_lang.upper()}"
        )
        bot.edit_message_text(
            f"🌍 زبان به {new_lang.upper()} تغییر یافت!\nLanguage changed to {new_lang.upper()}!",
            call.message.chat.id,
            call.message.message_id
        )
    
    @bot.callback_query_handler(func=lambda call: call.data == "start_register")
    def start_register(call):
        user_id = call.from_user.id
        
        # درخواست شماره از کاربر
        keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        btn_share = KeyboardButton("📱 ارسال شماره", request_contact=True)
        keyboard.add(btn_share)
        
        bot.send_message(
            call.message.chat.id,
            "📱 **لطفاً شماره خود را ارسال کنید:**\n\n"
            "برای این کار روی دکمه‌ی **«ارسال شماره»** کلیک کنید.",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id)
    
    @bot.message_handler(content_types=['contact'])
    def handle_contact(message):
        user_id = message.from_user.id
        contact = message.contact
        
        if contact.user_id == user_id:
            phone = contact.phone_number
            
            if not validate_phone(phone):
                bot.reply_to(message, get_text(user_id, "invalid_phone"))
                return
            
            # ارسال کد تایید
            code = generate_verification_code()
            verification_codes[user_id] = {
                "code": code,
                "phone": phone,
                "expire": datetime.now() + timedelta(minutes=5)
            }
            
            # حذف صفحه‌کلید
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            bot.send_message(
                message.chat.id,
                f"✅ **کد تایید به شماره‌ی شما ارسال شد:**\n\n"
                f"📱 **شماره:** {phone}\n"
                f"🔑 **کد:** `{code}`\n\n"
                f"⏳ کد تا ۵ دقیقه اعتبار دارد.\n\n"
                f"کد را در پیام بعدی وارد کنید:",
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        else:
            bot.reply_to(message, "❌ لطفاً شماره خودتان را ارسال کنید!")
    
    @bot.message_handler(func=lambda message: message.text and message.text.isdigit() and len(message.text) == 6)
    def verify_code(message):
        user_id = message.from_user.id
        
        if user_id not in verification_codes:
            bot.reply_to(message, get_text(user_id, "error"))
            return
        
        data = verification_codes[user_id]
        code = int(message.text)
        
        if datetime.now() > data["expire"]:
            bot.reply_to(message, get_text(user_id, "code_expired"))
            del verification_codes[user_id]
            return
        
        if code == data["code"]:
            # ثبت‌نام کامل
            register_user(user_id, data["phone"])
            del verification_codes[user_id]
            
            bot.reply_to(
                message,
                f"✅ **ثبت‌نام شما با موفقیت انجام شد!**\n\n"
                f"🎁 **هدیه ثبت‌نام:** {REGISTRATION_GIFT} 💎 الماس\n"
                f"⏳ **{TRIAL_DAYS} روز Trial فعال شد**\n\n"
                f"⚡ از منوی اصلی استفاده کنید:"
            )
            show_main_menu(bot, message)
        else:
            bot.reply_to(message, get_text(user_id, "wrong_code"))

def send_registration_welcome(bot, message):
    """ارسال پیام خوش‌آمدگویی ثبت‌نام"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_register = InlineKeyboardButton("📱 ثبت‌نام با شماره", callback_data="start_register")
    btn_lang = InlineKeyboardButton("🌍 تغییر زبان / Change Language", callback_data="change_lang")
    keyboard.add(btn_register, btn_lang)
    
    text = (
        "🌙 **به Ghost Assistant خوش آمدید!**\n\n"
        "⚡ برای استفاده از تمام امکانات، لطفاً ثبت‌نام کنید.\n\n"
        f"🔹 **هدیه ثبت‌نام:** {REGISTRATION_GIFT} 💎 الماس\n"
        f"🔹 **{TRIAL_DAYS} روز Trial رایگان**\n\n"
        "📱 برای شروع، شماره خود را وارد کنید."
    )
    bot.send_message(chat_id, text, reply_markup=keyboard, parse_mode='Markdown')

def register_user(user_id, phone):
    """ثبت‌نام کاربر جدید"""
    data = load_data("users.json")
    
    # تنظیمات کاربر جدید
    data["users"][str(user_id)] = {
        "phone": phone,
        "phone_verified": True,
        "language": "fa",
        "register_date": get_time(),
        "trial_end": (datetime.now() + timedelta(days=TRIAL_DAYS)).isoformat(),
        "is_premium": False,
        "premium_expire": None,
        "diamonds": {
            "gift": REGISTRATION_GIFT,
            "purchased": 0,
            "total": REGISTRATION_GIFT
        },
        "wallet": {
            "balance": 0,
            "transactions": []
        },
        "settings": {
            "timezone": "+3:30",
            "notifications": True,
            "show_time": True,
            "auto_offline": False,
            "offline_text": "🌙 من آفلاین هستم..."
        },
        "last_activity": get_time(),
        "name": f"کاربر {user_id}",
        "username": None
    }
    
    # ثبت تراکنش هدیه
    data["users"][str(user_id)]["wallet"]["transactions"].append({
        "id": generate_id(),
        "type": "gift",
        "amount": REGISTRATION_GIFT,
        "description": "هدیه ثبت‌نام",
        "date": get_time(),
        "status": "completed",
        "diamond_type": "gift"
    })
    
    data["stats"]["total"] = data["stats"].get("total", 0) + 1
    save_data("users.json", data)

def show_main_menu(bot, message):
    """نمایش منوی اصلی"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_profile = KeyboardButton("👤 پروفایل")
    btn_wallet = KeyboardButton("💳 کیف پول")
    btn_diamonds = KeyboardButton("💎 الماس")
    btn_premium = KeyboardButton("⭐ اشتراک")
    btn_payment = KeyboardButton("💰 پرداخت")
    btn_settings = KeyboardButton("⚙️ تنظیمات")
    btn_support = KeyboardButton("📞 پشتیبانی")
    btn_ads = KeyboardButton("📢 تبلیغات")
    
    # دکمه‌های ادمین (فقط برای ادمین‌ها)
    admin_ids = [8831703400]  # آیدی‌های ادمین
    if user_id in admin_ids:
        btn_admin = KeyboardButton("👑 پنل مدیریت")
        keyboard.add(btn_admin)
    
    keyboard.add(btn_profile, btn_wallet)
    keyboard.add(btn_diamonds, btn_premium)
    keyboard.add(btn_payment, btn_ads)
    keyboard.add(btn_settings, btn_support)
    
    text = (
        "⚡ **منوی اصلی Ghost Assistant**\n"
        "━━━━━━━━━━━━━━━\n"
        "از دکمه‌های زیر برای دسترسی به بخش‌ها استفاده کنید:\n\n"
        f"👤 پروفایل - اطلاعات کاربری\n"
        f"💳 کیف پول - مدیریت موجودی\n"
        f"💎 الماس - خرید و مدیریت\n"
        f"⭐ اشتراک - خرید اشتراک\n"
        f"💰 پرداخت - پرداخت‌ها\n"
        f"📢 تبلیغات - ثبت تبلیغ\n"
        f"⚙️ تنظیمات - تنظیمات شخصی\n"
        f"📞 پشتیبانی - ارتباط با ما"
    )
    bot.send_message(chat_id, text, reply_markup=keyboard, parse_mode='Markdown')
