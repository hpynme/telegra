import telebot
import os

# টোকেন Environment variable থেকে নেওয়া (Render-এর জন্য)
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# আলাদা ইউজারের জন্য কাজের লিস্ট
user_tasks = {}

# /start কমান্ড
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 হ্যালো আহাদ ভাই!\nএই বটে আপনি নিচের কমান্ডগুলো ব্যবহার করতে পারবেন:\n\n"
                          "🟢 `/add` → নতুন কাজ যোগ করুন\n"
                          "🟢 `/list` → আপনার সব কাজ দেখুন\n"
                          "🟢 `/clear` → সব কাজ ডিলিট করুন")

# /add <task>
@bot.message_handler(commands=['add'])
def add_task(message):
    uid = message.from_user.id
    task = message.text.replace('/add', '').strip()

    if not task:
        bot.reply_to(message, "❗ `/add` কমান্ডের পরে কাজ লিখুন। যেমন: `/add ভিডিও বানানো`")
        return

    user_tasks.setdefault(uid, []).append(task)
    bot.reply_to(message, f"✅ টাস্ক যোগ হয়েছে: {task}")

# /list
@bot.message_handler(commands=['list'])
def list_tasks(message):
    uid = message.from_user.id
    tasks = user_tasks.get(uid, [])

    if not tasks:
        bot.reply_to(message, "📭 আপনার কোনো টাস্ক নেই। `/add` দিয়ে কাজ যোগ করুন।")
        return

    task_list = "\n".join([f"{i+1}. {t}" for i, t in enumerate(tasks)])
    bot.reply_to(message, f"📝 আপনার কাজের তালিকা:\n{task_list}")

# /clear
@bot.message_handler(commands=['clear'])
def clear_tasks(message):
    uid = message.from_user.id
    user_tasks[uid] = []
    bot.reply_to(message, "🗑️ আপনার সব কাজ ডিলিট করা হয়েছে।")

# বট চালু রাখার জন্য
bot.infinity_polling()
