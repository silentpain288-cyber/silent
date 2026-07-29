from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8961040480:AAHNKEnK7LZuCp9fSJ5td2_XdGFqPtwp_dY"
CHANNEL_USERNAME = "@ReaperSelfChannel"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_mention = f"@{update.effective_user.username}" if update.effective_user.username else update.effective_user.first_name
    
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        
        if chat_member.status in ["member", "administrator", "creator"]:
            # کاربر عضو است
            text = (
                "<b>༒『忍』𝕹𝕴𝕹𝕵𝕬『忍』༒</b>\n"
                "<b>/start</b>\n\n"
                "<b>❈ 𝙎𝙚𝙡𝙛 𝙋𝙝𝙖𝙣𝙩𝙤𝙢『𖣘』:</b>\n"
                "<b>✅ عضویت تأیید شد!</b>\n"
                "<b>اکنون به تمام امکانات ربات دسترسی داری 😉</b>\n\n"
                "<b>🔗 کانال: @Phantomupdatess</b>"
            )
            
            await update.message.reply_text(
                text,
                parse_mode='HTML'
            )
            return
    except:
        pass
    
    # کاربر عضو نیست
    text = (
        "<b>⫸ برای دسترسی به خدمات ما، ابتدا باید در کانال زیر عضو شوید.</b>\n"
        "<b>◄ پس از عضویت، روی دکمه‌ی «عضو شدم» کلیک کنید.</b>"
    )
    
    keyboard = [
        [InlineKeyboardButton("ریپر سلف Reaper Self", url="https://t.me/ReaperSelfChannel")],
        [InlineKeyboardButton("✓ عضو شدم", callback_data="check_membership")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        
        if chat_member.status in ["member", "administrator", "creator"]:
            # کاربر عضو شد
            text = (
                "<b>༒『忍』𝕹𝕴𝕹𝕵𝕬『忍』༒</b>\n"
                "<b>/start</b>\n\n"
                "<b>❈ 𝙎𝙚𝙡𝙛 𝙋𝙝𝙖𝙣𝙩𝙤𝙢『𖣘』:</b>\n"
                "<b>✅ عضویت تأیید شد!</b>\n"
                "<b>اکنون به تمام امکانات ربات دسترسی داری 😉</b>\n\n"
                "<b>🔗 کانال: @Phantomupdatess</b>"
            )
            
            await query.edit_message_text(
                text,
                parse_mode='HTML'
            )
            
        else:
            # کاربر عضو نیست
            text = (
                "<b>⫸ شما هنوز عضو کانال زیر نشده اید !</b>\n"
                "<b>◄ ابتدا برای استفاده از ربات در کانال زیر عضو شوید !</b>"
            )
            
            keyboard = [
                [InlineKeyboardButton("ریپر سلف Reaper Self", url="https://t.me/ReaperSelfChannel")],
                [InlineKeyboardButton("✓ عضو شدم", callback_data="check_membership")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                text,
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
            
    except Exception as e:
        await query.answer("❌ خطا در بررسی عضویت!", show_alert=True)

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_membership, pattern="check_membership"))
    
    print("🤖 ربات در حال اجراست...")
    app.run_polling()

if __name__ == "__main__":
    main()
