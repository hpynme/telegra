import telebot
import os

TOKEN = os.getenv("TOKEN")  # Render এ সেট হবে

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.reply_to(msg, "হ্যালো আহাদ ভাই! আপনার বট কাজ করছে।")

bot.infinity_polling()
