import threading
from datetime import datetime, timedelta

import time
import schedule

from config import config
from data_base import select_all_rows
from telegram_bot import write_message

global thread


def run():
    all_words = select_all_rows()
    words = []
    for word in all_words:
        count_message = int(word[3] / 2)
        plus_days = 0
        if count_message < len(config.repetition_intervals):
            for i in range(0, count_message + 1):
                plus_days += config.repetition_intervals[i]
        else:
            for value in config.repetition_intervals:
                plus_days += value
            plus_days += 20
        if (datetime.fromisoformat(word[2]).date() + timedelta(days=plus_days)) == datetime.today().date():
            words.append(word)
    count = 0
    message = ""
    for word in words:
        count += 1
        message += f"{word[0]} - {word[1]}"
        if count < len(words):
            message += "\n"
    if message != "":
        write_message(message)


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


def start():
    global thread
    schedule.every().day.at("11:24").do(run)
    schedule.every().day.at("21:50").do(run)
    thread = threading.Thread(target=schedule_checker)
    thread.start()


def stop():
    global thread
    thread.join()
