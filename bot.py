import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU"
CHANNEL_ID = "@Phantomupdatess"  # 🔥 یوزرنیم جدید شما

bot = telebot.TeleBot(TOKEN)

# صفحه‌ی کلیدهای درون‌خطی
def membership_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_channel = InlineKeyboardButton(
        text="❈ 𝙎𝙚𝙡𝙛 𝙋𝙝𝙖𝙣𝙩𝙤𝙢『𖣘』",
        url="https://t.me/Phantomupdatess"  # لینک جدید شما
    )
    btn_check = InlineKeyboardButton(
        text="✅ عضو شدم",
        callback_data="check_membership"
    )
    keyboard.add(btn_channel, btn_check)
    return keyboard

# بررسی عضویت کاربر
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    try:
        # ابتدا بررسی کنید که ربات به کانال دسترسی دارد
        bot.get_chat(CHANNEL_ID)
        
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        
        if member.status in ['member', 'administrator', 'creator']:
            bot.reply_to(
                message, 
                "✅ **شما قبلاً عضو کانال هستید!**\n"
                "خوش آمدی به جمع فانتومی‌ها ⚡\n\n"
                "🔗 کانال: @Phantomupdatess"
            )
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
            bot.send_message(
                chat_id,
                text,
                reply_markup=membership_keyboard(),
                parse_mode='Markdown'
            )
    except Exception as e:
        print(f"❌ خطا: {e}")
        bot.reply_to(
            message, 
            "⚠️ **ربات به کانال دسترسی ندارد!**\n"
            "لطفاً ربات را به‌عنوان ادمین به کانال اضافه کنید.\n\n"
            "🔗 کانال: @Phantomupdatess"
        )

# بررسی عضویت با دکمه
@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def check_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        
        if member.status in ['member', 'administrator', 'creator']:
            bot.edit_message_text(
                "✅ **عضویت تأیید شد!**\n"
                "اکنون به تمام امکانات ربات دسترسی داری 😉\n\n"
                "🔗 کانال: @Phantomupdatess",
                chat_id,
                message_id
            )
            bot.answer_callback_query(call.id, "🎉 عضویت شما تأیید شد!")
        else:
            bot.answer_callback_query(
                call.id,
                "❌ هنوز عضو کانال نشدی!\n"
                "لطفاً اول عضو شو بعد دکمه رو بزن.",
                show_alert=True
            )
    except Exception as e:
        print(f"❌ خطا: {e}")
        bot.answer_callback_query(
            call.id,
            "⚠️ خطا در بررسی عضویت. دوباره تلاش کن.",
            show_alert=True
        )

# دستور کمک
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "🤖 **راهنمای ربات فانتوم**\n\n"
        "📌 **دستورات:**\n"
        "/start - شروع مجدد ربات\n"
        "/help - نمایش این پیام\n"
        "/channel - اطلاعات کانال\n\n"
        "🔗 **کانال ما:**\n"
        "@Phantomupdatess"
    )
    bot.reply_to(message, help_text, parse_mode='Markdown')

# اطلاعات کانال
@bot.message_handler(commands=['channel'])
def channel_command(message):
    channel_text = (
        "📢 **کانال رسمی فانتوم**\n\n"
        "🔗 لینک: https://t.me/Phantomupdatess\n"
        "📌 یوزرنیم: @Phantomupdatess\n\n"
        "❗️ برای استفاده از ربات، حتماً عضو کانال شوید."
    )
    bot.reply_to(message, channel_text, parse_mode='Markdown')

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 ربات فانتوم فعال شد...")
    print(f"📌 کانال: {CHANNEL_ID}")
    print(f"🔗 لینک: https://t.me/Phantomupdatess")
    print("=" * 50)
    bot.infinity_polling(skip_pending=True)
