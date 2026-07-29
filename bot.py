# bot.py - مرحله ۱: عضویت اجباری + خوش‌آمدگویی
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os
from datetime import datetime

# ==================== تنظیمات ====================
TOKEN = "8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU"
CHANNEL_ID = "@Phantomupdatess"
DATA_FILE = "user_data.json"

# ==================== دیتابیس ====================
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

# ==================== پیام خوش‌آمدگویی ====================
def get_welcome_message(user_name):
    """پیام خوش‌آمدگویی حرفه‌ای با نام کاربر"""
    return f"""
🌟 **به جمع فانتومی‌ها خوش اومدی {user_name}!** 🌟

⫸◄◂

❈ **اینجا قراره چه خبر باشه؟** ❈

🎯 **خدمات اختصاصی فانتوم:**
┌─────────────────┐
│ 💎 الماس و کیف پول │
│ ⭐ اشتراک ویژه     │
│ 🎮 بازی و سرگرمی   │
│ 📢 تبلیغات هدفمند  │
│ 👑 پنل اختصاصی     │
└─────────────────┘

⫸◄◂

🔥 **پس بیا تو جمع ما...**
⚡ **عضو شو، از امکانات استفاده کن!**
💪 **با فانتوم، همیشه یه قدم جلوتری!**

📌 **کانال ما:** @Phantomupdatess
"""

# ==================== دکمه‌های خوش‌آمدگویی ====================
def welcome_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_profile = InlineKeyboardButton("👤 پروفایل", callback_data="profile")
    btn_shop = InlineKeyboardButton("🛒 فروشگاه", callback_data="shop")
    btn_support = InlineKeyboardButton("📞 پشتیبانی", callback_data="support")
    btn_help = InlineKeyboardButton("📖 راهنما", callback_data="help")
    keyboard.add(btn_profile, btn_shop)
    keyboard.add(btn_support, btn_help)
    return keyboard

# ==================== دستور /start ====================
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    
    print(f"✅ کاربر {user_name} ({user_id}) استارت زد")
    
    # بررسی عضویت در کانال
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
    
    # ثبت کاربر جدید
    data = load_data()
    if str(user_id) not in data["users"]:
        data["users"][str(user_id)] = {
            "name": user_name,
            "username": message.from_user.username,
            "join_date": datetime.now().isoformat(),
            "last_visit": datetime.now().isoformat(),
            "step": "welcome"  # برای پیگیری مرحله کاربر
        }
        data["stats"]["total"] = data["stats"].get("total", 0) + 1
        save_data(data)
        print(f"✅ کاربر جدید ثبت شد: {user_name}")
    
    # ارسال پیام خوش‌آمدگویی
    welcome_text = get_welcome_message(user_name)
    bot.send_message(
        chat_id, 
        welcome_text, 
        reply_markup=welcome_keyboard(),
        parse_mode='Markdown'
    )

# ==================== دکمه عضو شدم ====================
@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def check_callback(call):
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    
    print(f"✅ {user_name} دکمه عضو شدم رو زد")
    
    if check_membership(user_id):
        bot.edit_message_text(
            "✅ **عضویت تأیید شد!**\n\n"
            "🎉 به جمع فانتومی‌ها خوش اومدی!\n\n"
            "🔥 حالا می‌تونی از همه امکانات استفاده کنی.",
            call.message.chat.id,
            call.message.message_id
        )
        bot.answer_callback_query(call.id, "🎉 عضویت شما تأیید شد!")
        start_command(call.message)  # ارسال مجدد پیام خوش‌آمدگویی
    else:
        bot.answer_callback_query(
            call.id,
            "❌ هنوز عضو کانال نشدی!\nلطفاً اول عضو شو بعد دکمه رو بزن.",
            show_alert=True
        )

# ==================== دکمه‌های خوش‌آمدگویی ====================
@bot.callback_query_handler(func=lambda call: call.data == "profile")
def profile_callback(call):
    bot.answer_callback_query(call.id, "👤 بخش پروفایل به زودی اضافه می‌شود!")
    bot.send_message(
        call.message.chat.id,
        "👤 **پروفایل کاربری**\n\n"
        "🔧 این بخش در مرحله بعدی اضافه می‌شود.\n"
        "⚡ منتظر بروزرسانی باشید!",
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data == "shop")
def shop_callback(call):
    bot.answer_callback_query(call.id, "🛒 فروشگاه به زودی باز می‌شود!")
    bot.send_message(
        call.message.chat.id,
        "🛒 **فروشگاه فانتوم**\n\n"
        "🔧 این بخش در مرحله بعدی اضافه می‌شود.\n"
        "⚡ به زودی با محصولات ویژه برمی‌گردیم!",
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data == "support")
def support_callback(call):
    bot.answer_callback_query(call.id, "📞 پشتیبانی")
    bot.send_message(
        call.message.chat.id,
        "📞 **پشتیبانی فانتوم**\n\n"
        "💬 ارتباط با ما:\n\n"
        "🆔 پشتیبانی: @PhantomSupport\n"
        "━━━━━━━━━━━━━━━\n"
        "⏰ ساعت پاسخگویی: ۱۰ صبح تا ۱۰ شب",
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data == "help")
def help_callback(call):
    bot.answer_callback_query(call.id, "📖 راهنما")
    bot.send_message(
        call.message.chat.id,
        "📖 **راهنمای ربات فانتوم**\n\n"
        "🔹 **مراحل استفاده:**\n"
        "1️⃣ در کانال عضو شوید\n"
        "2️⃣ روی /start کلیک کنید\n"
        "3️⃣ از خدمات استفاده کنید\n\n"
        "🔹 **خدمات:**\n"
        "• 💎 الماس و کیف پول\n"
        "• ⭐ اشتراک ویژه\n"
        "• 🎮 بازی‌های جذاب\n\n"
        "📌 **کانال:** @Phantomupdatess",
        parse_mode='Markdown'
    )

# ==================== پیام‌های متنی ====================
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "/start":
        return  # توسط هندلر بالا مدیریت می‌شود
    
    # بررسی عضویت
    if not check_membership(message.from_user.id):
        bot.reply_to(
            message,
            "⫸◄◂\n"
            "❈ **لطفاً ابتدا عضو کانال شوید!** ❈\n\n"
            "🔗 @Phantomupdatess",
            parse_mode='Markdown'
        )
        return
    
    bot.reply_to(
        message,
        "❓ **دستور نامعتبر!**\n\n"
        "برای شروع، روی /start کلیک کنید.",
        parse_mode='Markdown'
    )

# ==================== اجرا ====================
if __name__ == "__main__":
    print("=" * 60)
    print("🌟 ربات فانتوم - مرحله ۱")
    print("=" * 60)
    print(f"📌 کانال: {CHANNEL_ID}")
    print("💡 ویژگی‌های این مرحله:")
    print("  ✅ عضویت اجباری در کانال")
    print("  ✅ پیام خوش‌آمدگویی حرفه‌ای")
    print("  ✅ دکمه‌های شیشه‌ای (پروفایل، فروشگاه، پشتیبانی، راهنما)")
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
