from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

class PlayerBot(Bot):
    def play_round(self):
        yield Submission(Countdown, check_html=False)
        yield MarketPage
        yield Results
