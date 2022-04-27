import threading
from datetime import datetime, timedelta

import time
import schedule

from config import config
from data_base import select_all_rows, update_word
from telegram_bot import write_message

global thread

words_to_repeat = []


def generate_message(list_words: list):
    count = 0
    message = ""
    for word in list_words:
        count += 1
        message += f"{word[0]} - {word[1]}"
        if count < len(list_words):
            message += "\n"
    return message


def clear_words():
    global words_to_repeat
    words_to_repeat = []


def first_shipment_of_the_day():
    global words_to_repeat
    words_to_repeat = []
    all_words = select_all_rows()
    for word in all_words:
        if datetime.strptime(word[2], config.date_format).date() <= datetime.today():
            words_to_repeat.append(word)
            if len(config.repetition_intervals) - 1 >= word[3]:
                new_date = datetime.strptime(word[2], config.date_format).date() + timedelta(days=config.repetition_intervals[word[3]])
            else:
                new_date = datetime.strptime(word[2], config.date_format).date() + timedelta(days=30)
            update_word(word[0], new_date, config.repetition_intervals[word[3]])
    message = generate_message(words_to_repeat)
    if message != "":
        write_message(message)
    else:
        write_message("Отсутствуют слова для повторения")


def next_shipment_of_the_day():
    global words_to_repeat
    if len(words_to_repeat) > 0:
        message = generate_message(words_to_repeat)
        if message != "":
            write_message(message)
        else:
            write_message("Отсутствуют слова для повторения")
    else:
        first_shipment_of_the_day()


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


def start():
    global thread
    schedule.every().day.at("07:19").do(first_shipment_of_the_day)
    schedule.every().day.at("21:50").do(next_shipment_of_the_day)
    schedule.every().day.at("22:00").do(clear_words)
    thread = threading.Thread(target=schedule_checker)
    thread.start()


def stop():
    global thread
    thread.join()
