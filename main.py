import logging
import scheduler
from telegram_bot import bot


def setup_logger():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


setup_logger()
scheduler.start()
bot.infinity_polling()
scheduler.stop()
