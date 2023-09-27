from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

class PlayerBot(Bot):
    def play_round(self):
        if self.player.participant.vars['is_employer'] == True and self.player.participant.vars['small_market']:
            pass
        else:
            session = self.player.session
            rounds_part_two = session.config['total_rounds'] - session.config['shock_after_rounds']
            if self.player.round_number <= rounds_part_two:
                yield Submission(Countdown, check_html=False)
                yield MarketPage
                yield Results
