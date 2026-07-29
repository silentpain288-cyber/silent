import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU"
CHANNEL_ID = "@NnHHB5BhE785OTRk"  # یا عدد آیدی کانال

bot = telebot.TeleBot(TOKEN)

# صفحه‌ی کلیدهای درون‌خطی
def membership_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)  # دکمه‌ها زیر هم
    btn_channel = InlineKeyboardButton(
        text="❈ 𝙎𝙚𝙡𝙛 𝙋𝙝𝙖𝙣𝙩𝙤𝙢『𖣘』",
        url="https://t.me/+NnHHB5BhE785OTRk"
    )
    btn_check = InlineKeyboardButton(
        text="✅ عضو شدم",
        callback_data="check_membership"
    )
    keyboard.add(btn_channel, btn_check)
    return keyboard

# پیام خوش‌آمدگویی با عضویت اجباری
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            bot.reply_to(message, "✅ **شما قبلاً عضو کانال هستید!**\nخوش آمدی به جمع فانتومی‌ها ⚡")
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
                message.chat.id,
                text,
                reply_markup=membership_keyboard(),
                parse_mode='Markdown'
            )
    except Exception as e:
        bot.reply_to(message, "⚠️ خطایی رخ داد. لطفاً دوباره تلاش کن.")

# بررسی عضویت با دکمه
@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def check_callback(call):
    user_id = call.from_user.id
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            bot.edit_message_text(
                "✅ **عضویت تأیید شد!**\nاکنون به تمام امکانات ربات دسترسی داری 😉",
                call.message.chat.id,
                call.message.message_id
            )
        else:
            bot.answer_callback_query(
                call.id,
                "❌ هنوز عضو کانال نشدی!\nلطفاً اول عضو شو بعد دکمه رو بزن.",
                show_alert=True
            )
    except:
        bot.answer_callback_query(
            call.id,
            "⚠️ خطا در بررسی عضویت. دوباره تلاش کن.",
            show_alert=True
        )

if __name__ == "__main__":
    print("ربات فعال شد...")
    bot.infinity_polling()
