# -*- coding: utf-8 -*-
"""
ربات ساده تلگرام - نسخه با خطایابی کامل
"""

import logging
import traceback
import sys

# تنظیم لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

TOKEN = "8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU"

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
    logger.info("✅ کتابخانه telegram با موفقیت وارد شد")
except Exception as e:
    logger.error(f"❌ خطا در وارد کردن کتابخانه telegram: {e}")
    raise

# ==================== دستورات ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        name = user.first_name or user.username or 'کاربر'
        
        keyboard = [
            [InlineKeyboardButton("💎 الماس", callback_data="diamonds"),
             InlineKeyboardButton("⭐ پریمیوم", callback_data="premium")],
            [InlineKeyboardButton("💰 کیف پول", callback_data="wallet"),
             InlineKeyboardButton("👤 پروفایل", callback_data="profile")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = f"🎉 سلام {name} عزیز!\nبه ربات خوش آمدید."
        await update.message.reply_text(text, reply_markup=reply_markup)
        logger.info(f"✅ start برای {user.id} اجرا شد")
    except Exception as e:
        logger.error(f"❌ خطا در start: {e}")
        await update.message.reply_text("❌ خطایی رخ داد")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        keyboard = [
            [InlineKeyboardButton("💎 الماس", callback_data="diamonds"),
             InlineKeyboardButton("⭐ پریمیوم", callback_data="premium")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("📋 منوی اصلی", reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"❌ خطا در menu: {e}")

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(f"✅ انتخاب شما: {query.data}")
    except Exception as e:
        logger.error(f"❌ خطا در callback: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"❌ خطا: {context.error}")
    logger.error(traceback.format_exc())
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text("❌ خطا! دوباره تلاش کنید.")
        except:
            pass

# ==================== اجرا ====================

def main():
    try:
        logger.info("🚀 ربات در حال راه‌اندازی...")
        
        # ساخت اپلیکیشن
        app = ApplicationBuilder().token(TOKEN).build()
        logger.info("✅ اپلیکیشن ساخته شد")
        
        # ثبت دستورات
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("menu", menu))
        app.add_handler(CallbackQueryHandler(callback))
        app.add_error_handler(error_handler)
        logger.info("✅ هندلرها ثبت شدند")
        
        # اجرا
        logger.info("✅ ربات روشن شد! در حال Polling...")
        app.run_polling()
        
    except Exception as e:
        logger.error(f"❌ خطای اصلی: {e}")
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    main()
