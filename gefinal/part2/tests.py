from otree.api import Currency as c, currency_range
from . import *
from pprint import pprint
from otree.api import Bot
from part1.tests import generate_private_offer, create_private_offers, accept_offer, call_live_method, \
    reemploy_live_method, market_live_method


class PlayerBot(Bot):
    def play_round(self):
        proceed = True
        player = self.player
        session = player.session
        if player.participant.vars['small_market'] and not player.participant.vars[
            'migrant']:
            proceed= False

        round_part_two = player.round_number + session.config['shock_after_rounds']
        if round_part_two >= player.session.config['total_rounds']:
            proceed = False
        if proceed:
            if player.participant.is_employer and player.round_number > 1:
                num_workers = player.participant.vars['num_workers'][round_part_two - 2]
                if num_workers > 0:
                    yield CheckReemploy, dict(reemploy=random.randint(0, 1))

            if self.player.participant.is_employer and self.player.reemploy == 1:
                yield Reemploy
            logger.critical(f'player: {player}; round: {player.round_number}')
            pprint(player.participant.vars)
            logger.critical('*' * 100)
            yield Submission(Countdown, check_html=False)

            yield MarketPage
            if self.player.is_employed:
                yield WorkPage, dict(effort_choice=random.randint(0, 1))
            yield Results
