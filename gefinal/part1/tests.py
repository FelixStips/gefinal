from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot
from otree.live import call_live_method_compat
from .logger import logger
from pprint import pprint
from part1 import Offer
import random


def accept_offer(offer: Offer, worker):
    # Adjusted to access properties via dot notation for a class instance 'offer'
    # offer  ether has     wage_points = models.FloatField() or
    #     wage_tokens = models.FloatField()
    # lets set wage based on which of two is not None
    wage = offer.wage_points if offer.wage_points is not None else offer.wage_tokens
    # same with currency_is_points
    currency_is_points = offer.wage_points is not None
    acceptance = {
        'information_type': 'accept',
        'private': False,  # Default value for private
        'employer_id': offer.employer_id,
        'wage': wage,
        'effort': offer.effort,
        'job_number': offer.job_number,
        'job_id': offer.job_id,  # Safely get 'job_id' if it exists, else default to None
        'worker_id': worker.participant.vars['playerID'],
        'currency_is_points': currency_is_points
    }
    return acceptance


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
    workers = [p for p in players if p.participant.vars["string_role"] == "worker" and not p.is_employed]
    employers = [p for p in players if p.participant.vars["string_role"] == "employer"]
    for i in employers:
        offer = generate_offer(i)
        logger.critical(f'Offer: {offer}')
        res = method(i.id_in_group, offer)
        #     lets get offers belonding to the group
        offers = Offer.filter(group=group)
        logger.error(f'how much offers: {len(offers)}')
    for offer in offers:
        random_worker = random.choice(workers)
        acceptance = accept_offer(offer, random_worker)
        logger.critical(f'Acceptance: {acceptance}')
        res = method(random_worker.id_in_group, acceptance)
        workers = [p for p in players if p.participant.vars["string_role"] == "worker" and not p.is_employed]



class PlayerBot(Bot):
    def play_round(self):
        logger.info(f'My role is: {self.player.participant.vars["string_role"]}')
        yield MarketPage
