import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU'
CHANNEL_ID = '@Phantomupdatess'

bot = telebot.TeleBot(TOKEN)

# ==================== بررسی عضویت ====================

def is_user_member(user_id):
    try:
        member_status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return member_status in ['member', 'administrator', 'creator']
    except:
        return False

# ==================== منوی اصلی (فقط دکمه حساب کاربری) ====================

def main_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("👤 حساب کاربری", callback_data="account")
    markup.add(btn1)
    return markup

# ==================== دستور /start ====================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "کاربر گرامی"
    
    # بررسی عضویت در همان ابتدا
    if is_user_member(user_id):
        # اگر عضو هست، مستقیم بره به منو
        menu_text = """
⫸◄◂ 𝕄𝕖𝕟𝕦 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

✅ به ربات خوش آمدید!

📌 لطفاً یکی از گزینه‌های زیر را انتخاب کنید:

👤 حساب کاربری

⫸◄◂
"""
        bot.send_message(
            message.chat.id,
            menu_text,
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )
    else:
        # اگر عضو نیست، پیام عضویت اجباری نمایش داده میشه
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
        
        markup = InlineKeyboardMarkup(row_width=1)
        channel_btn = InlineKeyboardButton("❈ 𝙎𝙚𝙡𝙛 𝙋𝙝𝙖𝙣𝙩𝙤𝙢『𖣘』", url="https://t.me/Phantomupdatess")
        check_btn = InlineKeyboardButton("✅ عضو شدم ( ✓ )", callback_data="check_membership")
        markup.add(channel_btn, check_btn)
        
        bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

# ==================== بررسی کلیک روی دکمه عضو شدم ====================

@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def handle_check_membership(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if is_user_member(user_id):
        # عضویت تأیید شد - نمایش منو
        menu_text = """
⫸◄◂ 𝕄𝕖𝕟𝕦 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

✅ تبریک! عضویت شما تأیید شد.

📌 لطفاً یکی از گزینه‌های زیر را انتخاب کنید:

👤 حساب کاربری

⫸◄◂
"""
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=menu_text,
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "✅ عضویت شما تأیید شد!", show_alert=False)
    else:
        bot.answer_callback_query(
            call.id,
            "⛔ شما هنوز عضو کانال نشده‌اید!\nلطفاً ابتدا روی دکمه کانال کلیک کرده و عضو شوید.",
            show_alert=True
        )

# ==================== دکمه حساب کاربری ====================

@bot.callback_query_handler(func=lambda call: call.data == "account")
def handle_account(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    # بررسی مجدد عضویت
    if not is_user_member(user_id):
        bot.answer_callback_query(
            call.id,
            "⛔ شما از کانال خارج شده‌اید!\nلطفاً دوباره عضو شوید.",
            show_alert=True
        )
        # برگردوندن به پیام عضویت
        first_name = call.from_user.first_name or "کاربر گرامی"
        welcome_text = f"""
⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

سلام {first_name} عزیز 🌹

⫸◄◂
برای دسترسی به امکانات اختصاصی و دریافت آخرین آپدیت‌های امنیتی، 
نیاز است ابتدا در کانال رسمی ما عضو شوید.
◂◄⫷

👇 لطفاً پس از عضویت، دکمه «عضو شدم» را بزنید.
⫸◄◂
        """
        markup = InlineKeyboardMarkup(row_width=1)
        channel_btn = InlineKeyboardButton("❈ 𝙎𝙚𝙡𝙛 𝙋𝙝𝙖𝙣𝙩𝙤𝙢『𖣘』", url="https://t.me/Phantomupdatess")
        check_btn = InlineKeyboardButton("✅ عضو شدم ( ✓ )", callback_data="check_membership")
        markup.add(channel_btn, check_btn)
        
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=welcome_text,
            reply_markup=markup,
            parse_mode='Markdown'
        )
        return
    
    # نمایش اطلاعات حساب کاربری
    account_text = f"""
⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

👤 *حساب کاربری*

📌 مشخصات:
┌─────────────────
│ 👤 نام: {call.from_user.first_name}
│ 🆔 آیدی: `{call.from_user.id}`
│ ✅ وضعیت: عضو فعال
│ 📅 تاریخ عضویت: امروز
└─────────────────

💎 الماس: ۰
⭐ اشتراک: رایگان

⫸◄◂
"""
    
    # دکمه بازگشت به منو
    markup = InlineKeyboardMarkup(row_width=1)
    back_btn = InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_menu")
    markup.add(back_btn)
    
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text=account_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id)

# ==================== دکمه بازگشت به منو ====================

@bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
def handle_back_to_menu(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not is_user_member(user_id):
        bot.answer_callback_query(
            call.id,
            "⛔ شما از کانال خارج شده‌اید!",
            show_alert=True
        )
        return
    
    menu_text = """
⫸◄◂ 𝕄𝕖𝕟𝕦 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

✅ به ربات خوش آمدید!

📌 لطفاً یکی از گزینه‌های زیر را انتخاب کنید:

👤 حساب کاربری

⫸◄◂
"""
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text=menu_text,
        reply_markup=main_menu(),
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id)

# ==================== اجرا ====================

if __name__ == "__main__":
    print("🤖 ربات با موفقیت اجرا شد...")
    print("📌 @PhantomSecurityBot")
    bot.infinity_polling()
