from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

class PlayerBot(Bot):
    def play_round(self):
        yield PreResults
        yield Results, dict(email="bot@gmail.com")
        yield End, dict(feedback="This is a test feedback.")
        yield Submission(Close, check_html=False)

