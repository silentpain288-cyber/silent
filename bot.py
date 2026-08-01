import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# توکن ربات شما
TOKEN = "8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU"
CHANNEL_LINK = "https://t.me/+NnHHB5BhE785OTRk"

bot = AsyncTeleBot(TOKEN)

# دکمه‌های زیبا با خطوط دورن
def create_buttons():
    markup = InlineKeyboardMarkup(row_width=1)
    
    # دکمه اول - عضویت در کانال
    btn_channel = InlineKeyboardButton(
        text="❈ 𝙎𝙚𝙡𝙛 𝙋𝙝𝙖𝙣𝙩𝙤𝙢『𖣘』",
        url=CHANNEL_LINK
    )
    
    # دکمه دوم - بررسی عضویت
    btn_check = InlineKeyboardButton(
        text="✅ عضو شدم ( ✓ )",
        callback_data="check_membership"
    )
    
    markup.add(btn_channel, btn_check)
    return markup

@bot.message_handler(commands=['start'])
async def send_welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "کاربر عزیز"
    
    # متن زیبا و حرفه‌ای با استفاده از کاراکترهای ویژه
    welcome_text = f"""
◄━━━━━━━━━━━━━━━━━━━►
    ✦ 𝙋𝙝𝙖𝙣𝙩𝙤𝙢 𝘽𝙤𝙩 ✦
◄━━━━━━━━━━━━━━━━━━━►

⫸ سلام {user_name} عزیز! ⫷

⫸ برای استفاده از خدمات ویژه ما ✦

⫸ ابتدا باید در کانال اختصاصی ما عضو بشی ✦

⫸ پس از عضویت، دکمه "عضو شدم" رو بزن ✦

◄━━━━━━━━━━━━━━━━━━━►
    ❈ 𝙎𝙚𝙡𝙛 𝙋𝙝𝙖𝙣𝙩𝙤𝙢『𖣘』
◄━━━━━━━━━━━━━━━━━━━►

⫷ منتظرت هستیم! ✦
"""
    
    await bot.send_message(
        user_id,
        welcome_text,
        reply_markup=create_buttons(),
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
async def check_membership(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    # در اینجا می‌تونید کد بررسی عضویت رو اضافه کنید
    # مثلاً با استفاده از get_chat_member
    
    await bot.answer_callback_query(
        call.id,
        text="✅ عضویت شما تایید شد! به جمع ما خوش اومدی 🎉",
        show_alert=True
    )
    
    # پیام تبریک بعد از تایید عضویت
    success_text = """
◄━━━━━━━━━━━━━━━━━━━►
    ✨ تبریک! ✨
◄━━━━━━━━━━━━━━━━━━━►

⫸ عضویت شما با موفقیت تایید شد! ⫷

⫸ حالا می‌تونی از تمام خدمات ما استفاده کنی ✦

⫸ خوشحالیم که در جمع مایی ✦

◄━━━━━━━━━━━━━━━━━━━►
    ❈ 𝙎𝙚𝙡𝙛 𝙋𝙝𝙖𝙣𝙩𝙤𝙢『𖣘』
◄━━━━━━━━━━━━━━━━━━━►
"""
    await bot.send_message(
        chat_id,
        success_text,
        parse_mode='HTML'
    )

async def main():
    logger.info("ربات با موفقیت راه‌اندازی شد!")
    await bot.polling()

if __name__ == "__main__":
    asyncio.run(main())
