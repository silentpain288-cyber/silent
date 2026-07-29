import telebot

TOKEN = "8883032492:AAGUNmCljCd2AMf8n6hxlo9pUgSaQRpW0MU"
CHANNEL_ID = "@NnHHB5BhE785OTRk"  # آیدی کانال شما
USER_ID = 8831703400  # آیدی شما

bot = telebot.TeleBot(TOKEN)

print("=" * 50)
print("🔍 شروع عیب‌یابی ربات...")
print("=" * 50)

# مرحله 1: بررسی اینکه ربات زنده است
try:
    me = bot.get_me()
    print(f"✅ ربات فعال است: @{me.username}")
except Exception as e:
    print(f"❌ ربات غیرفعال است: {e}")
    exit()

# مرحله 2: بررسی دسترسی به کانال
try:
    chat = bot.get_chat(CHANNEL_ID)
    print(f"✅ کانال پیدا شد: {chat.title}")
    print(f"   📌 نوع کانال: {'عمومی' if chat.username else 'خصوصی'}")
    print(f"   📌 آیدی عددی: {chat.id}")
except Exception as e:
    print(f"❌ خطا در دسترسی به کانال: {e}")
    print("   ⚠️ مطمئن شوید ربات در کانال عضو است و ادمین است!")
    exit()

# مرحله 3: بررسی اینکه ربات ادمین است
try:
    bot_member = bot.get_chat_member(CHANNEL_ID, me.id)
    print(f"✅ وضعیت ربات در کانال: {bot_member.status}")
    if bot_member.status in ['administrator', 'creator']:
        print("   ✅ ربات ادمین است ✓")
    else:
        print("   ⚠️ ربات ادمین نیست! لطفاً ربات را ادمین کنید.")
except Exception as e:
    print(f"❌ خطا در بررسی وضعیت ربات: {e}")

# مرحله 4: بررسی عضویت کاربر شما
try:
    member = bot.get_chat_member(CHANNEL_ID, USER_ID)
    print(f"✅ وضعیت کاربر {USER_ID}: {member.status}")
    if member.status in ['member', 'administrator', 'creator']:
        print("   ✅ کاربر عضو کانال است ✓")
    else:
        print("   ⚠️ کاربر عضو کانال نیست!")
except Exception as e:
    print(f"❌ خطا در بررسی کاربر: {e}")
    if "user not found" in str(e):
        print("   ⚠️ کاربر در کانال نیست یا ربات دسترسی ندارد!")

print("=" * 50)
print("🏁 عیب‌یابی به پایان رسید.")
