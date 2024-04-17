from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot
# example of message by employer
#  live_method {'information_type': 'offer', 'employer_id': 1, 'wage': 22, 'effort': 1, 'status': 'open', 'job_number': 1, 'currency_is_points': True}
# example of message by worker
#  live_method {'information_type': 'accept', 'private': False, 'employer_id': 4, 'wage': 22, 'effort': 1, 'job_number': 2, 'job_id': 211, 'worker_id': 5, 'currency_is_points': True}
class PlayerBot(Bot):
    def play_round(self):
        session = self.player.session
        if self.player.round_number <= session.config['shock_after_rounds']:
            yield Submission(Countdown, check_html=False)
            yield MarketPage
            yield Results
