# -*- coding: utf-8 -*-

import logging
import scheduler
from data_base import create_table
from telegram_bot import bot


def setup_logger():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


if __name__ == "__main__":
    setup_logger()
    create_table()
    scheduler.start()
    bot.infinity_polling()
    scheduler.stop()
