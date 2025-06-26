import telebot
import os
from datetime import datetime

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="MarkdownV2")

# ইউজার আইডি অনুযায়ী টাস্ক ও নোট ডাটা
user_tasks = {}
user_done = {}
user_pinned = {}
user_notes = {}

def escape_markdown(text):
    escape_chars = r"\_*[]()~`>#+-=|{}.!"
    for ch in escape_chars:
        text = text.replace(ch, f"\\{ch}")
    return text

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
                 "👋 হ্যালো আহাদ ভাই!\n\n"
                 "নিচের কমান্ডগুলো ব্যবহার করুন:\n"
                 "`/add কাজ লিখুন` - কাজ যোগ করুন\n"
                 "`/list` - সব কাজ দেখুন\n"
                 "`/done নম্বর` - কাজ সম্পন্ন করুন\n"
                 "`/remove নম্বর` - কাজ ডিলিট করুন\n"
                 "`/edit নম্বর নতুন_কাজ` - কাজ সংশোধন করুন\n"
                 "`/clear` - সব কাজ মুছুন\n"
                 "`/pin নম্বর` - জরুরি কাজ পিন করুন\n"
                 "`/unpin` - পিন রিমুভ করুন\n"
                 "`/note লিখুন` - নোট যোগ করুন\n"
                 "`/notes` - নোট দেখুন\n"
                 "`/help` - সাহায্যের জন্য\n"
                 "`/about` - বট সম্পর্কে\n"
                 "`/total` - মোট কাজ সংখ্যা\n"
                 "`/date` - আজকের তারিখ\n"
                 "`/time` - বর্তমান সময়\n"
                 "`/save` - কাজ টেক্সট আকারে পান\n"
                 "`/copyall` - সব কাজ copyable দেখুন\n"
                 "`/find খুঁজুন` - কাজের মধ্যে সার্চ\n"
                 "`/reset` - সব কিছু রিসেট\n"
                 , parse_mode="MarkdownV2")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.reply_to(message,
                 "বট কমান্ডগুলো:\n"
                 "`/add কাজ লিখুন`\n"
                 "`/list`\n"
                 "`/done নম্বর`\n"
                 "`/remove নম্বর`\n"
                 "`/edit নম্বর নতুন_কাজ`\n"
                 "`/clear`\n"
                 "`/pin নম্বর`\n"
                 "`/unpin`\n"
                 "`/note লিখুন`\n"
                 "`/notes`\n"
                 "`/total`\n"
                 "`/date`\n"
                 "`/time`\n"
                 "`/save`\n"
                 "`/copyall`\n"
                 "`/find খুঁজুন`\n"
                 "`/reset`\n"
                 , parse_mode="MarkdownV2")

@bot.message_handler(commands=['about'])
def about(message):
    bot.reply_to(message,
                 "Ahad Pro To-Do Bot v2\n"
                 "Author: Ahad\n"
                 "Features: Advanced To-Do, Notes, Reminder demo\n"
                 "Built with ❤️ using Python & telebot\n"
                 "GitHub ready & Render deployable\n"
                 , parse_mode="MarkdownV2")

@bot.message_handler(commands=['add'])
def add_task(message):
    uid = message.from_user.id
    task = message.text.replace('/add', '').strip()
    if not task:
        bot.reply_to(message, "❗ কাজ লিখে দিন: `/add তোমার কাজ`", parse_mode="MarkdownV2")
        return
    user_tasks.setdefault(uid, []).append(task)
    bot.reply_to(message, f"✅ কাজ যোগ হয়েছে: `{escape_markdown(task)}`", parse_mode="MarkdownV2")

@bot.message_handler(commands=['list'])
def list_tasks(message):
    uid = message.from_user.id
    tasks = user_tasks.get(uid, [])
    pinned = user_pinned.get(uid, None)
    done = user_done.get(uid, [])
    if not tasks:
        bot.reply_to(message, "📭 কোনো কাজ নেই। `/add` দিয়ে যোগ করুন।", parse_mode="MarkdownV2")
        return
    lines = []
    if pinned:
        lines.append(f"📌 *পিন করা কাজ:* `{escape_markdown(pinned)}`\n")
    for i, t in enumerate(tasks):
        mark = "✔️" if i in done else "❌"
        lines.append(f"{i+1}\\.\ {mark} `{escape_markdown(t)}`")
    text = "\n".join(lines)
    bot.reply_to(message, f"📝 *আপনার কাজের তালিকা:*\n\n{text}", parse_mode="MarkdownV2")

@bot.message_handler(commands=['done'])
def done_task(message):
    uid = message.from_user.id
    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        bot.reply_to(message, "❗ সঠিক ব্যবহার: `/done কাজের_নম্বর`", parse_mode="MarkdownV2")
        return
    idx = int(args[1]) - 1
    tasks = user_tasks.get(uid, [])
    if idx < 0 or idx >= len(tasks):
        bot.reply_to(message, "❗ ভুল কাজের নম্বর", parse_mode="MarkdownV2")
        return
    user_done.setdefault(uid, [])
    if idx in user_done[uid]:
        bot.reply_to(message, "⚠️ কাজ ইতিমধ্যে সম্পন্ন হয়েছে।", parse_mode="MarkdownV2")
        return
    user_done[uid].append(idx)
    bot.reply_to(message, f"✅ কাজ {idx+1} সম্পন্ন হয়েছে।", parse_mode="MarkdownV2")

@bot.message_handler(commands=['remove'])
def remove_task(message):
    uid = message.from_user.id
    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        bot.reply_to(message, "❗ সঠিক ব্যবহার: `/remove কাজের_নম্বর`", parse_mode="MarkdownV2")
        return
    idx = int(args[1]) - 1
    tasks = user_tasks.get(uid, [])
    if idx < 0 or idx >= len(tasks):
        bot.reply_to(message, "❗ ভুল কাজের নম্বর", parse_mode="MarkdownV2")
        return
    removed_task = tasks.pop(idx)
    # Remove from done list if present
    if uid in user_done and idx in user_done[uid]:
        user_done[uid].remove(idx)
    # Adjust done indices > idx
    if uid in user_done:
        user_done[uid] = [i-1 if i > idx else i for i in user_done[uid]]
    bot.reply_to(message, f"🗑️ কাজ '{escape_markdown(removed_task)}' ডিলিট হয়েছে।", parse_mode="MarkdownV2")

@bot.message_handler(commands=['edit'])
def edit_task(message):
    uid = message.from_user.id
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3 or not parts[1].isdigit():
        bot.reply_to(message, "❗ সঠিক ব্যবহার: `/edit কাজের_নম্বর নতুন_কাজ`", parse_mode="MarkdownV2")
        return
    idx = int(parts[1]) - 1
    new_task = parts[2].strip()
    tasks = user_tasks.get(uid, [])
    if idx < 0 or idx >= len(tasks):
        bot.reply_to(message, "❗ ভুল কাজের নম্বর", parse_mode="MarkdownV2")
        return
    old_task = tasks[idx]
    tasks[idx] = new_task
    bot.reply_to(message, f"✏️ কাজ পরিবর্তন হয়েছে:\nপুরানো: `{escape_markdown(old_task)}`\nনতুন: `{escape_markdown(new_task)}`", parse_mode="MarkdownV2")

@bot.message_handler(commands=['clear'])
def clear_tasks(message):
    uid = message.from_user.id
    user_tasks[uid] = []
    user_done[uid] = []
    user_pinned[uid] = None
    bot.reply_to(message, "🗑️ সব কাজ ডিলিট করা হয়েছে।", parse_mode="MarkdownV2")

@bot.message_handler(commands=['pin'])
def pin_task(message):
    uid = message.from_user.id
    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        bot.reply_to(message, "❗ সঠিক ব্যবহার: `/pin কাজের_নম্বর`", parse_mode="MarkdownV2")
        return
    idx = int(args[1]) - 1
    tasks = user_tasks.get(uid, [])
    if idx < 0 or idx >= len(tasks):
        bot.reply_to(message, "❗ ভুল কাজের নম্বর", parse_mode="MarkdownV2")
        return
    user_pinned[uid] = tasks[idx]
    bot.reply_to(message, f"📌 কাজ পিন করা হয়েছে: `{escape_markdown(tasks[idx])}`", parse_mode="MarkdownV2")

@bot.message_handler(commands=['unpin'])
def unpin_task(message):
    uid = message.from_user.id
    if user_pinned.get(uid):
        user_pinned[uid] = None
        bot.reply_to(message, "📌 পিন রিমুভ করা হয়েছে।", parse_mode="MarkdownV2")
    else:
        bot.reply_to(message, "⚠️ কোন কাজ পিন করা নেই।", parse_mode="MarkdownV2")

@bot.message_handler(commands=['note'])
def add_note(message):
    uid = message.from_user.id
    note = message.text.replace('/note', '').strip()
    if not note:
        bot.reply_to(message, "❗ `/note` এর পরে কিছু লিখুন।", parse_mode="MarkdownV2")
        return
    user_notes.setdefault(uid, []).append(note)
    bot.reply_to(message, f"🗒️ নোট যোগ হয়েছে: `{escape_markdown(note)}`", parse_mode="MarkdownV2")

@bot.message_handler(commands=['notes'])
def list_notes(message):
    uid = message.from_user.id
    notes = user_notes.get(uid, [])
    if not notes:
        bot.reply_to(message, "📭 কোনো নোট নেই। `/note` দিয়ে যোগ করুন।", parse_mode="MarkdownV2")
        return
    notes_text = "\n".join([f"{i+1}\\.\ `{escape_markdown(n)}`" for i, n in enumerate(notes)])
    bot.reply_to(message, f"🗒️ আপনার নোটগুলো:\n\n{notes_text}", parse_mode="MarkdownV2")

@bot.message_handler(commands=['total'])
def total_tasks(message):
    uid = message.from_user.id
    count = len(user_tasks.get(uid, []))
    bot.reply_to(message, f"📊 আপনার মোট কাজ সংখ্যা: {count}", parse_mode="MarkdownV2")

@bot.message_handler(commands=['date'])
def date_cmd(message):
    now = datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    bot.reply_to(message, f"📅 আজকের তারিখ: {date_str}", parse_mode="MarkdownV2")

@bot.message_handler(commands=['time'])
def time_cmd(message):
    now = datetime.now()
    time_str = now.strftime("%I:%M %p")
    bot.reply_to(message, f"⏰ বর্তমান সময়: {time_str}", parse_mode="MarkdownV2")

@bot.message_handler(commands=['save'])
def save_tasks(message):
    uid = message.from_user.id
    tasks = user_tasks.get(uid, [])
    if not tasks:
        bot.reply_to(message, "📭 কোনো কাজ নেই যা সেভ করতে পারেন।", parse_mode="MarkdownV2")
        return
    text = "\n".join([f"{i+1}. {t}" for i, t in enumerate(tasks)])
    bot.reply_to(message, f"💾 আপনার কাজগুলো:\n```\n{text}\n```", parse_mode="MarkdownV2")

@bot.message_handler(commands=['copyall'])
def copy_all(message):
    uid = message.from_user.id
    tasks = user_tasks.get(uid, [])
    if not tasks:
        bot.reply_to(message, "📭 কোনো কাজ নেই।", parse_mode="MarkdownV2")
        return
    text = "\n".join([f"{i+1}\\.\ `{escape_markdown(t)}`" for i, t in enumerate(tasks)])
    bot.reply_to(message, f"📋 সব কাজ (copyable):\n\n{text}", parse_mode="MarkdownV2")

@bot.message_handler(commands=['find'])
def find_task(message):
    uid = message.from_user.id
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "❗ সঠিক ব্যবহার: `/find খুঁজুন`", parse_mode="MarkdownV2")
        return
    keyword = args[1].lower()
    tasks = user_tasks.get(uid, [])
    results = [f"{i+1}\\.\ `{escape_markdown(t)}`" for i, t in enumerate(tasks) if keyword in t.lower()]
    if not results:
        bot.reply_to(message, "🔍 কোন কাজ পাওয়া যায়নি।", parse_mode="MarkdownV2")
        return
    bot.reply_to(message, "🔍 খোঁজা ফলাফল:\n\n" + "\n".join(results), parse_mode="MarkdownV2")

@bot.message_handler(commands=['reset'])
def reset_bot(message):
    uid = message.from_user.id
    user_tasks[uid] = []
    user_done[uid] = []
    user_pinned[uid] = None
    user_notes[uid] = []
    bot.reply_to(message, "♻️ সব কিছু রিসেট করা হয়েছে।", parse_mode="MarkdownV2")

# বট চালু রাখুন
bot.infinity_polling()
