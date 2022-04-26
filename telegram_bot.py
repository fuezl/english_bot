from datetime import date, timedelta

import telebot
from telebot import types
from telebot.types import Message

from config import config
from data_base import insert_new_word

bot = telebot.TeleBot(config.bot_token, parse_mode="MARKDOWN")
word = None
translation = None


def write_message(message: str):
    bot.send_message(text=message, chat_id=config.chat_id)


def start_screen(message: str, shat_id: int):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Добавить слово')
    itembtn2 = types.KeyboardButton('10 случайных слов')
    itembtn3 = types.KeyboardButton('Удалить слово')
    markup.add(itembtn1, itembtn2, itembtn3)
    msg = bot.send_message(shat_id, message, reply_markup=markup)
    bot.register_next_step_handler(msg, add_english_word)


@bot.message_handler(commands=['start'])
def all_words(message: Message):
    start_screen("Выберите один из предложенных вариантов", message.chat.id)


def add_english_word(message: Message):
    try:
        chat_id = message.chat.id

        if message.text == 'Добавить слово':
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            bt1 = types.KeyboardButton('Отмена')
            markup.add(bt1)
            msg = bot.send_message(chat_id, 'Введите слово или фразу на английском', reply_markup=markup)
            bot.register_next_step_handler(msg, add_translation)

    except Exception as e:
        print(str(e))


def add_translation(message: Message):
    global word
    try:
        chat_id = message.chat.id

        if message.text != 'Отмена':
            word = message.text
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            bt1 = types.KeyboardButton('Отмена')
            markup.add(bt1)
            msg = bot.send_message(chat_id, 'Введите перевод на русский', reply_markup=markup)
            bot.register_next_step_handler(msg, save_translation)
        else:
            start_screen("Слово не добавлено", chat_id)

    except Exception as e:
        print(str(e))


def save_translation(message: Message):
    global word
    global translation
    chat_id = message.chat.id
    try:
        if message.text != 'Отмена':
            translation = message.text
            next_shipping_date = date.today() + timedelta(days=config.repetition_intervals[0])
            if isinstance(word, str):
                insert_new_word(word, translation, next_shipping_date)
                start_screen(f"Слово/фраза {word!r} с переводом {translation!r} сохранены для последующего повторения", chat_id)
            else:
                start_screen("Слово не сохранено, попробуйте ещё раз", chat_id)
        else:
            start_screen(f"Перевод не введён, слово {word!r} не сохранено!", chat_id)

    except Exception as e:
        print(str(e))
        start_screen("Непредвиденная ошибка при сохранении слова, попробуйте ещё раз", chat_id)
