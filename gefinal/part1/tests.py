from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot
from otree.live import call_live_method_compat
from .logger import logger
from pprint import pprint
from part1 import Offer
import random

def generate_offer(player, job_number=1, currency_is_points=True):
    wage = random.randint(0, 100)  # Random wage between 0 and 100
    effort = random.randint(0, 1)  # Random binary effort 0 or 1
    offer = {
        'information_type': 'offer',
        'employer_id': player.participant.playerID,
        'wage': wage,
        'effort': effort,
        'status': 'open',
        'job_number': job_number,
        'currency_is_points': currency_is_points
    }
    return offer


def call_live_method(method, **kwargs):
    logger.critical(f'live_method {kwargs}')
    group = kwargs['group']
    players = group.get_players()
    workers = [p for p in players if p.participant.vars["string_role"] == "worker"]
    employers = [p for p in players if p.participant.vars["string_role"] == "employer"]
    for i in employers:
        offer = generate_offer(i)
        logger.critical(f'Offer: {offer}')
        res = method(i.id_in_group, offer)
    #     lets get offers belonding to the group
        offers = Offer.filter(group=group)
        logger.error(f'how much offers: {len(offers)}')
    # for p in group.get_players():
    #     logger.critical(p.participant.vars["string_role"])
    # method(1, {"offer": 50})
    # method(2, {"accepted": False})
    # method(1, {"offer": 60})
    # retval = method(2, {"accepted": True})
    # you can do asserts on retval


class PlayerBot(Bot):
    def play_round(self):
        # if self.player.participant.vars["string_role"] == "employer":
        #     res = MarketPage.live_method(self.player,
        #                        {'information_type': 'offer', 'employer_id': self.player.participant.playerID, 'wage': 22, 'effort': 1, 'status': 'open', 'job_number': 1, 'currency_is_points': True})
        #

        logger.info(f'My role is: {self.player.participant.vars["string_role"]}')
        yield MarketPage

