# test.py
import telebot

TOKEN = "8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def test_start(message):
    bot.reply_to(message, "✅ ربات کار می‌کند! اگر این پیام را می‌بینید، همه چیز سالم است.")

print("🤖 ربات تست در حال اجرا...")
print("📱 به ربات بروید و /start را بزنید")

try:
    bot.infinity_polling(skip_pending=True)
except Exception as e:
    print(f"❌ خطا: {e}")
