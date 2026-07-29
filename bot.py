import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import random
import json
import os
from datetime import datetime

TOKEN = "8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU"
CHANNEL_ID = "@Phantomupdatess"

bot = telebot.TeleBot(TOKEN)

# ==================== بخش ذخیره‌سازی دیتا ====================
DATA_FILE = "user_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"users": {}, "stats": {"total": 0}}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ==================== بخش بررسی عضویت ====================
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
                "🔗 @Phantomupdatess"
            )
            bot.reply_to(message, text, parse_mode='Markdown')
            return
        return func(message)
    return wrapper

# ==================== صفحه کلید اصلی ====================
def main_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton("📊 وضعیت من")
    btn2 = KeyboardButton("🎮 بازی شانس")
    btn3 = KeyboardButton("📢 اطلاعات کانال")
    btn4 = KeyboardButton("👤 پروفایل")
    btn5 = KeyboardButton("🎁 جایزه روزانه")
    btn6 = KeyboardButton("📞 پشتیبانی")
    keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return keyboard

# ==================== دستور /start ====================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    if check_membership(user_id):
        # ثبت کاربر جدید
        data = load_data()
        if str(user_id) not in data["users"]:
            data["users"][str(user_id)] = {
                "first_join": datetime.now().isoformat(),
                "name": message.from_user.first_name,
                "score": 0,
                "daily_claimed": False
            }
            data["stats"]["total"] += 1
            save_data(data)
        
        welcome_text = (
            "👋 **خوش آمدی به ربات فانتوم!**\n\n"
            "⚡ با استفاده از دکمه‌های زیر می‌توانی از خدمات ما استفاده کنی:\n\n"
            "📊 **وضعیت من** - اطلاعات حساب کاربری\n"
            "🎮 **بازی شانس** - یک بازی ساده و جذاب\n"
            "📢 **اطلاعات کانال** - اطلاعات کانال ما\n"
            "👤 **پروفایل** - مشاهده پروفایل\n"
            "🎁 **جایزه روزانه** - دریافت جایزه روزانه\n"
            "📞 **پشتیبانی** - ارتباط با پشتیبانی"
        )
        bot.send_message(chat_id, welcome_text, reply_markup=main_keyboard(), parse_mode='Markdown')
    else:
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
        keyboard = InlineKeyboardMarkup(row_width=1)
        btn_channel = InlineKeyboardButton("❈ 𝙎𝙚𝙡𝙛 𝙋𝙝𝙖𝙣𝙩𝙤𝙢『𖣘』", url="https://t.me/Phantomupdatess")
        btn_check = InlineKeyboardButton("✅ عضو شدم", callback_data="check_membership")
        keyboard.add(btn_channel, btn_check)
        bot.send_message(chat_id, text, reply_markup=keyboard, parse_mode='Markdown')

# ==================== دکمه عضو شدم ====================
@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def check_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    if check_membership(user_id):
        bot.edit_message_text(
            "✅ **عضویت تأیید شد!**\n"
            "اکنون به تمام امکانات ربات دسترسی داری 😉\n\n"
            "🔗 کانال: @Phantomupdatess",
            chat_id,
            message_id
        )
        bot.answer_callback_query(call.id, "🎉 عضویت شما تأیید شد!")
        
        # ارسال منوی اصلی
        welcome_text = (
            "👋 **خوش آمدی به ربات فانتوم!**\n\n"
            "⚡ با استفاده از دکمه‌های زیر می‌توانی از خدمات ما استفاده کنی:"
        )
        bot.send_message(chat_id, welcome_text, reply_markup=main_keyboard(), parse_mode='Markdown')
    else:
        bot.answer_callback_query(
            call.id,
            "❌ هنوز عضو کانال نشدی!\nلطفاً اول عضو شو بعد دکمه رو بزن.",
            show_alert=True
        )

# ==================== دکمه وضعیت من ====================
@bot.message_handler(func=lambda message: message.text == "📊 وضعیت من")
@membership_required
def my_status(message):
    user_id = message.from_user.id
    data = load_data()
    user_data = data["users"].get(str(user_id), {})
    
    status_text = (
        "📊 **وضعیت حساب کاربری**\n"
        "━━━━━━━━━━━━━━━\n"
        f"👤 **نام:** {user_data.get('name', 'ناشناس')}\n"
        f"🆔 **آیدی:** `{user_id}`\n"
        f"⭐ **امتیاز:** {user_data.get('score', 0)}\n"
        f"📅 **تاریخ ثبت:** {user_data.get('first_join', 'نامشخص')[:10]}\n"
        "━━━━━━━━━━━━━━━\n"
        f"📊 **کل کاربران:** {data['stats']['total']}"
    )
    bot.reply_to(message, status_text, parse_mode='Markdown')

# ==================== دکمه بازی شانس ====================
@bot.message_handler(func=lambda message: message.text == "🎮 بازی شانس")
@membership_required
def lucky_game(message):
    user_id = message.from_user.id
    data = load_data()
    
    # بازی شانس: عدد 1 تا 10 حدس بزن
    number = random.randint(1, 10)
    keyboard = InlineKeyboardMarkup(row_width=5)
    buttons = []
    for i in range(1, 11):
        buttons.append(InlineKeyboardButton(str(i), callback_data=f"guess_{i}"))
    keyboard.add(*buttons)
    
    bot.reply_to(
        message,
        "🎮 **بازی شانس!**\n"
        "یک عدد بین 1 تا 10 انتخاب کن:\n"
        "💡 اگر درست حدس بزنی، ۵ امتیاز می‌گیری!",
        reply_markup=keyboard,
        parse_mode='Markdown'
    )
    
    # ذخیره عدد برای کاربر
    data["users"][str(user_id)]["lucky_number"] = number
    save_data(data)

@bot.callback_query_handler(func=lambda call: call.data.startswith("guess_"))
def guess_callback(call):
    user_id = call.from_user.id
    guess = int(call.data.split("_")[1])
    data = load_data()
    user_data = data["users"].get(str(user_id), {})
    correct = user_data.get("lucky_number", 0)
    
    if guess == correct:
        user_data["score"] = user_data.get("score", 0) + 5
        data["users"][str(user_id)] = user_data
        save_data(data)
        bot.answer_callback_query(call.id, "🎉 آفرین! درست حدس زدی! +۵ امتیاز")
        bot.edit_message_text(
            f"✅ **تبریک!**\nعدد {correct} درست بود!\n⭐ امتیاز شما: {user_data['score']}",
            call.message.chat.id,
            call.message.message_id
        )
    else:
        bot.answer_callback_query(call.id, f"❌ عدد {guess} اشتباه بود! عدد {correct} درست بود.")
        bot.edit_message_text(
            f"❌ **متاسفانه!**\nعدد {guess} اشتباه بود.\nعدد درست: {correct}\n\n💪 دوباره تلاش کن!",
            call.message.chat.id,
            call.message.message_id
        )

# ==================== دکمه اطلاعات کانال ====================
@bot.message_handler(func=lambda message: message.text == "📢 اطلاعات کانال")
@membership_required
def channel_info(message):
    info_text = (
        "📢 **کانال رسمی فانتوم**\n"
        "━━━━━━━━━━━━━━━\n"
        "🔗 **لینک:** https://t.me/Phantomupdatess\n"
        "📌 **یوزرنیم:** @Phantomupdatess\n"
        "━━━━━━━━━━━━━━━\n"
        "📝 **توضیحات:**\n"
        "جدیدترین آپدیت‌ها و اخبار فانتوم\n"
        "━━━━━━━━━━━━━━━\n"
        "📊 **آمار:**\n"
        "🔹 تعداد اعضا: {members}\n"
        "━━━━━━━━━━━━━━━\n"
        "💎 عضو شو و از مزایا بهره‌مند شو!"
    )
    try:
        chat = bot.get_chat(CHANNEL_ID)
        members = chat.get_members_count() if hasattr(chat, 'get_members_count') else "نامشخص"
        bot.reply_to(message, info_text.format(members=members), parse_mode='Markdown')
    except:
        bot.reply_to(message, info_text.format(members="نامشخص"), parse_mode='Markdown')

# ==================== دکمه پروفایل ====================
@bot.message_handler(func=lambda message: message.text == "👤 پروفایل")
@membership_required
def profile(message):
    user = message.from_user
    data = load_data()
    user_data = data["users"].get(str(user.id), {})
    
    profile_text = (
        "👤 **پروفایل کاربری**\n"
        "━━━━━━━━━━━━━━━\n"
        f"🆔 **آیدی:** `{user.id}`\n"
        f"👤 **نام:** {user.first_name}\n"
        f"📛 **نام کاربری:** @{user.username if user.username else 'ندارد'}\n"
        f"⭐ **امتیاز:** {user_data.get('score', 0)}\n"
        f"📅 **عضو از:** {user_data.get('first_join', 'نامشخص')[:10]}\n"
        "━━━━━━━━━━━━━━━\n"
        f"🔹 **وضعیت:** {'✅ فعال' if check_membership(user.id) else '❌ غیرفعال'}"
    )
    bot.reply_to(message, profile_text, parse_mode='Markdown')

# ==================== دکمه جایزه روزانه ====================
@bot.message_handler(func=lambda message: message.text == "🎁 جایزه روزانه")
@membership_required
def daily_reward(message):
    user_id = message.from_user.id
    data = load_data()
    user_data = data["users"].get(str(user_id), {})
    
    today = datetime.now().date().isoformat()
    last_claim = user_data.get("daily_last_claim", "")
    
    if last_claim == today:
        bot.reply_to(
            message,
            "❌ **شما امروز جایزه خود را دریافت کرده‌اید!**\n"
            "⏳ فردا دوباره امتحان کن.\n\n"
            "💡 هر روز می‌توانی ۱۰ امتیاز جایزه بگیری!"
        )
    else:
        user_data["score"] = user_data.get("score", 0) + 10
        user_data["daily_last_claim"] = today
        data["users"][str(user_id)] = user_data
        save_data(data)
        
        bot.reply_to(
            message,
            "🎁 **تبریک!**\n"
            "شما جایزه روزانه خود را دریافت کردید!\n"
            f"⭐ +۱۰ امتیاز\n\n"
            f"📊 امتیاز کل: {user_data['score']}"
        )

# ==================== دکمه پشتیبانی ====================
@bot.message_handler(func=lambda message: message.text == "📞 پشتیبانی")
@membership_required
def support(message):
    support_text = (
        "📞 **پشتیبانی فانتوم**\n"
        "━━━━━━━━━━━━━━━\n"
        "💬 برای ارتباط با پشتیبانی، از راه‌های زیر استفاده کن:\n\n"
        "📧 **ایمیل:** support@phantom.com\n"
        "🆔 **آیدی پشتیبانی:** @PhantomSupport\n"
        "━━━━━━━━━━━━━━━\n"
        "⏰ **ساعت پاسخگویی:**\n"
        "🕐 ۱۰ صبح تا ۱۰ شب"
    )
    bot.reply_to(message, support_text, parse_mode='Markdown')

# ==================== دستورات جدید ====================
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "🤖 **راهنمای ربات فانتوم**\n"
        "━━━━━━━━━━━━━━━\n"
        "📌 **دستورات:**\n"
        "/start - شروع مجدد ربات\n"
        "/help - نمایش این پیام\n"
        "/channel - اطلاعات کانال\n"
        "/profile - مشاهده پروفایل\n"
        "/score - مشاهده امتیاز\n"
        "━━━━━━━━━━━━━━━\n"
        "🔹 **منوی اصلی:**\n"
        "از دکمه‌های زیر استفاده کن:\n"
        "📊 وضعیت من\n"
        "🎮 بازی شانس\n"
        "📢 اطلاعات کانال\n"
        "👤 پروفایل\n"
        "🎁 جایزه روزانه\n"
        "📞 پشتیبانی"
    )
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['channel'])
def channel_command(message):
    channel_text = (
        "📢 **کانال رسمی فانتوم**\n\n"
        "🔗 لینک: https://t.me/Phantomupdatess\n"
        "📌 یوزرنیم: @Phantomupdatess\n\n"
        "❗️ برای استفاده از ربات، حتماً عضو کانال شوید."
    )
    bot.reply_to(message, channel_text, parse_mode='Markdown')

@bot.message_handler(commands=['profile'])
@membership_required
def profile_command(message):
    user = message.from_user
    data = load_data()
    user_data = data["users"].get(str(user.id), {})
    
    profile_text = (
        "👤 **پروفایل کاربری**\n"
        "━━━━━━━━━━━━━━━\n"
        f"🆔 **آیدی:** `{user.id}`\n"
        f"👤 **نام:** {user.first_name}\n"
        f"⭐ **امتیاز:** {user_data.get('score', 0)}"
    )
    bot.reply_to(message, profile_text, parse_mode='Markdown')

@bot.message_handler(commands=['score'])
@membership_required
def score_command(message):
    user_id = message.from_user.id
    data = load_data()
    user_data = data["users"].get(str(user_id), {})
    score = user_data.get('score', 0)
    
    bot.reply_to(
        message,
        f"⭐ **امتیاز شما:** {score}\n\n"
        f"📊 **رتبه:** {'🥇 عالی' if score > 50 else '🥈 خوب' if score > 20 else '🥉 تازه‌کار'}"
    )

# ==================== پیام‌های متنی دیگر ====================
@bot.message_handler(func=lambda message: True)
@membership_required
def echo_all(message):
    bot.reply_to(
        message,
        "❓ **دستور نامعتبر!**\n\n"
        "از دکمه‌های منو استفاده کن یا /help را بزن."
    )

# ==================== اجرای ربات ====================
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 ربات فانتوم فعال شد...")
    print(f"📌 کانال: {CHANNEL_ID}")
    print(f"🔗 لینک: https://t.me/Phantomupdatess")
    print("=" * 50)
    print("⏳ منتظر پیام‌ها هستم...")
    bot.infinity_polling(skip_pending=True)
