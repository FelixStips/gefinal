from otree.api import Currency as c, currency_range
from . import *
from pprint import pprint
import random
from otree.api import Bot
from part1.tests import generate_private_offer, create_private_offers, accept_offer, \
    reemploy_live_method, market_live_method

from part2 import Offer
def call_live_method(method, **kwargs):
    logger.critical(f'live_method {kwargs}')
    kwargs['Offer'] = Offer
    if kwargs.get('page_class').__name__ == 'MarketPage':
        market_live_method(method, **kwargs)
    if kwargs.get('page_class').__name__ == 'Reemploy':
        reemploy_live_method(method, **kwargs)

class PlayerBot(Bot):
    def play_round(self):

        player = self.player
        session = player.session
        if player.participant.vars['small_market'] and not player.participant.vars[
            'migrant']:

            return
        round_part_two = player.round_number - 1 + session.config['shock_after_rounds']
        if round_part_two >= player.session.config['total_rounds']:

            return

        round_part_two = self.player.round_number + self.session.config['shock_after_rounds']

        if self.player.participant.is_employer and self.player.round_number > 1:
            num_workers = self.player.participant.vars['num_workers'][round_part_two - 2]

            if num_workers > 0:
                yield CheckReemploy, dict(reemploy=random.randint(0, 1))


        if self.player.participant.is_employer and self.player.reemploy == 1:
            yield Reemploy

        yield Submission(Countdown, check_html=False)

        yield MarketPage
        if self.player.is_employed:
            yield WorkPage, dict(effort_choice=random.randint(0, 1))
        yield Results
        round_part_two = player.round_number + session.config['shock_after_rounds']
        if round_part_two >= player.session.config['total_rounds']:

            return
