import threading
import time
import schedule

global thread


def run():
    print("1")


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


def start():
    global thread
    schedule.every().day.at("07:20").do(run)
    schedule.every().day.at("21:50").do(run)
    thread = threading.Thread(target=schedule_checker)
    thread.start()


def stop():
    global thread
    thread.join()
