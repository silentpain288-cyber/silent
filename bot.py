import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU'
CHANNEL_ID = '@Phantomupdatess'

bot = telebot.TeleBot(TOKEN)

def is_user_member(user_id):
    try:
        member_status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return member_status in ['member', 'administrator', 'creator']
    except:
        return False

def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("👤 حساب کاربری", callback_data="account")
    btn2 = InlineKeyboardButton("💎 الماس", callback_data="diamond")
    btn3 = InlineKeyboardButton("💳 کیف پول", callback_data="wallet")
    btn4 = InlineKeyboardButton("⭐ اشتراک", callback_data="subscription")
    btn5 = InlineKeyboardButton("🤖 امکانات", callback_data="features")
    btn6 = InlineKeyboardButton("📢 تبلیغات", callback_data="ads")
    btn7 = InlineKeyboardButton("⚙️ تنظیمات", callback_data="settings")
    btn8 = InlineKeyboardButton("📞 پشتیبانی", callback_data="support")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "کاربر گرامی"
    
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

@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def handle_check_membership(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if is_user_member(user_id):
        menu_text = """
⫸◄◂ 𝕄𝕖𝕟𝕦 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

✅ تبریک! عضویت شما تأیید شد.

📌 لطفاً یکی از گزینه‌های زیر را انتخاب کنید:

👤 حساب کاربری
💎 الماس  
💳 کیف پول
⭐ اشتراک
🤖 امکانات
📢 تبلیغات
⚙️ تنظیمات
📞 پشتیبانی

⫸◄◂
"""
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=menu_text,
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )
    else:
        bot.answer_callback_query(
            call.id,
            "⛔ شما هنوز عضو کانال نشده‌اید!\nلطفاً ابتدا روی دکمه کانال کلیک کرده و عضو شوید.",
            show_alert=True
        )

@bot.callback_query_handler(func=lambda call: True)
def handle_menu_buttons(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not is_user_member(user_id):
        bot.answer_callback_query(
            call.id,
            "⛔ شما از کانال خارج شده‌اید!\nلطفاً دوباره عضو شوید.",
            show_alert=True
        )
        return
    
    responses = {
        "account": "👤 *حساب کاربری*\n\nنام: {}\nآیدی: `{}`\nوضعیت: فعال ✅".format(
            call.from_user.first_name, call.from_user.id
        ),
        "diamond": "💎 *الماس*\n\nتعداد الماس شما: ۰\nبرای دریافت الماس، از بخش اشتراک استفاده کنید.",
        "wallet": "💳 *کیف پول*\n\nموجودی: ۰ تومان\nتراکنش‌های اخیر: ندارد",
        "subscription": "⭐ *اشتراک*\n\nاشتراک فعلی: رایگان\nبرای تهیه اشتراک ویژه کلیک کنید.",
        "features": "🤖 *امکانات*\n\n🔹 ابزارهای امنیتی\n🔹 اسکنر فایل\n🔹 گزارش‌گیری خودکار",
        "ads": "📢 *تبلیغات*\n\nبرای تبلیغات در کانال ما، با پشتیبانی تماس بگیرید.",
        "settings": "⚙️ *تنظیمات*\n\n🔹 تغییر زبان\n🔹 اعلان‌ها\n🔹 حریم خصوصی",
        "support": "📞 *پشتیبانی*\n\nبرای ارتباط با پشتیبانی:\n📧 @PhantomSupport\n🕘 پاسخگویی ۲۴/۷"
    }
    
    if call.data in responses:
        markup = InlineKeyboardMarkup(row_width=1)
        back_btn = InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_menu")
        markup.add(back_btn)
        
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=responses[call.data],
            reply_markup=markup,
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id)
    
    elif call.data == "back_to_menu":
        menu_text = """
⫸◄◂ 𝕄𝕖𝕟𝕦 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

📌 لطفاً یکی از گزینه‌های زیر را انتخاب کنید:

👤 حساب کاربری
💎 الماس  
💳 کیف پول
⭐ اشتراک
🤖 امکانات
📢 تبلیغات
⚙️ تنظیمات
📞 پشتیبانی

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

if __name__ == "__main__":
    print("🤖 ربات با موفقیت اجرا شد...")
    bot.infinity_polling()
