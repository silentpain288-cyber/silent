from telebot.apihelper import ApiTelegramException

@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
async def check_membership(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    try:
        # بررسی عضویت در کانال
        # آیدی عددی کانال را جایگزین کنید
        CHANNEL_ID = "@your_channel_username"  # یا آیدی عددی مثل -1001234567890
        
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        
        if member.status in ['member', 'administrator', 'creator']:
            await bot.answer_callback_query(
                call.id,
                text="✅ عضویت شما تایید شد! به جمع ما خوش اومدی 🎉",
                show_alert=True
            )
            # ارسال پیام تبریک
            await bot.send_message(
                chat_id,
                "✨ تبریک! عضویت شما با موفقیت تایید شد! ✨"
            )
        else:
            await bot.answer_callback_query(
                call.id,
                text="❌ شما هنوز عضو کانال نشدید! لطفاً ابتدا عضو شوید.",
                show_alert=True
            )
            
    except ApiTelegramException as e:
        if "user not found" in str(e).lower():
            await bot.answer_callback_query(
                call.id,
                text="❌ شما هنوز عضو کانال نشدید! لطفاً ابتدا عضو شوید.",
                show_alert=True
            )
        else:
            logger.error(f"خطا در بررسی عضویت: {e}")
            await bot.answer_callback_query(
                call.id,
                text="⚠️ خطایی رخ داد. لطفاً دوباره تلاش کنید.",
                show_alert=True
            )
