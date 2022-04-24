import telebot
from telebot.types import Message

from config import Config
from data_base import select_all_rows

bot = telebot.TeleBot(Config().bot_token, parse_mode="MARKDOWN")


@bot.message_handler(commands=['all_words'])
def stop_pipeline(message: Message):
    words = select_all_rows()
    reply = ""
    count = 0
    for word in words:
        count += 1
        reply += f"{word[0]} - {word[1]}"
        if count < len(words):
            reply += "\n"
    bot.reply_to(message, reply)
