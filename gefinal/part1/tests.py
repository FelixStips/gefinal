from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

class PlayerBot(Bot):
    def play_round(self):
        session = self.player.session
        if self.player.round_number <= session.config['shock_after_rounds']:
            yield Submission(Countdown, check_html=False)
            yield MarketPage
            yield Results
