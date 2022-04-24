from dotenv import dotenv_values


class Config(object):
    bot_token = None
    repetition_intervals = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
            cls.bot_token = dotenv_values(".env").get("BOT_TOKEN")
            if cls.bot_token is None:
                raise Exception("В .env отсутствует значение для ключа BOT_TOKEN")
            cls.repetition_intervals = dotenv_values(".env").get("REPETITION_INTERVALS")
            if cls.repetition_intervals is None:
                raise Exception("В .env отсутствует значение для ключа REPETITION_INTERVALS")
            else:
                cls.repetition_intervals = cls.repetition_intervals.split(",")
                for i in range(0, len(cls.repetition_intervals)):
                    cls.repetition_intervals[i] = int(cls.repetition_intervals[i])
        return cls
