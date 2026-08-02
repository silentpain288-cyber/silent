import telebot
import sqlite3
import datetime
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU'
CHANNEL_ID = '@Phantomupdatess'

bot = telebot.TeleBot(TOKEN)

# ==================== دیتابیس ====================

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
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
            first_join INTEGER DEFAULT 1,
            user_number INTEGER
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS diamond_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount INTEGER,
            type TEXT,
            date TEXT,
            status TEXT
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS wallet_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount INTEGER,
            type TEXT,
            description TEXT,
            date TEXT,
            status TEXT
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
    
    today = datetime.datetime.now()
    expiry = today + datetime.timedelta(days=30)
    expiry_str = expiry.strftime('%Y-%m-%d %H:%M:%S')
    
    user_number = random.randint(100000, 999999)
    
    c.execute('''
        INSERT OR IGNORE INTO users 
        (user_id, first_name, username, join_date, subscription_end, diamonds, wallet_balance, is_subscribed, first_join, user_number)
        VALUES (?, ?, ?, ?, ?, 30, 0, 1, 0, ?)
    ''', (user_id, first_name, username, today.strftime('%Y-%m-%d %H:%M:%S'), expiry_str, user_number))
    
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

def get_user_number(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT user_number FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

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

def get_days_remaining(user_id):
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

def check_subscription_status(user_id):
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
                c.execute('UPDATE users SET is_subscribed = 0 WHERE user_id = ?', (user_id,))
                conn.commit()
                conn.close()
                return False
            else:
                conn.close()
                return True
    conn.close()
    return False

def add_diamond_transaction(user_id, amount, type_, status="completed"):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO diamond_transactions (user_id, amount, type, date, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, amount, type_, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), status))
    conn.commit()
    conn.close()

def get_diamond_transactions(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM diamond_transactions WHERE user_id = ? ORDER BY date DESC LIMIT 10', (user_id,))
    result = c.fetchall()
    conn.close()
    return result

def add_wallet_transaction(user_id, amount, type_, description, status="completed"):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO wallet_transactions (user_id, amount, type, description, date, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, amount, type_, description, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), status))
    conn.commit()
    conn.close()

def update_diamonds(user_id, amount):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET diamonds = diamonds + ? WHERE user_id = ?', (amount, user_id))
    conn.commit()
    conn.close()

def update_wallet(user_id, amount):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET wallet_balance = wallet_balance + ? WHERE user_id = ?', (amount, user_id))
    conn.commit()
    conn.close()

# ==================== بررسی عضویت کانال ====================

def is_user_member(user_id):
    try:
        member_status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return member_status in ['member', 'administrator', 'creator']
    except:
        return False

# ==================== قوانین ====================

def rules_text():
    return """
⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

📋 *قوانین استفاده از ربات*

1️⃣ رعایت اخلاق در استفاده از ربات
2️⃣ استفاده از امکانات ربات برای مقاصد قانونی
3️⃣ عدم ارسال هرزنامه و محتوای نامناسب
4️⃣ احترام به سایر کاربران
5️⃣ تخلف از قوانین منجر به مسدودیت می‌شود

✅ با استفاده از ربات، پذیرش قوانین تلقی می‌شود.

⫸◄◂
"""

# ==================== منوی اصلی ====================

def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("👤 حساب کاربری", callback_data="account")
    btn2 = InlineKeyboardButton("💎 الماس", callback_data="diamond")
    btn3 = InlineKeyboardButton("💳 کیف پول", callback_data="wallet")
    btn4 = InlineKeyboardButton("⭐ اشتراک", callback_data="subscription")
    btn5 = InlineKeyboardButton("🤖 امکانات", callback_data="features")
    btn6 = InlineKeyboardButton("📢 تبلیغات", callback_data="ads")
    btn7 = InlineKeyboardButton("🧠 AI", callback_data="ai")
    btn8 = InlineKeyboardButton("⚙️ تنظیمات", callback_data="settings")
    btn9 = InlineKeyboardButton("📞 پشتیبانی", callback_data="support")
    btn10 = InlineKeyboardButton("📋 تعریف سلف", callback_data="self_define")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10)
    return markup

# ==================== دستور /start ====================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "کاربر گرامی"
    username = message.from_user.username or ""
    
    user = get_user(user_id)
    if not user:
        add_user(user_id, first_name, username)
    else:
        update_user_info(user_id, first_name, username)
    
    if is_user_member(user_id):
        # حذف پیام قبلی
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
        
        # خوش‌آمدگویی
        welcome_text = f"""
⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

🌟 به ربات *Self Phantom* خوش آمدید {first_name} عزیز!

🎁 شما دریافت کردید:
💎 ۳۰ الماس هدیه
⭐ ۱ ماه اشتراک رایگان

⫸◄◂
"""
        bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown')
        bot.send_message(message.chat.id, rules_text(), parse_mode='Markdown')
        
        # منوی اصلی
        menu_text = """
⫸◄◂ 𝕄𝕖𝕟𝕦 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

📌 لطفاً یکی از گزینه‌های زیر را انتخاب کنید:

👤 حساب کاربری
💎 الماس  
💳 کیف پول
⭐ اشتراک
🤖 امکانات
📢 تبلیغات
🧠 AI
⚙️ تنظیمات
📞 پشتیبانی
📋 تعریف سلف

⫸◄◂
"""
        bot.send_message(
            message.chat.id,
            menu_text,
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )
    else:
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
        
        bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

# ==================== بررسی عضویت ====================

@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def handle_check_membership(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if is_user_member(user_id):
        # حذف پیام عضویت
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass
        
        # خوش‌آمدگویی
        welcome_text = f"""
⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

🌟 به ربات *Self Phantom* خوش آمدید!

🎁 شما دریافت کردید:
💎 ۳۰ الماس هدیه
⭐ ۱ ماه اشتراک رایگان

⫸◄◂
"""
        bot.send_message(chat_id, welcome_text, parse_mode='Markdown')
        bot.send_message(chat_id, rules_text(), parse_mode='Markdown')
        
        menu_text = """
⫸◄◂ 𝕄𝕖𝕟𝕦 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

📌 لطفاً یکی از گزینه‌های زیر را انتخاب کنید:

👤 حساب کاربری
💎 الماس  
💳 کیف پول
⭐ اشتراک
🤖 امکانات
📢 تبلیغات
🧠 AI
⚙️ تنظیمات
📞 پشتیبانی
📋 تعریف سلف

⫸◄◂
"""
        bot.send_message(
            chat_id,
            menu_text,
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

# ==================== حساب کاربری ====================

@bot.callback_query_handler(func=lambda call: call.data == "account")
def handle_account(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not is_user_member(user_id):
        bot.answer_callback_query(call.id, "⛔ شما از کانال خارج شده‌اید!", show_alert=True)
        return
    
    user = get_user(user_id)
    diamonds = get_user_diamonds(user_id)
    wallet = get_user_wallet(user_id)
    days_left = get_days_remaining(user_id)
    is_subscribed = check_subscription_status(user_id)
    user_number = get_user_number(user_id)
    
    if is_subscribed:
        sub_status = f"✅ فعال ( {days_left} روز باقی مانده )"
    else:
        sub_status = "❌ منقضی شده / فعال نیست"
    
    account_text = f"""
⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

👤 *حساب کاربری*

📌 مشخصات:
┌─────────────────
│ 👤 نام: {call.from_user.first_name}
│ 🆔 شماره کاربر: `{user_number}`
│ 🆔 آیدی تلگرام: `{call.from_user.id}`
│ ✅ وضعیت: عضو فعال کانال
│ 📅 تاریخ عضویت: {user[3] if user else 'امروز'}
└─────────────────

💎 الماس: {diamonds}
💳 کیف پول: {wallet:,} تومان

⭐ وضعیت اشتراک:
{sub_status}

⫸◄◂
"""
    
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

# ==================== الماس ====================

@bot.callback_query_handler(func=lambda call: call.data == "diamond")
def handle_diamond(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not is_user_member(user_id):
        bot.answer_callback_query(call.id, "⛔ شما از کانال خارج شده‌اید!", show_alert=True)
        return
    
    diamonds = get_user_diamonds(user_id)
    
    diamond_text = f"""
⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

💎 *الماس*

موجودی فعلی: {diamonds} الماس

📊 برای خرید الماس، یکی از گزینه‌های زیر را انتخاب کنید:

💰 هر ۱ الماس = ۱,۰۰۰ تومان
حداکثر خرید: ۱۰۰ الماس

⫸◄◂
"""
    
    markup = InlineKeyboardMarkup(row_width=2)
    btn_buy = InlineKeyboardButton("🛒 خرید الماس", callback_data="buy_diamond")
    btn_trans = InlineKeyboardButton("📊 تراکنش‌ها", callback_data="diamond_transactions")
    btn_back = InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_menu")
    markup.add(btn_buy, btn_trans)
    markup.add(btn_back)
    
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text=diamond_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "buy_diamond")
def handle_buy_diamond(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    buy_text = """
💎 *خرید الماس*

تعداد الماس مورد نظر را وارد کنید:

📌 حداقل: ۱ الماس
📌 حداکثر: ۱۰۰ الماس

💰 قیمت: ۱,۰۰۰ تومان = ۱ الماس

👇 عدد مورد نظر را به صورت عددی وارد کنید:
"""
    
    markup = InlineKeyboardMarkup(row_width=1)
    back_btn = InlineKeyboardButton("🔙 بازگشت", callback_data="diamond")
    markup.add(back_btn)
    
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text=buy_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id)
    
    bot.register_next_step_handler(call.message, process_diamond_purchase)

def process_diamond_purchase(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    try:
        amount = int(message.text)
        if 1 <= amount <= 100:
            total_cost = amount * 1000
            wallet = get_user_wallet(user_id)
            
            if wallet >= total_cost:
                update_wallet(user_id, -total_cost)
                update_diamonds(user_id, amount)
                add_diamond_transaction(user_id, amount, "buy")
                
                bot.send_message(
                    chat_id,
                    f"✅ خرید موفق!\n\n💎 {amount} الماس به حساب شما اضافه شد.\n💰 مبلغ: {total_cost:,} تومان از کیف پول کسر شد.",
                    parse_mode='Markdown'
                )
                
                diamonds = get_user_diamonds(user_id)
                diamond_text = f"""
⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

💎 *الماس*

موجودی فعلی: {diamonds} الماس

📊 برای خرید الماس، یکی از گزینه‌های زیر را انتخاب کنید:

💰 هر ۱ الماس = ۱,۰۰۰ تومان
حداکثر خرید: ۱۰۰ الماس

⫸◄◂
"""
                markup = InlineKeyboardMarkup(row_width=2)
                btn_buy = InlineKeyboardButton("🛒 خرید الماس", callback_data="buy_diamond")
                btn_trans = InlineKeyboardButton("📊 تراکنش‌ها", callback_data="diamond_transactions")
                btn_back = InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_menu")
                markup.add(btn_buy, btn_trans)
                markup.add(btn_back)
                
                bot.send_message(
                    chat_id,
                    diamond_text,
                    reply_markup=markup,
                    parse_mode='Markdown'
                )
            else:
                bot.send_message(
                    chat_id,
                    f"⛔ موجودی کیف پول شما کافی نیست!\n\nموجودی: {wallet:,} تومان\nهزینه مورد نیاز: {total_cost:,} تومان",
                    parse_mode='Markdown'
                )
        else:
            bot.send_message(
                chat_id,
                "⛔ تعداد الماس باید بین ۱ تا ۱۰۰ باشد!",
                parse_mode='Markdown'
            )
    except ValueError:
        bot.send_message(
            chat_id,
            "⛔ لطفاً یک عدد معتبر وارد کنید!",
            parse_mode='Markdown'
        )

@bot.callback_query_handler(func=lambda call: call.data == "diamond_transactions")
def handle_diamond_transactions(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    transactions = get_diamond_transactions(user_id)
    
    if transactions:
        trans_text = "📊 *تراکنش‌های الماس*\n\n"
        for trans in transactions[:10]:
            trans_text += f"🔹 {trans[3]}: {trans[2]} الماس - {trans[4]}\n"
    else:
        trans_text = "📊 *تراکنش‌های الماس*\n\nهیچ تراکنشی یافت نشد."
    
    markup = InlineKeyboardMarkup(row_width=1)
    back_btn = InlineKeyboardButton("🔙 بازگشت", callback_data="diamond")
    markup.add(back_btn)
    
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text=trans_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id)

# ==================== کیف پول ====================

@bot.callback_query_handler(func=lambda call: call.data == "wallet")
def handle_wallet(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not is_user_member(user_id):
        bot.answer_callback_query(call.id, "⛔ شما از کانال خارج شده‌اید!", show_alert=True)
        return
    
    wallet = get_user_wallet(user_id)
    user_number = get_user_number(user_id)
    
    wallet_text = f"""
⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

💳 *کیف پول*

💰 موجودی: {wallet:,} تومان

🆔 شماره کاربر: `{user_number}`

📌 برای شارژ یا برداشت، یکی از گزینه‌های زیر را انتخاب کنید:

⫸◄◂
"""
    
    markup = InlineKeyboardMarkup(row_width=2)
    btn_deposit = InlineKeyboardButton("💰 شارژ کیف پول", callback_data="deposit_wallet")
    btn_withdraw = InlineKeyboardButton("🏦 برداشت", callback_data="withdraw_wallet")
    btn_back = InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_menu")
    markup.add(btn_deposit, btn_withdraw)
    markup.add(btn_back)
    
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text=wallet_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "deposit_wallet")
def handle_deposit_wallet(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    user_number = get_user_number(user_id)
    
    deposit_text = f"""
💰 *شارژ کیف پول*

📋 برای شارژ کیف پول، مبلغ مورد نظر را به شماره کارت زیر واریز کنید:

🏦 شماره کارت: `6037-9918-1234-5678`
👤 صاحب حساب: *Self Phantom*

📌 مبلغ مورد نظر را به تومان وارد کنید:

🆔 شماره کاربر: `{user_number}`

⚠️ پس از واریز، رسید را به پشتیبانی ارسال کنید.

⫸◄◂
"""
    
    markup = InlineKeyboardMarkup(row_width=1)
    back_btn = InlineKeyboardButton("🔙 بازگشت", callback_data="wallet")
    markup.add(back_btn)
    
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text=deposit_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id)
    
    bot.register_next_step_handler(call.message, process_deposit)

def process_deposit(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    try:
        amount = int(message.text)
        if amount > 0:
            bot.send_message(
                chat_id,
                f"✅ درخواست شارژ {amount:,} تومان ثبت شد!\n\n📋 لطفاً مبلغ را به شماره کارت زیر واریز کنید:\n🏦 `6037-9918-1234-5678`\n\n🆔 شماره کاربر: `{get_user_number(user_id)}`\n\n⚠️ پس از واریز، رسید را به پشتیبانی ارسال کنید تا کیف پول شما شارژ شود.",
                parse_mode='Markdown'
            )
        else:
            bot.send_message(
                chat_id,
                "⛔ لطفاً یک عدد مثبت وارد کنید!",
                parse_mode='Markdown'
            )
    except ValueError:
        bot.send_message(
            chat_id,
            "⛔ لطفاً یک عدد معتبر وارد کنید!",
            parse_mode='Markdown'
        )

@bot.callback_query_handler(func=lambda call: call.data == "withdraw_wallet")
def handle_withdraw_wallet(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    withdraw_text = """
🏦 *برداشت از کیف پول*

📌 مبلغ مورد نظر برای برداشت را وارد کنید:

⚠️ حداقل برداشت: ۱۰,۰۰۰ تومان
💰 کارمزد برداشت: ۵٪

📋 پس از تایید، مبلغ به شماره کارت شما واریز می‌شود.

👇 عدد مورد نظر را وارد کنید:
"""
    
    markup = InlineKeyboardMarkup(row_width=1)
    back_btn = InlineKeyboardButton("🔙 بازگشت", callback_data="wallet")
    markup.add(back_btn)
    
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text=withdraw_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id)
    
    bot.register_next_step_handler(call.message, process_withdraw)

def process_withdraw(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    try:
        amount = int(message.text)
        if amount >= 10000:
            wallet = get_user_wallet(user_id)
            fee = int(amount * 0.05)
            total = amount + fee
            
            if wallet >= total:
                update_wallet(user_id, -total)
                add_wallet_transaction(user_id, amount, "withdraw", f"برداشت {amount:,} تومان (کارمزد: {fee:,})")
                
                bot.send_message(
                    chat_id,
                    f"✅ درخواست برداشت ثبت شد!\n\n💰 مبلغ: {amount:,} تومان\n💸 کارمزد: {fee:,} تومان\n📌 مبلغ واریزی: {amount:,} تومان\n\n🕘 حداکثر ۲۴ ساعت کاری واریز می‌شود.",
                    parse_mode='Markdown'
                )
            else:
                bot.send_message(
                    chat_id,
                    f"⛔ موجودی کیف پول شما کافی نیست!\n\nموجودی: {wallet:,} تومان\nمبلغ مورد نیاز: {total:,} تومان",
                    parse_mode='Markdown'
                )
        else:
            bot.send_message(
                chat_id,
                "⛔ حداقل مبلغ برداشت ۱۰,۰۰۰ تومان است!",
                parse_mode='Markdown'
            )
    except ValueError:
        bot.send_message(
            chat_id,
            "⛔ لطفاً یک عدد معتبر وارد کنید!",
            parse_mode='Markdown'
        )

# ==================== اشتراک ====================

@bot.callback_query_handler(func=lambda call: call.data == "subscription")
def handle_subscription(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not is_user_member(user_id):
        bot.answer_callback_query(call.id, "⛔ شما از کانال خارج شده‌اید!", show_alert=True)
        return
    
    days_left = get_days_remaining(user_id)
    is_subscribed = check_subscription_status(user_id)
    
    if is_subscribed:
        status_text = f"✅ فعال ( {days_left} روز باقی مانده )"
    else:
        status_text = "❌ منقضی شده / فعال نیست"
    
    sub_text = f"""
⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

⭐ *اشتراک ویژه*

وضعیت فعلی: {status_text}

📌 پلن‌های اشتراک:

┌─────────────────────────
│ 📦 *پلن ۱ ماهه* 🌙
│ 💰 ۵۰,۰۰۰ تومان
│ 🎁 ۳۰ الماس هدیه
└─────────────────────────

┌─────────────────────────
│ 📦 *پلن ۳ ماهه* 📅
│ 💰 ۱۲۰,۰۰۰ تومان
│ 🎁 ۱۰۰ الماس هدیه
└─────────────────────────

┌─────────────────────────
│ 📦 *پلن ۶ ماهه* 📆
│ 💰 ۲۰۰,۰۰۰ تومان
│ 🎁 ۲۵۰ الماس هدیه
└─────────────────────────

👇 برای خرید، عدد پلن مورد نظر را وارد کنید:
۱ = ۱ ماهه
۲ = ۳ ماهه
۳ = ۶ ماهه

⫸◄◂
"""
    
    markup = InlineKeyboardMarkup(row_width=1)
    back_btn = InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_menu")
    markup.add(back_btn)
    
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text=sub_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id)
    
    bot.register_next_step_handler(call.message, process_subscription_purchase)

def process_subscription_purchase(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    plans = {
        "1": {"month": 1, "price": 50000, "diamonds": 30, "name": "۱ ماهه"},
        "2": {"month": 3, "price": 120000, "diamonds": 100, "name": "۳ ماهه"},
        "3": {"month": 6, "price": 200000, "diamonds": 250, "name": "۶ ماهه"}
    }
    
    choice = message.text.strip()
    
    if choice in plans:
        plan = plans[choice]
        wallet = get_user_wallet(user_id)
        
        if wallet >= plan["price"]:
            update_wallet(user_id, -plan["price"])
            update_diamonds(user_id, plan["diamonds"])
            
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            
            now = datetime.datetime.now()
            new_expiry = now + datetime.timedelta(days=plan["month"] * 30)
            new_expiry_str = new_expiry.strftime('%Y-%m-%d %H:%M:%S')
            
            c.execute('''
                UPDATE users 
                SET subscription_end = ?, is_subscribed = 1
                WHERE user_id = ?
            ''', (new_expiry_str, user_id))
            conn.commit()
            conn.close()
            
            add_wallet_transaction(user_id, plan["price"], "subscription", f"خرید اشتراک {plan['name']}")
            
            bot.send_message(
                chat_id,
                f"✅ اشتراک با موفقیت خریداری شد!\n\n⭐ پلن: {plan['name']}\n💎 {plan['diamonds']} الماس هدیه\n📅 تاریخ انقضا: {new_expiry.strftime('%Y-%m-%d')}\n💰 مبلغ: {plan['price']:,} تومان",
                parse_mode='Markdown'
            )
        else:
            bot.send_message(
                chat_id,
                f"⛔ موجودی کیف پول شما کافی نیست!\n\nموجودی: {wallet:,} تومان\nهزینه: {plan['price']:,} تومان",
                parse_mode='Markdown'
            )
    else:
        bot.send_message(
            chat_id,
            "⛔ لطفاً عدد ۱، ۲ یا ۳ را وارد کنید!",
            parse_mode='Markdown'
        )

# ==================== تبلیغات ====================

@bot.callback_query_handler(func=lambda call: call.data == "ads")
def handle_ads(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not is_user_member(user_id):
        bot.answer_callback_query(call.id, "⛔ شما از کانال خارج شده‌اید!", show_alert=True)
        return
    
    ads_text = """
⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

📢 *تبلیغات در کانال*

📊 پکیج‌های تبلیغاتی:

┌─────────────────────────
│ 📦 *پکیج ۱ ماهه*
│ 📌 ۴ تبلیغ
│ 💰 ۱۵۰,۰۰۰ تومان
│ ✅ مناسب برای شروع
└─────────────────────────

┌─────────────────────────
│ 📦 *پکیج ۲ ماهه*
│ 📌 ۶ تبلیغ
│ 💰 ۳۷۰,۰۰۰ تومان
│ ✅ تخفیف ویژه
└─────────────────────────

┌─────────────────────────
│ 📦 *پکیج ۴ ماهه*
│ 📌 ۹ تبلیغ
│ 💰 ۷۰۰,۰۰۰ تومان
│ ✅ بهترین ارزش
└─────────────────────────

📌 برای سفارش، با پشتیبانی تماس بگیرید.

⫸◄◂
"""
    
    markup = InlineKeyboardMarkup(row_width=1)
    btn_contact = InlineKeyboardButton("📞 تماس با پشتیبانی", callback_data="support")
    btn_back = InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_menu")
    markup.add(btn_contact, btn_back)
    
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text=ads_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id)

# ==================== امکانات (خالی) ====================

@bot.callback_query_handler(func=lambda call: call.data == "features")
def handle_features(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not is_user_member(user_id):
        bot.answer_callback_query(call.id, "⛔ شما از کانال خارج شده‌اید!", show_alert=True)
        return
    
    features_text = """
⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

🤖 *امکانات*

🔹 به زودی...

⫸◄◂
"""
    
    markup = InlineKeyboardMarkup(row_width=1)
    back_btn = InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_menu")
    markup.add(back_btn)
    
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text=features_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id)

# ==================== AI ====================

@bot.callback_query_handler(func=lambda call: call.data == "ai")
def handle_ai(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not is_user_member(user_id):
        bot.answer_callback_query(call.id, "⛔ شما از کانال خارج شده‌اید!", show_alert=True)
        return
    
    ai_text = """
⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

🧠 *AI هوشمند*

⚡ این بخش به زودی اضافه می‌شود!

🔜 منتظر آپدیت‌های بعدی باشید.

⫸◄◂
"""
    
    markup = InlineKeyboardMarkup(row_width=1)
    back_btn = InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_menu")
    markup.add(back_btn)
    
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text=ai_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id)

# ==================== تنظیمات (خالی) ====================

@bot.callback_query_handler(func=lambda call: call.data == "settings")
def handle_settings(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not is_user_member(user_id):
        bot.answer_callback_query(call.id, "⛔ شما از کانال خارج شده‌اید!", show_alert=True)
        return
    
    settings_text = """
⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

⚙️ *تنظیمات*

🔹 به زودی...

⫸◄◂
"""
    
    markup = InlineKeyboardMarkup(row_width=1)
    back_btn = InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_menu")
    markup.add(back_btn)
    
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text=settings_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id)

# ==================== پشتیبانی ====================

@bot.callback_query_handler(func=lambda call: call.data == "support")
def handle_support(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    support_text = """
⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

📞 *پشتیبانی*

برای ارتباط با پشتیبانی:

📧 @PhantomSupport
🕘 پاسخگویی ۲۴/۷

📌 سوالات متداول:
🔹 سوال ۱: ...
🔹 سوال ۲: ...

⫸◄◂
"""
    
    markup = InlineKeyboardMarkup(row_width=1)
    back_btn = InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_menu")
    markup.add(back_btn)
    
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text=support_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id)

# ==================== تعریف سلف (خالی) ====================

@bot.callback_query_handler(func=lambda call: call.data == "self_define")
def handle_self_define(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not is_user_member(user_id):
        bot.answer_callback_query(call.id, "⛔ شما از کانال خارج شده‌اید!", show_alert=True)
        return
    
    self_text = """
⫸◄◂ 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

📋 *تعریف سلف*

🔹 به زودی...

⫸◄◂
"""
    
    markup = InlineKeyboardMarkup(row_width=1)
    back_btn = InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_menu")
    markup.add(back_btn)
    
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text=self_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id)

# ==================== بازگشت به منو ====================

@bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
def handle_back_to_menu(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not is_user_member(user_id):
        bot.answer_callback_query(call.id, "⛔ شما از کانال خارج شده‌اید!", show_alert=True)
        return
    
    menu_text = """
⫸◄◂ 𝕄𝕖𝕟𝕦 𝕊𝕖𝕝𝕗 ℙ𝕙𝕒𝕟𝕥𝕠𝕞 ◂◄⫷

📌 لطفاً یکی از گزینه‌های زیر را انتخاب کنید:

👤 حساب کاربری
💎 الماس  
💳 کیف پول
⭐ اشتراک
🤖 امکانات
📢 تبلیغات
🧠 AI
⚙️ تنظیمات
📞 پشتیبانی
📋 تعریف سلف

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
