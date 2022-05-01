# -*- coding: utf-8 -*-

import random
import re
from datetime import date, timedelta
from typing import Union

import enchant
import telebot
from telebot import types
from telebot.types import Message

from config import config
from data_base import insert_new_word, select_all_rows, check_exist_word, db_delete_word

bot = telebot.TeleBot(config.bot_token, parse_mode="MARKDOWN")
word = None
translation = None


def generate_message(list_words: list) -> str:
    count = 0
    message = ""
    for i in list_words:
        count += 1
        if count % 2 == 1:
            message += f"*{i[0]} - {i[1]}*"
        else:
            message += f"{i[0]} - {i[1]}"
        if count < len(list_words):
            message += "\n"
    return message


def cancel_marcup():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    bt1 = types.KeyboardButton('Отмена')
    markup.add(bt1)
    return markup


def write_message(message: str, chat_id: Union[int, str] = config.chat_id):
    bot.send_message(text=message, chat_id=chat_id)


def start_screen(message: str, shat_id: Union[int, str] = config.chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton('Добавить слово')
    button2 = types.KeyboardButton('Удалить слово')
    button3 = types.KeyboardButton('Вывести 10 случайных слов')
    button4 = types.KeyboardButton('Вывести все слова')
    markup.add(button1, button2, button3, button4)
    msg = bot.send_message(shat_id, message, reply_markup=markup)
    bot.register_next_step_handler(msg, add_english_word)


@bot.message_handler(commands=['start'])
def start(message: Message):
    start_screen("Выберите один из предложенных вариантов", message.chat.id)


def add_english_word(message: Message):
    try:
        chat_id = message.chat.id

        if message.text == 'Добавить слово':
            msg = bot.send_message(chat_id, 'Введите слово или фразу на английском', reply_markup=cancel_marcup())
            bot.register_next_step_handler(msg, add_translation)

        elif message.text == 'Удалить слово':
            msg = bot.send_message(chat_id, 'Введите слово или его перевод которое хотите удалить', reply_markup=cancel_marcup())
            bot.register_next_step_handler(msg, delete_word)

        elif message.text == 'Вывести все слова':
            all_words = select_all_rows()
            if len(all_words) > 0:
                start_screen(generate_message(all_words), chat_id)
            else:
                start_screen("Отсутствуют сохранённые слова", chat_id)

        elif message.text == 'Вывести 10 случайных слов':
            all_words = select_all_rows()
            if len(all_words) == 0:
                start_screen("Словарь пусть, добавьте новые слова для изучения", chat_id)
            elif len(all_words) < 10:
                case = 'слов'
                if len(all_words) == 1:
                    case += "о"
                elif 2 <= len(all_words) <= 4:
                    case += "а"
                write_message(f"В словаре содержится только {len(all_words)} {case} для повторения", chat_id)
                start_screen(generate_message(all_words), chat_id)
            else:
                ten_words = []
                for i in range(10):
                    int_random = random.randint(0, len(all_words) - 1)
                    ten_words.append(all_words.pop(int_random))
                start_screen(generate_message(ten_words), chat_id)
        else:
            start_screen("Неизвестная команда, нужно выбрать один из предложенных вариантов", chat_id)

    except Exception as e:
        print(str(e))


def add_translation(message: Message):
    global word
    try:
        chat_id = message.chat.id

        if message.text != 'Отмена':
            word = message.text

            wrong_words = []
            d = enchant.Dict("en_US")
            pars_words = re.findall("[a-zA-Z]+|[а-яА-Я]+", word)
            if len(pars_words) > 0:
                for i in pars_words:
                    if not d.check(i):
                        wrong_words.append(i)
                if len(wrong_words) == 1:
                    msg = bot.send_message(chat_id, f"Слово {wrong_words[0]!r} не найдено в английском словаре, повторите ввод", reply_markup=cancel_marcup())
                    bot.register_next_step_handler(msg, add_translation)
                elif len(wrong_words) > 1:
                    msg = bot.send_message(chat_id, f"Слова {', '.join(wrong_words)!r} не найдены в английском словаре, повторите ввод", reply_markup=cancel_marcup())
                    bot.register_next_step_handler(msg, add_translation)
                else:
                    msg = bot.send_message(chat_id, 'Введите перевод на русский', reply_markup=cancel_marcup())
                    bot.register_next_step_handler(msg, save_translation)
            else:
                msg = bot.send_message(chat_id, f"Введите английское слово или фразу вместо {word!r}", reply_markup=cancel_marcup())
                bot.register_next_step_handler(msg, add_translation)
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


def delete_word(message: Message):
    chat_id = message.chat.id
    mes = message.text.lower().capitalize()
    try:
        if mes != 'Отмена':
            if check_exist_word(mes):
                db_delete_word(mes)
                start_screen(f"Слово/перевод {mes!r} удалено из словаря", chat_id)
            else:
                start_screen(f"{mes!r} не найдено в словаре", chat_id)
        else:
            start_screen("Удаление отменено", chat_id)

    except Exception as e:
        print(str(e))
        start_screen("Непредвиденная ошибка при удалении слова, попробуйте ещё раз", chat_id)
