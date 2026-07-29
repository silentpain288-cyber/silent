# -*- coding: utf-8 -*-
"""
ساده‌ترین ربات برای تست Railway
"""

import logging

# تنظیم لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU"

logger.info("🚀 مرحله 1: شروع ربات...")

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes
    logger.info("✅ مرحله 2: کتابخانه‌ها با موفقیت وارد شدند")
except Exception as e:
    logger.error(f"❌ مرحله 2: خطا در وارد کردن کتابخانه‌ها: {e}")
    raise

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"📩 دریافت start از {update.effective_user.id}")
    await update.message.reply_text("✅ ربات کار می‌کند!")

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"📩 دریافت test از {update.effective_user.id}")
    await update.message.reply_text("✅ تست موفق!")

def main():
    logger.info("🚀 مرحله 3: در حال ساخت اپلیکیشن...")
    
    try:
        app = Application.builder().token(TOKEN).build()
        logger.info("✅ مرحله 4: اپلیکیشن ساخته شد")
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("test", test))
        logger.info("✅ مرحله 5: هندلرها ثبت شدند")
        
        logger.info("✅ مرحله 6: ربات روشن شد! در حال Polling...")
        app.run_polling()
        
    except Exception as e:
        logger.error(f"❌ مرحله 6: خطای اصلی: {e}")
        raise

if __name__ == "__main__":
    main()
