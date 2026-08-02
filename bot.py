import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# توکن ربات خود را وارد کنید
TOKEN = '8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU'
CHANNEL_USERNAME = '@Phantomupdatess'  # نام کاربری کانال (با @)
CHANNEL_ID = '@Phantomupdatess'  # یا آی‌دی عددی کانال (مثلاً -100123456)

bot = telebot.TeleBot(TOKEN)

# تابع برای بررسی عضویت در کانال
def is_user_member(user_id):
    try:
        member_status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return member_status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"خطا در بررسی عضویت: {e}")
        return False

# دستور /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "کاربر گرامی"

    # طراحی زیبا و منحصربه‌فرد با استفاده از نشانه‌های درخواستی
    welcome_text = f"""
⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

سلام {first_name} عزیز 🌹

⫸◄◂
برای دسترسی به امکانات اختصاصی و دریافت آخرین آپدیت‌های امنیتی، 
نیاز است ابتدا در کانال رسمی ما عضو شوید.
◂◄⫷

📌 عضویت شما در کانال، نه تنها به ما انرژی می‌دهد، 
بلکه از آخرین اخبار و ترفندهای امنیتی نیز باخبرتان می‌کند!

👇 لطفاً پس از عضویت، دکمه «عضو شدم» را بزنید تا وارد ربات شوید.
⫸◄◂
    """

    # ساخت کیبورد با دو دکمه (دورن خطی)
    markup = InlineKeyboardMarkup(row_width=1)  # هر دکمه در یک خط جداگانه

    # دکمه اول: لینک کانال (با آیکون و فونت خاص)
    channel_btn = InlineKeyboardButton(
        text="❈ 𝙎𝙚𝙡𝙛 𝙋𝙝𝙖𝙣𝙩𝙤𝙢『𖣘』", 
        url="https://t.me/Phantomupdatess"
    )
    
    # دکمه دوم: بررسی عضویت (عضو شدم)
    check_btn = InlineKeyboardButton(
        text="✅ عضو شدم ( ✓ )", 
        callback_data="check_membership"
    )

    markup.add(channel_btn, check_btn)

    # ارسال پیام خوش‌آمدگویی
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

# پردازش کلیک روی دکمه "عضو شدم"
@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def handle_check_membership(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    if is_user_member(user_id):
        # اگر کاربر عضو است، دسترسی داده می‌شود
        bot.edit_message_text(
            chat_id=chat_id, 
            message_id=call.message.message_id,
            text="✅ *تبریک!* عضویت شما تأیید شد.\n\nاکنون می‌توانید از تمامی خدمات ربات استفاده کنید.\n⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷",
            parse_mode='Markdown'
        )
        # در اینجا می‌توانید منوی اصلی ربات را نمایش دهید
        # مثلاً: show_main_menu(chat_id)
    else:
        # اگر عضو نیست، خطا نشان داده می‌شود
        bot.answer_callback_query(
            call.id, 
            "⛔ شما هنوز عضو کانال نشده‌اید!\nلطفاً ابتدا روی دکمه کانال کلیک کرده و عضو شوید.", 
            show_alert=True
        )

# اجرای ربات
if __name__ == "__main__":
    print("ربات با موفقیت اجرا شد...")
    bot.infinity_polling()
