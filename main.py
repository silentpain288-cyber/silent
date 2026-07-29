# main.py
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from config import *
from utils.database import init_db, load_data, save_data
from handlers.start import setup_handlers

# ایجاد نمونه ربات
bot = telebot.TeleBot(BOT_TOKEN)

# مقداردهی اولیه دیتابیس
init_db()

# تنظیم هندلرها
setup_handlers(bot)

# ==================== بخش منوی اصلی ====================
@bot.message_handler(func=lambda message: message.text == "👤 پروفایل")
def profile_menu(message):
    user_id = message.from_user.id
    data = load_data("users.json")
    user_data = data["users"].get(str(user_id), {})
    
    if not user_data:
        bot.reply_to(message, "❌ لطفاً ابتدا ثبت‌نام کنید! /start")
        return
    
    # محاسبه وضعیت اشتراک
    is_trial = False
    trial_days_left = 0
    if user_data.get("trial_end"):
        trial_end = datetime.fromisoformat(user_data["trial_end"])
        now = datetime.now()
        if now < trial_end:
            is_trial = True
            trial_days_left = (trial_end - now).days
    
    is_premium = user_data.get("is_premium", False)
    premium_expire = user_data.get("premium_expire")
    premium_days_left = 0
    if premium_expire:
        prem_end = datetime.fromisoformat(premium_expire)
        if datetime.now() < prem_end:
            premium_days_left = (prem_end - datetime.now()).days
    
    profile_text = (
        "👤 **پروفایل کاربری**\n"
        "━━━━━━━━━━━━━━━\n"
        f"🆔 **آیدی:** `{user_id}`\n"
        f"📱 **شماره:** {user_data.get('phone', 'نامشخص')}\n"
        f"📅 **تاریخ ثبت:** {user_data.get('register_date', 'نامشخص')[:10]}\n"
        "━━━━━━━━━━━━━━━\n"
        f"💎 **الماس:** {user_data.get('diamonds', {}).get('total', 0)}\n"
        f"💰 **موجودی:** {user_data.get('wallet', {}).get('balance', 0)} تومان\n"
        "━━━━━━━━━━━━━━━\n"
        "⭐ **وضعیت اشتراک:**\n"
    )
    
    if is_premium and premium_days_left > 0:
        profile_text += f"✅ **Premium** ({premium_days_left} روز باقی‌مانده)\n"
    elif is_trial:
        profile_text += f"⏳ **Trial** ({trial_days_left} روز باقی‌مانده)\n"
    else:
        profile_text += "❌ **رایگان** (برای خرید اشتراک اقدام کنید)\n"
    
    profile_text += "━━━━━━━━━━━━━━━"
    
    bot.reply_to(message, profile_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == "💎 الماس")
def diamonds_menu(message):
    user_id = message.from_user.id
    data = load_data("users.json")
    user_data = data["users"].get(str(user_id), {})
    
    if not user_data:
        bot.reply_to(message, "❌ لطفاً ابتدا ثبت‌نام کنید! /start")
        return
    
    diamonds = user_data.get("diamonds", {})
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_buy = InlineKeyboardButton("🛒 خرید الماس", callback_data="buy_diamonds")
    btn_use = InlineKeyboardButton("💎 استفاده از الماس", callback_data="use_diamonds")
    keyboard.add(btn_buy, btn_use)
    
    text = (
        "💎 **اطلاعات الماس**\n"
        "━━━━━━━━━━━━━━━\n"
        f"🎁 الماس هدیه: {diamonds.get('gift', 0)}\n"
        f"🛒 الماس خریداری: {diamonds.get('purchased', 0)}\n"
        "━━━━━━━━━━━━━━━\n"
        f"💎 مجموع الماس: {diamonds.get('total', 0)}\n"
        "━━━━━━━━━━━━━━━\n"
        f"💰 قیمت هر الماس: {DIAMOND_PRICE:,} تومان\n\n"
        "از دکمه‌های زیر استفاده کنید:"
    )
    bot.reply_to(message, text, reply_markup=keyboard, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "buy_diamonds")
def buy_diamonds_callback(call):
    keyboard = InlineKeyboardMarkup(row_width=3)
    amounts = [5, 10, 20, 50, 100, 200]
    for amount in amounts:
        price = amount * DIAMOND_PRICE
        keyboard.add(InlineKeyboardButton(f"{amount} 💎 = {price:,} تومان", callback_data=f"buy_diamond_{amount}"))
    keyboard.add(InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_diamonds"))
    
    bot.edit_message_text(
        "🛒 **خرید الماس**\n\n"
        "تعداد الماس مورد نظر را انتخاب کنید:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_diamond_"))
def confirm_diamond_purchase(call):
    amount = int(call.data.split("_")[2])
    price = amount * DIAMOND_PRICE
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_confirm = InlineKeyboardButton("✅ تایید خرید", callback_data=f"confirm_diamond_{amount}")
    btn_cancel = InlineKeyboardButton("❌ انصراف", callback_data="back_to_diamonds")
    keyboard.add(btn_confirm, btn_cancel)
    
    bot.edit_message_text(
        f"🛒 **تایید خرید**\n\n"
        f"تعداد: {amount} 💎\n"
        f"مبلغ: {price:,} تومان\n\n"
        "آیا از خرید خود مطمئن هستید؟",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "back_to_diamonds")
def back_to_diamonds(call):
    # بازگشت به منوی الماس
    diamonds_menu(call.message)
    bot.answer_callback_query(call.id)

# ==================== اجرای ربات ====================
if __name__ == "__main__":
    print("=" * 60)
    print("🤖 Ghost Assistant فعال شد!")
    print(f"📌 کانال: {CHANNEL_ID}")
    print(f"💎 قیمت هر الماس: {DIAMOND_PRICE:,} تومان")
    print("=" * 60)
    print("⏳ منتظر پیام‌ها هستم...")
    
    try:
        bot.infinity_polling(skip_pending=True)
    except KeyboardInterrupt:
        print("\n⏹️ ربات متوقف شد.")
    except Exception as e:
        print(f"❌ خطا: {e}")
