# -*- coding: utf-8 -*-
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ ربات کار می‌کند!")

def main():
    logger.info("🚀 ربات در حال راه‌اندازی...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    logger.info("✅ ربات روشن شد!")
    app.run_polling()

if __name__ == "__main__":
    main()
