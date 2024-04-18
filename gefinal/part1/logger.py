import logging
from termcolor import colored

class ColoredFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def format(self, record):
        if record.levelno == logging.DEBUG:
            return colored(super().format(record), 'green')
        elif record.levelno == logging.INFO:
            return colored(super().format(record), 'blue')
        elif record.levelno == logging.WARNING:
            return colored(super().format(record), 'yellow')
        elif record.levelno == logging.ERROR:
            return colored(super().format(record), 'red')
        elif record.levelno == logging.CRITICAL:
            return colored(super().format(record), 'magenta')
        else:
            return super().format(record)

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.ERROR)

