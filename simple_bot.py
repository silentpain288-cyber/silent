# simple_bot.py
import telebot

TOKEN = "8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ سلام! ربات کار می‌کند!")

print("🤖 ربات ساده در حال اجرا...")
bot.infinity_polling()
