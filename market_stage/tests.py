from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot
from otree.live import call_live_method_compat
from .logger import logger
from pprint import pprint
from market_stage import Offer

import random


def generate_private_offer(worker_id, employer_id, max_wage, currency_is_points):
    wage = random.randint(0, max_wage)  # Random wage between 0 and max_wage
    effort = random.randint(0, 1)  # Random binary effort (0 or 1)
    job_number = random.choice([3, 4])  # Random job number, either 3 or 4

    private_offer = {
        'information_type': 'private_offer',
        'employer_id': employer_id,
        'worker_id': worker_id,
        'wage': wage,
        'effort': effort,
        'job_number': job_number,
        'currency_is_points': currency_is_points
    }
    return private_offer


def create_private_offers(info):
    offers = []
    employer_id = info['playerID']  # Assume employer ID comes from 'playerID'
    max_wage = info['max_wage']
    currency_is_points = info['currency_is_points']

    # Iterate over the number of workers specified
    for i in range(1, info['num_workers'] + 1):
        worker_id_key = f'worker_id_{i}'
        wage_key = f'wage_{i}'

        if info[worker_id_key] != 'NA':
            worker_id = info[worker_id_key]
            # Generate an offer for each worker
            offer = generate_private_offer(worker_id, employer_id, max_wage, currency_is_points)
            offers.append(offer)

    return offers


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


def market_live_method(method, **kwargs):
    Offer = kwargs['Offer']
    group = kwargs['group']
    players = group.get_players()
    workers = [p for p in players if p.participant.vars["string_role"] == "worker" and not p.is_employed]
    employers = [p for p in players if p.participant.vars["string_role"] == "employer"]
    for i in employers:
        offer = generate_offer(i)
        logger.info(f'Offer: {offer}')
        res = method(i.id_in_group, offer)
        #     lets get offers belonding to the group
        offers = Offer.filter(group=group)

    for offer in offers:
        if workers:
            random_worker = random.choice(workers)
            acceptance = accept_offer(offer, random_worker)
            logger.info(f'Acceptance: {acceptance}')
            res = method(random_worker.id_in_group, acceptance)
            workers = [p for p in players if p.participant.vars["string_role"] == "worker" and not p.is_employed]


def reemploy_live_method(method, **kwargs):
    Offer = kwargs['Offer']
    logger.info('Reemploy live_method')
    Page = kwargs['page_class']
    group = kwargs['group']
    players = group.get_players()
    employers = [p for p in players if p.participant.vars["string_role"] == "employer"]
    eligible_employers = [p for p in employers if p.participant.vars.get('is_employer') and p.reemploy == 1]
    for i in eligible_employers:
        necessary_vars = ['max_wage', 'num_workers', 'wage_1', 'wage_2', 'playerID', ]
        nesessary_js_vars = ['currency_is_points', 'my_id', 'worker_id_1', 'worker_id_2']
        vars_for_template = {k: v for k, v in Page.vars_for_template(i).items() if k in necessary_vars}
        js_vars = {k: v for k, v in Page.js_vars(i).items() if k in nesessary_js_vars}
        full_vars = {**vars_for_template, **js_vars}

        private_offers = create_private_offers(full_vars)
        for o in private_offers:
            logger.info(f'private_offer {o}')
            res = method(i.id_in_group, o)


def call_live_method(method, **kwargs):
    logger.info(f'live_method {kwargs}')
    kwargs['Offer'] = Offer
    if kwargs.get('page_class').__name__ == 'MarketPage':
        market_live_method(method, **kwargs)
    if kwargs.get('page_class').__name__ == 'Reemploy':
        reemploy_live_method(method, **kwargs)


class PlayerBot(Bot):
    def play_round(self):
        shock_round_number = self.player.session.config['shock_after_rounds'] + 1
        skip_game = self.player.in_round(shock_round_number).skip_game
        if not skip_game:
            shock_round = self.player.round_number == self.player.session.config['shock_after_rounds'] + 1
            if shock_round:
                yield AnotherIntroduction,
                yield AnotherInstruction,

            if not self.player.skip_game:
                if not shock_round:
                    if self.player.participant.vars.get('is_employer') and self.player.round_number > 1:
                        num_workers = self.player.in_round(self.player.round_number - 1).num_workers_employed
                        if num_workers > 0:
                            yield CheckReemploy, dict(reemploy=random.randint(0, 1))
                    if self.player.participant.vars.get('is_employer') and self.player.reemploy == 1:
                        yield Reemploy

                yield Submission(Countdown, check_html=False)
                yield MarketPage
                if self.player.is_employed:
                    yield WorkPage, dict(effort_choice=random.randint(0, 1))
                yield Results

# making private offers
# Reemploy live_method 4 {'information_type': 'private_offer', 'employer_id': 4, 'worker_id': 5, 'wage': 77, 'effort': 1, 'job_number': 3, 'currency_is_points': True}
# Reemploy live_method 4 {'information_type': 'private_offer', 'employer_id': 4, 'worker_id': 6, 'wage': 88, 'effort': 1, 'job_number': 4, 'currency_is_points': True}
#
# accepting private offers
# {'information_type': 'accept',
#  'private': True,
#  'job_id': 9220, 'employer_id': 4, 'worker_id': 5, 'wage': 77,
#  'effort': 1, 'currency_is_points': True,
#  'job_number': None}
# accepting public offers
#  {'information_type': 'accept',
#   'private': False,
#   'employer_id': 1,
#   'wage': 12,
#   'effort': 1,
#   'job_number': 1,
#   'job_id': 110,
#   'worker_id': 3,
#   'currency_is_points': True}
