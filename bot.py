# -*- coding: utf-8 -*-
"""
ربات ساده تلگرام - نسخه تست
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# تنظیمات
TOKEN = "8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU"
ADMIN_ID = "8961040480"

# لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== دستورات ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور start"""
    user = update.effective_user
    name = user.first_name or user.username or 'کاربر'
    
    keyboard = [
        [InlineKeyboardButton("💎 الماس", callback_data="diamonds"),
         InlineKeyboardButton("⭐ پریمیوم", callback_data="premium")],
        [InlineKeyboardButton("💰 کیف پول", callback_data="wallet"),
         InlineKeyboardButton("👤 پروفایل", callback_data="profile")],
        [InlineKeyboardButton("📞 پشتیبانی", callback_data="support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f"""
🎉 سلام {name} عزیز!

به ربات خوش آمدید.
از منوی زیر استفاده کنید.
"""
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور menu"""
    keyboard = [
        [InlineKeyboardButton("💎 الماس", callback_data="diamonds"),
         InlineKeyboardButton("⭐ پریمیوم", callback_data="premium")],
        [InlineKeyboardButton("💰 کیف پول", callback_data="wallet"),
         InlineKeyboardButton("👤 پروفایل", callback_data="profile")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📋 *منوی اصلی*", reply_markup=reply_markup, parse_mode='Markdown')

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور profile"""
    user = update.effective_user
    text = f"""
👤 *پروفایل*

🆔 شناسه: {user.id}
👤 نام: {user.first_name or 'نامشخص'}
🆔 یوزرنیم: @{user.username or 'ندارد'}
📅 عضو از: {user.date_joined.strftime('%Y/%m/%d') if hasattr(user, 'date_joined') else 'نامشخص'}
"""
    await update.message.reply_text(text, parse_mode='Markdown')

async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور wallet"""
    text = """
💰 *کیف پول*

💎 الماس: 0
💰 موجودی: 0 تومان

هنوز تراکنشی ثبت نشده است.
"""
    await update.message.reply_text(text, parse_mode='Markdown')

async def diamonds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور diamonds"""
    keyboard = [
        [InlineKeyboardButton("۱۰ 💎 ۸۰,۰۰۰ت", callback_data="buy_10"),
         InlineKeyboardButton("۵۰ 💎 ۳۵۰,۰۰۰ت", callback_data="buy_50")],
        [InlineKeyboardButton("۱۰۰ 💎 ۶۵۰,۰۰۰ت", callback_data="buy_100"),
         InlineKeyboardButton("۵۰۰ 💎 ۲,۸۰۰,۰۰۰ت", callback_data="buy_500")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("💎 *خرید الماس*\nلطفاً پکیج مورد نظر را انتخاب کنید:", reply_markup=reply_markup, parse_mode='Markdown')

async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور premium"""
    keyboard = [
        [InlineKeyboardButton("۱ ماه (۴۰💎)", callback_data="premium_1")],
        [InlineKeyboardButton("۳ ماه (۱۰۰💎)", callback_data="premium_3")],
        [InlineKeyboardButton("۶ ماه (۱۸۰💎)", callback_data="premium_6")],
        [InlineKeyboardButton("۱ سال (۳۰۰💎)", callback_data="premium_12")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("⭐ *اشتراک پریمیوم*\nلطفاً پلن مورد نظر را انتخاب کنید:", reply_markup=reply_markup, parse_mode='Markdown')

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور support"""
    text = """
📞 *پشتیبانی*

🆔 پشتیبانی: @XMrHadi
👥 گروه: https://t.me/+9-hhQFaMoiAwYjc0
📢 کانال: https://t.me/+NnHHB5BhE785OTRk

ساعت پاسخگویی: ۹ صبح تا ۱۱ شب
"""
    await update.message.reply_text(text, parse_mode='Markdown')

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور cancel"""
    context.user_data.clear()
    await update.message.reply_text("✅ عملیات لغو شد.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور help"""
    text = """
📚 *راهنما*

/start - شروع و منوی اصلی
/menu - منوی اصلی
/profile - پروفایل کاربری
/wallet - کیف پول
/diamonds - خرید الماس
/premium - اشتراک پریمیوم
/support - پشتیبانی
/help - راهنما
/cancel - لغو عملیات
"""
    await update.message.reply_text(text, parse_mode='Markdown')

# ==================== Callback ====================

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت دکمه‌ها"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "diamonds":
        await diamonds(update, context)
    elif data == "premium":
        await premium(update, context)
    elif data == "wallet":
        await wallet(update, context)
    elif data == "profile":
        await profile(update, context)
    elif data == "support":
        await support(update, context)
    elif data.startswith("buy_"):
        amount = data.split("_")[1]
        await query.edit_message_text(f"✅ درخواست خرید {amount} الماس ثبت شد.\nلطفاً منتظر بمانید...")
    elif data.startswith("premium_"):
        plan = data.split("_")[1]
        plans = {"1": "۱ ماه", "3": "۳ ماه", "6": "۶ ماه", "12": "۱ سال"}
        await query.edit_message_text(f"✅ درخواست خرید {plans.get(plan, plan)} ثبت شد.\nلطفاً منتظر بمانید...")

# ==================== خطاها ====================

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت خطاها"""
    logger.error(f"خطا: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text("❌ خطایی رخ داد. لطفاً دوباره تلاش کنید.")

# ==================== اجرا ====================

def main():
    """اجرای اصلی"""
    print("🚀 ربات در حال راه‌اندازی...")
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # ثبت دستورات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("wallet", wallet))
    app.add_handler(CommandHandler("diamonds", diamonds))
    app.add_handler(CommandHandler("premium", premium))
    app.add_handler(CommandHandler("support", support))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("cancel", cancel))
    
    # دکمه‌ها
    app.add_handler(CallbackQueryHandler(callback))
    
    # خطاها
    app.add_error_handler(error_handler)
    
    print("✅ ربات روشن شد!")
    app.run_polling()

if __name__ == "__main__":
    main()
