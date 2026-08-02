import telebot
import sqlite3
import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU'
CHANNEL_ID = '@Phantomupdatess'

bot = telebot.TeleBot(TOKEN)

# ==================== دیتابیس ====================

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # جدول کاربران
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            username TEXT,
            join_date TEXT,
            subscription_end TEXT,
            diamonds INTEGER DEFAULT 30,
            wallet_balance INTEGER DEFAULT 0,
            is_subscribed INTEGER DEFAULT 0,
            first_join INTEGER DEFAULT 1
        )
    ''')
    
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def add_user(user_id, first_name, username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # تاریخ انقضای اشتراک (1 ماه بعد)
    today = datetime.datetime.now()
    expiry = today + datetime.timedelta(days=30)
    expiry_str = expiry.strftime('%Y-%m-%d %H:%M:%S')
    
    c.execute('''
        INSERT OR IGNORE INTO users 
        (user_id, first_name, username, join_date, subscription_end, diamonds, wallet_balance, is_subscribed, first_join)
        VALUES (?, ?, ?, ?, ?, 30, 0, 1, 0)
    ''', (user_id, first_name, username, today.strftime('%Y-%m-%d %H:%M:%S'), expiry_str))
    
    conn.commit()
    conn.close()

def update_user_info(user_id, first_name, username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        UPDATE users 
        SET first_name = ?, username = ?
        WHERE user_id = ?
    ''', (first_name, username, user_id))
    conn.commit()
    conn.close()

def get_user_diamonds(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT diamonds FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def get_user_wallet(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT wallet_balance FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def get_user_subscription(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT subscription_end, is_subscribed FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result if result else (None, 0)

def check_subscription_status(user_id):
    """بررسی وضعیت اشتراک و بروزرسانی خودکار"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute('SELECT subscription_end, is_subscribed FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    
    if result:
        expiry_str, is_sub = result
        if expiry_str:
            expiry = datetime.datetime.strptime(expiry_str, '%Y-%m-%d %H:%M:%S')
            now = datetime.datetime.now()
            
            if now > expiry:
                # اشتراک به اتمام رسیده
                c.execute('UPDATE users SET is_subscribed = 0 WHERE user_id = ?', (user_id,))
                conn.commit()
                conn.close()
                return False
            else:
                conn.close()
                return True
    conn.close()
    return False

def get_days_remaining(user_id):
    """محاسبه روزهای باقی مانده از اشتراک"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT subscription_end FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    
    if result and result[0]:
        expiry = datetime.datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
        now = datetime.datetime.now()
        remaining = (expiry - now).days
        return max(0, remaining)
    return 0

# ==================== بررسی عضویت کانال ====================

def is_user_member(user_id):
    try:
        member_status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return member_status in ['member', 'administrator', 'creator']
    except:
        return False

# ==================== منوی اصلی ====================

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

# ==================== دستور /start ====================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "کاربر گرامی"
    username = message.from_user.username or ""
    
    # ثبت یا بروزرسانی کاربر در دیتابیس
    user = get_user(user_id)
    if not user:
        # کاربر جدید - دریافت جایزه اولیه
        add_user(user_id, first_name, username)
    else:
        # بروزرسانی اطلاعات
        update_user_info(user_id, first_name, username)
    
    # بررسی عضویت در کانال
    if is_user_member(user_id):
        # نمایش منوی اصلی
        menu_text = f"""
⫸◄◂ 𝕄𝕖𝕟𝕦 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

✅ به ربات خوش آمدید {first_name} عزیز!

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
        bot.send_message(
            message.chat.id,
            menu_text,
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )
    else:
        # نمایش پیام عضویت اجباری
        welcome_text = f"""
⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

سلام {first_name} عزیز 🌹

⫸◄◂
برای دسترسی به امکانات اختصاصی و دریافت آخرین آپدیت‌های امنیتی، 
نیاز است ابتدا در کانال رسمی ما عضو شوید.
◂◄⫷

📌 عضویت شما در کانال، نه تنها به ما انرژی می‌دهد، 
بلکه از آخرین اخبار و ترفندهای امنیتی نیز باخبرتان می‌کند!

👇 لطفاً پس از عضویت، دکمه «عضو شدم» را بزنید.
⫸◄◂
        """
        
        markup = InlineKeyboardMarkup(row_width=1)
        channel_btn = InlineKeyboardButton("❈ 𝙎𝙚𝙡𝙛 𝙋𝙝𝙖𝙣𝙩𝙤𝙢『𖣘』", url="https://t.me/Phantomupdatess")
        check_btn = InlineKeyboardButton("✅ عضو شدم ( ✓ )", callback_data="check_membership")
        markup.add(channel_btn, check_btn)
        
        bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

# ==================== بررسی عضویت ====================

@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def handle_check_membership(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if is_user_member(user_id):
        # عضویت تأیید شد
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
    
    # بررسی عضویت در کانال
    if not is_user_member(user_id):
        bot.answer_callback_query(
            call.id,
            "⛔ شما از کانال خارج شده‌اید!\nلطفاً دوباره عضو شوید.",
            show_alert=True
        )
        return
    
    # دریافت اطلاعات از دیتابیس
    user = get_user(user_id)
    diamonds = get_user_diamonds(user_id)
    wallet = get_user_wallet(user_id)
    days_left = get_days_remaining(user_id)
    is_subscribed = check_subscription_status(user_id)
    
    # وضعیت اشتراک
    if is_subscribed:
        sub_status = f"✅ فعال ( {days_left} روز باقی مانده )"
    else:
        sub_status = "❌ منقضی شده / فعال نیست"
    
    # متن حساب کاربری
    account_text = f"""
⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

👤 *حساب کاربری*

📌 مشخصات:
┌─────────────────
│ 👤 نام: {call.from_user.first_name}
│ 🆔 آیدی: `{call.from_user.id}`
│ ✅ وضعیت: عضو فعال کانال
│ 📅 تاریخ عضویت: {user[3] if user else 'امروز'}
└─────────────────

💎 الماس: {diamonds}
💳 کیف پول: {wallet:,} تومان

⭐ وضعیت اشتراک:
{sub_status}

⫸◄◂
"""
    
    # دکمه بازگشت
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

# ==================== سایر دکمه‌های منو ====================

@bot.callback_query_handler(func=lambda call: call.data in ["diamond", "wallet", "subscription", "features", "ads", "settings", "support"])
def handle_menu_buttons(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not is_user_member(user_id):
        bot.answer_callback_query(
            call.id,
            "⛔ شما از کانال خارج شده‌اید!",
            show_alert=True
        )
        return
    
    responses = {
        "diamond": f"💎 *الماس*\n\nتعداد الماس شما: {get_user_diamonds(user_id)}\n\n🌟 برای دریافت الماس بیشتر، از بخش اشتراک استفاده کنید.",
        "wallet": f"💳 *کیف پول*\n\nموجودی: {get_user_wallet(user_id):,} تومان\n\n📊 تراکنش‌های اخیر: ندارد",
        "subscription": f"⭐ *اشتراک*\n\nروزهای باقی مانده: {get_days_remaining(user_id)} روز\n\n📌 اشتراک ویژه شامل:\n🔹 الماس روزانه\n🔹 تخفیف ویژه\n🔹 دسترسی به امکانات پیشرفته",
        "features": "🤖 *امکانات*\n\n🔹 ابزارهای امنیتی\n🔹 اسکنر فایل\n🔹 گزارش‌گیری خودکار\n🔹 هشدارهای لحظه‌ای",
        "ads": "📢 *تبلیغات*\n\nبرای تبلیغات در کانال ما، با پشتیبانی تماس بگیرید.\n\n📊 قیمت‌ها:\n🔹 پست عادی: ۱۰۰,۰۰۰ تومان\n🔹 پست ویژه: ۲۵۰,۰۰۰ تومان",
        "settings": "⚙️ *تنظیمات*\n\n🔹 تغییر زبان\n🔹 اعلان‌ها\n🔹 حریم خصوصی\n🔹 تم ربات",
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

# ==================== دکمه بازگشت ====================

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

# ==================== اجرا ====================

if __name__ == "__main__":
    init_db()
    print("🤖 ربات با موفقیت اجرا شد...")
    print("📌 @PhantomSecurityBot")
    print("✅ دیتابیس راه‌اندازی شد")
    bot.infinity_polling()
