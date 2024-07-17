from otree.api import *
import time
import datetime
import otree
from .logger import logger
from .market import live_method
from pprint import pprint
from os import environ
import math


def market_live_method(player, data):
    return live_method(player, data, Offer)


logger.info(f'otree version {otree.__version__}')

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'market_stage'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = int(environ.get('NUM_ROUNDS', 16))


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    @property
    def num_unmatched_workers(self):
        unmatched_workers = [w for w in self.workers if not w.is_employed]
        return len(unmatched_workers)

    @property
    def num_unmatched_jobs(self):
        offers = Offer.filter(group=self, status='open')
        return len(offers)

    @property
    def is_finished(self):
        return all([p.is_finished for p in self.workers]) or all([p.is_finished for p in self.employers])

    @property
    def num_job_offers(self):
        return len(Offer.filter(group=self, private=False, status='open'))

    @property
    def job_offer_counter(self):
        return len(Offer.filter(group=self, private=False))

    @property
    def prvt_job_offer_counter(self):
        return len(Offer.filter(group=self, private=True))

    @property
    def players_in_group(self):
        return len(self.get_players())

    @property
    def workers(self):
        return [p for p in self.get_players() if not p.is_employer]

    @property
    def employers(self):
        return [p for p in self.get_players() if p.participant.vars.get('is_employer', False)]

    @property
    def employers_in_group(self):
        return len(self.employers)

    @property
    def workers_in_group(self):
        return len(self.workers)

    marketID = models.IntegerField()
    large_market = models.BooleanField()
    large_market_1 = models.BooleanField()
    large_market_2 = models.BooleanField()

    start_timestamp = models.StringField()
    average_wage_points = models.FloatField()
    average_wage_tokens = models.FloatField()
    average_effort = models.FloatField()
    average_payoff_firms_points = models.FloatField()
    average_payoff_firms_tokens = models.FloatField()
    average_payoff_workers_points = models.FloatField()
    average_payoff_workers_tokens = models.FloatField()


class Offer(ExtraModel):
    group = models.Link(Group)
    marketID = models.IntegerField()
    round_number = models.IntegerField()
    job_id = models.IntegerField()
    job_number = models.IntegerField()
    timestamp_created = models.LongStringField()
    timestamp_accepted = models.LongStringField()
    timestamp_cancelled = models.LongStringField()
    status = models.StringField()
    show = models.BooleanField()
    private = models.BooleanField()
    employer_id = models.IntegerField()
    worker_id = models.IntegerField()
    wage_points = models.FloatField()
    wage_tokens = models.FloatField()
    effort = models.IntegerField()
    effort_given = models.IntegerField()


class Player(BasePlayer):
    is_employer = models.BooleanField()
    skip_game = models.BooleanField(initial=False)
    is_finished = models.BooleanField(initial=False)
    average_wage_points = models.FloatField()
    average_wage_tokens = models.FloatField()
    average_effort = models.FloatField()

    @property
    def num_workers_employed(self):
        return len(Offer.filter(group=self.group, employer_id=self.participant.playerID, status='accepted'))

    @property
    def total_wage_paid_tokens(self):
        """Total wage paid by the firm (in tokens)"""
        return sum([o.wage_tokens for o in
                    Offer.filter(group=self.group, employer_id=self.participant.playerID, status='accepted')])

    @property
    def total_wage_paid_points(self):
        """Total wage paid by the firm (in points)"""
        return self.total_wage_paid_tokens / self.session.config['exchange_rate']

    total_effort_received = models.IntegerField(initial=0)  # Total effort received by the firm
    effort_cost_points = models.FloatField()  # Effort cost equivalent to the effort level in points
    effort_cost_tokens = models.FloatField()  # Effort cost equivalent to the effort level in tokens
    effort_worth_points = models.FloatField()  # Effort worth of the firm (in points)
    effort_worth_tokens = models.FloatField()  # Effort worth of the firm (in tokens)
    payoff_points = models.FloatField(initial=0)  # Payoff of the firm (in points)
    payoff_tokens = models.FloatField(initial=0)  # Payoff of the firm (in tokens)
    is_employed = models.BooleanField(initial=False)  # Boolean for whether the worker is employed
    wage_received_tokens = models.FloatField(min=0)  # Wage the worker received by the firm (in tokens)
    wage_received_points = models.FloatField(min=0)  # Wage the worker received by the firm (in points)
    effort_requested = models.IntegerField(min=0, max=1)  # Effort level the firm requested from the worker
    effort_choice = models.IntegerField(min=0, max=1)  # Effort choice of the worker
    matched_with_id = models.IntegerField()  # ID of the firm the worker is matched with
    employer_payoff_points = models.FloatField()  # Payoff of the employer (in points)
    employer_payoff_tokens = models.FloatField()  # Payoff of the employer (in tokens)
    worker_counter = models.IntegerField()
    done = models.BooleanField(initial=False)
    reemploy = models.IntegerField(initial=0)
    show_private = models.BooleanField(initial=False)
    wait = models.BooleanField(initial=False)  # Show wait page if true (workers)
    invalid = models.BooleanField(initial=False)  # Show job acceptance was invalid alert if true
    offer1 = models.StringField(initial="empty")
    offer2 = models.StringField(initial="empty")
    offer3 = models.StringField(initial="empty")
    offer4 = models.StringField(initial="empty")


# FUNCTIONS
def creating_session(subsession: Subsession):
    for p in subsession.get_player():
        p.is_employer = p.participant.vars.get('is_employer', False)

    players = subsession.get_players()
    shock_after_rounds = subsession.session.config['shock_after_rounds']
    assert shock_after_rounds <= C.NUM_ROUNDS, 'Shock after rounds cannot be larger than the number of rounds'
    if subsession.round_number <= shock_after_rounds:
        players_in_large_market_1 = [p for p in players if p.participant.vars.get('large_market_1')]
        players_in_large_market_2 = [p for p in players if p.participant.vars.get('large_market_2')]
        players_in_small_market = [p for p in players if p.participant.vars.get('small_market')]
        subsession.set_group_matrix([players_in_large_market_1, players_in_large_market_2, players_in_small_market])

        logger.info(subsession.get_group_matrix())

    else:
        players_in_large_market_1 = [p for p in players if
                                     p.participant.vars.get('large_market_1') or p.participant.vars.get(
                                         'move_to_market_1')]
        players_in_large_market_2 = [p for p in players if
                                     p.participant.vars.get('large_market_2') or p.participant.vars.get(
                                         'move_to_market_2')]
        players_in_small_market = [p for p in players if
                                   p not in players_in_large_market_1 and p not in players_in_large_market_2]
        logger.info(f' {players_in_small_market=}')
        for p in players_in_small_market:
            p.participant.vars['skip_game'] = True

        subsession.set_group_matrix([players_in_large_market_1, players_in_large_market_2, players_in_small_market])
        logger.info(subsession.get_group_matrix())

    p1 = players_in_large_market_1[0]
    p2 = players_in_large_market_2[0]
    p3 = players_in_small_market[0]
    p1.group.marketID = 1
    p2.group.marketID = 2
    p3.group.marketID = 3
    p1.group.large_market = True
    p2.group.large_market = True
    p3.group.large_market = False


# PAGES
class CheckReemploy(Page):
    form_model = 'player'
    form_fields = ['reemploy']

    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == player.session.config['shock_after_rounds'] + 1:
            return False
        if player.participant.vars.get('is_employer') and player.round_number > 1:
            return player.in_round(player.round_number - 1).num_workers_employed > 0


class Reemploy(Page):
    timeout_seconds = 120
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == player.session.config['shock_after_rounds'] + 1:
            return False
        return player.participant.vars.get('is_employer') and player.reemploy == 1

    @staticmethod
    def js_vars(player: Player):
        session = player.session
        if player.participant.currency_is_points:
            max_wage = session.config['max_wage']
        else:
            max_wage = session.config['max_wage'] * session.config['exchange_rate']

        return dict(
            my_id=player.participant.vars['playerID'],
            worker_id_1=player.participant.vars['worker1_id'][player.round_number - 2],
            worker_id_2=player.participant.vars['worker2_id'][player.round_number - 2],
            currency_is_points=player.participant.vars['currency_is_points'],
            max_wage=max_wage,
        )

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session

        num_workers = player.participant.vars['num_workers'][player.round_number - 2]
        if num_workers == 1:
            effort_given_1 = player.participant.vars['worker1_effort_given'][player.round_number - 2]
            effort_given_1_string = session.config['effort_names'][effort_given_1]
            effort_given_2 = 999
            effort_given_2_string = ''
            if player.participant.currency_is_points:
                max_wage = session.config['max_wage']
                wage_1 = player.participant.vars['worker1_wage_points'][player.round_number - 2]
                wage_2 = 999
            else:
                max_wage = session.config['max_wage'] * session.config['exchange_rate']
                wage_1 = player.participant.vars['worker1_wage_tokens'][player.round_number - 2]
                wage_2 = 999
        if num_workers == 2:
            effort_given_1 = player.participant.vars['worker1_effort_given'][player.round_number - 2]
            effort_given_1_string = session.config['effort_names'][effort_given_1]
            effort_given_2 = player.participant.vars['worker2_effort_given'][player.round_number - 2]
            effort_given_2_string = session.config['effort_names'][effort_given_2]
            if player.participant.currency_is_points:
                max_wage = session.config['max_wage']
                wage_1 = player.participant.vars['worker1_wage_points'][player.round_number - 2]
                wage_2 = player.participant.vars['worker2_wage_points'][player.round_number - 2]
            else:
                max_wage = session.config['max_wage'] * session.config['exchange_rate']
                wage_1 = player.participant.vars['worker1_wage_tokens'][player.round_number - 2]
                wage_2 = player.participant.vars['worker2_wage_tokens'][player.round_number - 2]

        name_low_effort = session.config['effort_names'][0]
        name_high_effort = session.config['effort_names'][1]
        currency_plural = "points" if player.participant.currency_is_points else "tokens"

        return dict(
            currency_plural=currency_plural,
            max_wage=int(max_wage),
            wage_1=int(wage_1),
            wage_2=int(wage_2),
            effort_given_1_string=effort_given_1_string,
            effort_given_2_string=effort_given_2_string,
            num_workers=num_workers,
            name_low_effort=name_low_effort,
            name_high_effort=name_high_effort,
            playerID=player.participant.vars['playerID'],
        )

    @staticmethod
    def live_method(player: Player, data):
        session = player.session
        group = player.group

        print('Reemploy live_method', player.participant.vars['playerID'], data)

        if data['information_type'] == 'private_offer':
            if data['currency_is_points'] is True:
                wage_points = data['wage']
                wage_tokens = session.config['exchange_rate'] * wage_points
            else:
                wage_tokens = data['wage']
                wage_points = wage_tokens / session.config['exchange_rate']
            current_datetime = datetime.datetime.now()
            Offer.create(
                group=group,
                marketID=group.marketID,
                round_number=player.round_number,
                private=True,
                employer_id=data['employer_id'],
                worker_id=data['worker_id'],
                wage_points=wage_points,
                wage_tokens=wage_tokens,
                effort=data['effort'],
                status='open',
                show=True,
                effort_given=None,
                job_id=int(str(9) + str(group.marketID) + str(player.round_number) + str(group.prvt_job_offer_counter)),
                job_number=data['job_number'],
                timestamp_created=current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            )
        string_effort = session.config['effort_names'][data['effort']]
        players = group.get_players()

        for p in players:
            if p.participant.playerID == data['employer_id']:
                id = p.id_in_group

        return {id:
                    {'information_type': 'received',
                     'wage_points': wage_points,
                     'wage_tokens': wage_tokens,
                     'effort': data['effort'],
                     'string_effort': string_effort,
                     'job_number': data['job_number']}
                }


class WaitToStart(WaitPage):
    template_name = '_templates/includes/My_WaitPage.html'
    body_text = "Waiting for other players in your group to arrive."


class Countdown(Page):
    timer_text = 'The next market phase will start in:'

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['countdown_seconds']


class MarketPage(Page):
    timer_text = 'The market phase will end in:'

    @staticmethod
    def is_displayed(player: Player):
        return not player.is_finished

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['market_timeout_seconds']

    @staticmethod
    def after_all_players_arrive(group: Group):
        current_datetime = datetime.datetime.now()
        group.start_timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        group = player.group
        players_in_group = group.players_in_group
        employers_in_group = group.employers_in_group

        if player.participant.vars['currency_is_points'] is True:
            max_wage = session.config['max_wage']
        else:
            max_wage = session.config['max_wage'] * session.config['exchange_rate']

        name_low_effort = session.config['effort_names'][0]
        name_high_effort = session.config['effort_names'][1]

        return dict(max_wage=max_wage,
                    players_in_group=players_in_group,
                    employers_in_group=employers_in_group,
                    num_workers=players_in_group - employers_in_group,
                    round_number=player.round_number,
                    playerID=player.participant.vars['playerID'],
                    string_role=player.participant.vars['string_role'],
                    name_low_effort=name_low_effort,
                    name_high_effort=name_high_effort, )

    @staticmethod
    def js_vars(player: Player):
        session = player.session
        if player.participant.vars['currency_is_points'] is True:
            max_wage = session.config['max_wage']
        else:
            max_wage = session.config['max_wage'] * session.config['exchange_rate']
        name_low_effort = session.config['effort_names'][0]
        name_high_effort = session.config['effort_names'][1]
        return dict(max_wage=max_wage,
                    my_id=player.participant.vars['playerID'],
                    is_employer=player.participant.vars['is_employer'],
                    string_role=player.participant.vars['string_role'],
                    currency_is_points=player.participant.vars['currency_is_points'],
                    name_low_effort=name_low_effort,
                    name_high_effort=name_high_effort, )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.is_finished = True

    live_method = market_live_method


class WorkPage(Page):
    form_model = 'player'
    form_fields = ['effort_choice']

    @staticmethod
    def is_displayed(player: Player):
        return player.is_employed

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        name_high_effort = session.config['effort_names'][1]
        name_low_effort = session.config['effort_names'][0]
        if player.field_maybe_none('effort_requested') == 1:
            effort_requested = name_high_effort
        elif player.field_maybe_none('effort_requested') == 0:
            effort_requested = name_low_effort
        else:
            raise Exception('effort_requested not 0 or 1')
            effort_requested = "error"
        return dict(
            is_employer=player.participant.vars['is_employer'],
            string_role=player.participant.vars['string_role'],
            wage_received_points=player.wage_received_points,
            wage_received_tokens=player.wage_received_tokens,
            effort_requested=effort_requested,
            effort_cost_points_0=session.config['effort_costs_points'][0],
            effort_cost_points_1=session.config['effort_costs_points'][1],
            effort_cost_tokens_0=session.config['effort_costs_points'][0] * session.config['exchange_rate'],
            effort_cost_tokens_1=session.config['effort_costs_points'][1] * session.config['exchange_rate'],
            name_low_effort=name_low_effort,
            name_high_effort=name_high_effort,
        )


class ResultsWaitPage(WaitPage):
    template_name = '_templates/includes/My_WaitPage.html'
    body_text = "Waiting for workers to finish the effort stage."

    @staticmethod
    def after_all_players_arrive(group: Group):
        players = group.get_players()

        offers = Offer.filter(group=group)
        accepted_offers = Offer.filter(group=group, status='accepted')

        # First update the offers
        for p in players:
            session = p.session
            for o in accepted_offers:
                if p.participant.playerID == o.worker_id:
                    o.effort_given = p.effort_choice

        # Calculate averages directly from the offers
        group.average_wage_points = sum([p.wage_received_points for p in players if p.is_employed]) / sum(
            [p.is_employed for p in players]) if sum([p.is_employed for p in players]) > 0 else 0
        group.average_wage_tokens = sum([p.wage_received_tokens for p in players if p.is_employed]) / sum(
            [p.is_employed for p in players]) if sum([p.is_employed for p in players]) > 0 else 0
        group.average_effort = sum([p.effort_choice for p in players if p.is_employed]) / sum(
            [p.is_employed for p in players]) if sum([p.is_employed for p in players]) > 0 else 0

        for p in players:
            p.average_wage_points = group.average_wage_points
            p.average_wage_tokens = group.average_wage_tokens
            p.average_effort = group.average_effort

        # Get the player data from the offers (Note: this is ugly, but I want to store everything in participant to manage re-employment in the following round)
        for p in players:
            p.participant.vars['round_number'] = p.round_number
            p.participant.vars['round_for_points'].append(p.participant.vars['currency_is_points'])
            if p.participant.vars.get('is_employer'):
                p.participant.vars['num_workers'].append(p.num_workers_employed)

                # Check that everything works
                matching_offers = [o for o in offers if
                                   p.participant.playerID == o.employer_id and o.status == 'accepted']
                if len(matching_offers) != p.num_workers_employed:
                    raise Exception('Number of matching offers does not match the number of workers employed' + str(
                        p.num_workers_employed) + ' ' + str(len(matching_offers)) + ' ' + str(p.participant.playerID))
                if len(matching_offers) > 2 or len(matching_offers) < 0:
                    raise Exception('Number of matching offers is not 1 or 2' + str(p.num_workers_employed) + ' ' + str(
                        len(matching_offers)) + ' ' + str(p.participant.playerID))
                if p.num_workers_employed > 2 or p.num_workers_employed < 0:
                    raise Exception(
                        'Number of employed workers is not 1 or 2' + str(p.num_workers_employed) + ' ' + str(
                            len(matching_offers)) + ' ' + str(p.participant.playerID))

                if p.num_workers_employed == 0:
                    for i in range(1, 3):
                        for variable_suffix in ['wage_points', 'wage_tokens', 'effort_given', 'effort', 'id',
                                                'profit_points', 'profit_tokens']:
                            p.participant.vars[f'worker{i}_{variable_suffix}'].append('NA')

                elif p.num_workers_employed == 1:
                    p.participant.vars['worker2_wage_points'].append('NA')
                    p.participant.vars['worker2_wage_tokens'].append('NA')
                    p.participant.vars['worker2_effort_given'].append('NA')
                    p.participant.vars['worker2_effort'].append('NA')
                    p.participant.vars['worker2_id'].append('NA')
                    p.participant.vars['worker2_profit_points'].append('NA')
                    p.participant.vars['worker2_profit_tokens'].append('NA')
                    for o in matching_offers:
                        p.participant.vars['worker1_wage_points'].append(o.wage_points)
                        p.participant.vars['worker1_wage_tokens'].append(o.wage_tokens)
                        p.participant.vars['worker1_effort_given'].append(o.effort_given)
                        p.participant.vars['worker1_effort'].append(o.effort)
                        p.participant.vars['worker1_id'].append(o.worker_id)
                        worker1_profit_points = o.wage_points - session.config['effort_costs_points'][o.effort_given]
                        worker1_profit_tokens = o.wage_tokens - session.config['effort_costs_points'][o.effort_given] * \
                                                session.config['exchange_rate']
                        p.participant.vars['worker1_profit_points'].append(worker1_profit_points)
                        p.participant.vars['worker1_profit_tokens'].append(worker1_profit_tokens)
                        p.total_effort_received += o.effort_given
                elif p.num_workers_employed == 2:
                    p.worker_counter = 0
                    for o in matching_offers:
                        p.total_effort_received += o.effort_given
                        p.worker_counter += 1
                        if p.worker_counter == 1:
                            p.participant.vars['worker1_wage_points'].append(o.wage_points)
                            p.participant.vars['worker1_wage_tokens'].append(o.wage_tokens)
                            p.participant.vars['worker1_effort_given'].append(o.effort_given)
                            p.participant.vars['worker1_effort'].append(o.effort)
                            p.participant.vars['worker1_id'].append(o.worker_id)
                            worker1_profit_points = o.wage_points - session.config['effort_costs_points'][
                                o.effort_given]
                            worker1_profit_tokens = o.wage_tokens - session.config['effort_costs_points'][
                                o.effort_given] * session.config['exchange_rate']
                            p.participant.vars['worker1_profit_points'].append(worker1_profit_points)
                            p.participant.vars['worker1_profit_tokens'].append(worker1_profit_tokens)
                        elif p.worker_counter == 2:
                            p.participant.vars['worker2_wage_points'].append(o.wage_points)
                            p.participant.vars['worker2_wage_tokens'].append(o.wage_tokens)
                            p.participant.vars['worker2_effort_given'].append(o.effort_given)
                            p.participant.vars['worker2_effort'].append(o.effort)
                            p.participant.vars['worker2_id'].append(o.worker_id)
                            worker2_profit_points = o.wage_points - session.config['effort_costs_points'][
                                o.effort_given]
                            worker2_profit_tokens = o.wage_tokens - session.config['effort_costs_points'][
                                o.effort_given] * session.config['exchange_rate']
                            p.participant.vars['worker2_profit_points'].append(worker2_profit_points)
                            p.participant.vars['worker2_profit_tokens'].append(worker2_profit_tokens)

            else:  # Workers
                p.participant.vars['num_workers'].append('NA')
                p.participant.vars['worker1_wage_points'].append('NA')
                p.participant.vars['worker1_wage_tokens'].append('NA')
                p.participant.vars['worker1_effort_given'].append('NA')
                p.participant.vars['worker1_effort'].append('NA')
                p.participant.vars['worker1_id'].append('NA')
                p.participant.vars['worker1_profit_points'].append('NA')
                p.participant.vars['worker1_profit_tokens'].append('NA')
                p.participant.vars['worker2_wage_points'].append('NA')
                p.participant.vars['worker2_wage_tokens'].append('NA')
                p.participant.vars['worker2_effort_given'].append('NA')
                p.participant.vars['worker2_effort'].append('NA')
                p.participant.vars['worker2_id'].append('NA')
                p.participant.vars['worker2_profit_points'].append('NA')
                p.participant.vars['worker2_profit_tokens'].append('NA')

        # Get the total effort received (Note: I already have total wage from market page)
        for p in players:
            if p.participant.vars['is_employer']:
                if p.num_workers_employed == 0:
                    p.effort_worth_points = 0
                elif p.num_workers_employed == 1:
                    if p.total_effort_received == 0:
                        p.effort_worth_points = session.config['MPL_low'][0]
                    elif p.total_effort_received == 1:
                        p.effort_worth_points = session.config['MPL_high'][0]
                    else:
                        raise Exception('Error: wrong effort received')
                elif p.num_workers_employed == 2:
                    if p.total_effort_received == 0:  # if effort_received is 0, then both workers gave low effort
                        p.effort_worth_points = 2 * session.config['MPL_low'][1]
                    elif p.total_effort_received == 1:  # if effort_received is 1, then one worker gave high effort
                        p.effort_worth_points = session.config['MPL_high'][1] + session.config['MPL_low'][1]
                    elif p.total_effort_received == 2:
                        p.effort_worth_points = 2 * session.config['MPL_high'][
                            1]  # if effort_received is 2, then both workers gave high effort
                    else:
                        raise Exception('Error: wrong effort received')
                else:
                    raise Exception('Error: employed', p.num_workers_employed, 'workers')
                p.effort_worth_tokens = p.effort_worth_points * session.config['exchange_rate']

        # Update the profits
        for p in players:
            p.participant.vars['round_for_points'].append(p.participant.vars['currency_is_points'])
            if not p.participant.vars.get('is_employer'):  # Worker profits
                if p.is_employed:
                    p.effort_cost_points = session.config['effort_costs_points'][p.effort_choice]
                    p.effort_cost_tokens = session.config['effort_costs_points'][p.effort_choice] * session.config[
                        'exchange_rate']
                    p.payoff_tokens = p.wage_received_tokens - p.effort_cost_tokens
                    p.payoff_points = p.wage_received_points - p.effort_cost_points
                else:
                    p.payoff_tokens = 0
                    p.payoff_points = 0
            elif p.participant.vars.get('is_employer'):  # Employer profits
                p.payoff_tokens = p.effort_worth_tokens - p.total_wage_paid_tokens
                p.payoff_points = p.effort_worth_points - p.total_wage_paid_points

            p.participant.vars['total_points'].append(p.payoff_points)
            p.participant.vars['total_tokens'].append(p.payoff_tokens)

        # Now update the profits of your employer (to show on the results page)
        for p in players:
            if not p.participant.vars.get('is_employer'):
                others = p.get_others_in_group()
                try:
                    p.employer_payoff_points = [o.payoff_points for o in others if
                                                o.participant.playerID == p.field_maybe_none('matched_with_id')][0]
                    p.employer_payoff_tokens = [o.payoff_tokens for o in others if
                                                o.participant.playerID == p.field_maybe_none('matched_with_id')][0]
                except (KeyError, IndexError) as e:
                    p.employer_payoff_points = None
                    p.employer_payoff_tokens = None

        group.average_payoff_firms_points = sum(
            [p.payoff_points for p in players if p.participant.vars.get('is_employer')]) / sum(
            [p.participant.vars.get('is_employer') for p in players]) if sum(
            [p.participant.vars.get('is_employer') is True for p in players]) > 0 else 0
        group.average_payoff_firms_tokens = sum(
            [p.payoff_tokens for p in players if p.participant.vars.get('is_employer') ]) / sum(
            [p.participant.vars.get('is_employer') is True for p in players]) if sum(
            [p.participant.vars.get('is_employer') is True for p in players]) > 0 else 0
        group.average_payoff_workers_points = sum(
            [p.payoff_points for p in players if not p.participant.vars.get('is_employer') ]) / sum(
            [p.participant.vars.get('is_employer') is False for p in players]) if sum(
            [p.participant.vars.get('is_employer') is False for p in players]) > 0 else 0
        group.average_payoff_workers_tokens = sum(
            [p.payoff_tokens for p in players if not p.participant.vars.get('is_employer') ]) / sum(
            [p.participant.vars.get('is_employer') is False for p in players]) if sum(
            [p.participant.vars.get('is_employer') is False for p in players]) > 0 else 0


class Results(Page):
    form_model = 'player'
    timeout_seconds = 60

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        session = player.session

        name_high_effort = session.config['effort_names'][1]
        name_low_effort = session.config['effort_names'][0]

        total_low_effort = player.num_workers_employed - player.total_effort_received if player.total_effort_received is not None else None
        average_effort = int(group.field_maybe_none('average_effort') * 100) if group.field_maybe_none(
            'average_effort') is not None else None
        effort_string = name_high_effort if player.field_maybe_none('effort_choice') == 1 else (
            name_low_effort if player.field_maybe_none('effort_choice') == 0 else "")
        round_number = player.round_number
        if round_number <= session.config['shock_after_rounds']:
            rounds_left = session.config['shock_after_rounds'] - round_number
            part = 1
        else:
            rounds_left = C.NUM_ROUNDS - round_number
            part = 2

        average_wage_points = round(group.average_wage_points, 1) if group.average_wage_points is not None else None
        average_wage_tokens = round(group.average_wage_tokens, 1) if group.average_wage_tokens is not None else None
        average_profit_points = round(group.average_payoff_firms_points,
                                      1) if group.average_payoff_firms_points is not None else None
        average_profit_tokens = round(group.average_payoff_firms_tokens,
                                      1) if group.average_payoff_firms_tokens is not None else None
        average_income_points = round(group.average_payoff_workers_points,
                                      1) if group.average_payoff_workers_points is not None else None
        average_income_tokens = round(group.average_payoff_workers_tokens,
                                      1) if group.average_payoff_workers_tokens is not None else None

        if player.participant.vars['currency_is_points'] is True:
            effort_worth = player.field_maybe_none('effort_worth_points')
        else:
            effort_worth = player.field_maybe_none('effort_worth_tokens')

        if player.participant.vars['worker1_effort'][player.round_number - 1] == 1:
            worker1_effort = name_high_effort
        elif player.participant.vars['worker1_effort'][player.round_number - 1] == 0:
            worker1_effort = name_low_effort
        else:
            worker1_effort = 'NA'

        if player.participant.vars['worker1_effort_given'][player.round_number - 1] == 1:
            worker1_effort_given = name_high_effort
        elif player.participant.vars['worker1_effort_given'][player.round_number - 1] == 0:
            worker1_effort_given = name_low_effort
        else:
            worker1_effort_given = 'NA'

        if player.participant.vars['worker2_effort'][player.round_number - 1] == 1:
            worker2_effort = name_high_effort
        elif player.participant.vars['worker2_effort'][player.round_number - 1] == 0:
            worker2_effort = name_low_effort
        else:
            worker2_effort = 'NA'

        if player.participant.vars['worker2_effort_given'][player.round_number - 1] == 1:
            worker2_effort_given = name_high_effort
        elif player.participant.vars['worker2_effort_given'][player.round_number - 1] == 0:
            worker2_effort_given = name_low_effort
        else:
            worker2_effort_given = 'NA'

        worker1_wage_points = player.participant.vars['worker1_wage_points'][player.round_number - 1]
        worker1_wage_tokens = player.participant.vars['worker1_wage_tokens'][player.round_number - 1]
        worker1_payoff_points = player.participant.vars['worker1_profit_points'][player.round_number - 1]
        worker1_payoff_tokens = player.participant.vars['worker1_profit_tokens'][player.round_number - 1]
        worker1_id = player.participant.vars['worker1_id'][player.round_number - 1]
        worker2_wage_points = player.participant.vars['worker2_wage_points'][player.round_number - 1]
        worker2_wage_tokens = player.participant.vars['worker2_wage_tokens'][player.round_number - 1]
        worker2_payoff_points = player.participant.vars['worker2_profit_points'][player.round_number - 1]
        worker2_payoff_tokens = player.participant.vars['worker2_profit_tokens'][player.round_number - 1]
        worker2_id = player.participant.vars['worker2_id'][player.round_number - 1]

        if player.num_workers_employed == 0:
            worker1_effort_worth = 0
            worker2_effort_worth = 0
        elif player.num_workers_employed == 1 or player.num_workers_employed == 2:
            worker1_effort_worth = session.config['MPL_high'][
                player.num_workers_employed - 1] if worker1_effort_given == 'Normal' else session.config['MPL_low'][
                player.num_workers_employed - 1] if worker1_effort_given == 'Low' else 0
            worker2_effort_worth = session.config['MPL_high'][
                player.num_workers_employed - 1] if worker2_effort_given == 'Normal' else session.config['MPL_low'][
                player.num_workers_employed - 1] if worker2_effort_given == 'Low' else 0
        else:
            raise Exception('num_workers_employed is not 0, 1 or 2')

        if player.participant.vars['currency_is_points'] is False:
            worker1_effort_worth = round(worker1_effort_worth * session.config['exchange_rate'], 1)
            worker2_effort_worth = round(worker2_effort_worth * session.config['exchange_rate'], 1)

        return dict(
            worker1_effort_worth=worker1_effort_worth,
            worker2_effort_worth=worker2_effort_worth,
            name_low_effort=name_low_effort,
            name_high_effort=name_high_effort,
            round_number=round_number,
            rounds_left=rounds_left,
            part=part,
            is_employer=player.participant.vars.get('is_employer'),
            is_employed=player.is_employed,
            num_workers=player.num_workers_employed,
            worker_counter=player.field_maybe_none('worker_counter'),
            wage_received_points=player.field_maybe_none('wage_received_points'),
            wage_received_tokens=player.field_maybe_none('wage_received_tokens'),
            total_wage_paid_points=player.field_maybe_none('total_wage_paid_points'),
            total_wage_paid_tokens=player.field_maybe_none('total_wage_paid_tokens'),
            total_effort_received=player.total_effort_received,
            total_low_effort=total_low_effort,
            effort_worth=effort_worth,
            effort_choice=effort_string,
            employer_payoff_points=player.field_maybe_none('employer_payoff_points'),
            employer_payoff_tokens=player.field_maybe_none('employer_payoff_tokens'),
            total_payoff_points=sum(player.participant.vars['total_points']),
            total_payoff_tokens=sum(player.participant.vars['total_tokens']),
            average_wage_points=average_wage_points,
            average_wage_tokens=average_wage_tokens,
            average_profit_points=average_profit_points,
            average_profit_tokens=average_profit_tokens,
            average_income_points=average_income_points,
            average_income_tokens=average_income_tokens,
            average_effort=average_effort,
            num_unmatched_workers=group.field_maybe_none('num_unmatched_workers'),
            worker1_effort=worker1_effort,
            worker1_effort_given=worker1_effort_given,
            worker1_id=worker1_id,
            worker1_wage_points=worker1_wage_points,
            worker1_wage_tokens=worker1_wage_tokens,
            worker1_payoff_points=worker1_payoff_points,
            worker1_payoff_tokens=worker1_payoff_tokens,
            worker2_effort=worker2_effort,
            worker2_effort_given=worker2_effort_given,
            worker2_id=worker2_id,
            worker2_wage_points=worker2_wage_points,
            worker2_wage_tokens=worker2_wage_tokens,
            worker2_payoff_points=worker2_payoff_points,
            worker2_payoff_tokens=worker2_payoff_tokens,
        )


class MidPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == player.session.config['shock_after_rounds'] + 1


class AnotherIntroduction(MidPage):
    pass


class AnotherInstruction(MidPage):

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        group = player.group

        name_low_effort = session.config['effort_names'][0]
        name_high_effort = session.config['effort_names'][1]

        average_wage = sum(
            [p.field_maybe_none('average_wage_points') or 0 for p in player.in_previous_rounds()]) / session.config.get(
            'shock_after_rounds')
        average_effort = (sum([p.average_effort for p in player.in_previous_rounds()]) * 100) / session.config.get(
            'shock_after_rounds')
        average_wage = 0 if average_wage is None else int(average_wage)
        average_effort = 0 if average_effort is None else int(average_effort)
        effort_caller = math.floor(average_wage / 5) - 1
        print(effort_caller)
        print('$' * 100)
        predicted_effort = session.config['predicted_effort'][effort_caller]

        if player.participant.vars.get('small_market') is True:
            average_wage = 0
            average_effort = 0
            predicted_effort = 0

        income_diff = False if session.config.get('exchange_rate') == 1 else True

        if player.participant.vars.get('large_market_1') or player.participant.vars.get('move_to_market_1'):
            size_market = session.config.get('size_large_market', 0) + session.config.get('migration_small_shock_size',
                                                                                          0)
            num_employers = session.config.get('num_employers_large_market', 0)
            num_workers = session.config.get('size_large_market', 0) + session.config.get('migration_small_shock_size',
                                                                                          0) - \
                          session.config.get('num_employers_large_market', 0)
            shock_size = session.config.get('migration_small_shock_size', 0)
        elif player.participant.vars.get('large_market_2') or player.participant.vars.get('move_to_market_2'):
            size_market = session.config.get('size_small_market', 0) + session.config.get('migration_large_shock_size',
                                                                                          0)
            num_employers = session.config.get('num_employers_large_market', 0)
            num_workers = session.config.get('size_small_market', 0) + session.config.get('migration_large_shock_size',
                                                                                          0) - \
                          session.config.get('num_employers_large_market', 0)
            shock_size = session.config.get('migration_large_shock_size', 0)
        else:
            size_market = session.config.get('size_small_market', 0)
            num_employers = session.config.get('num_employers_small_market', 0)
            num_workers = session.config.get('size_small_market', 0) - session.config.get('num_employers_small_market',
                                                                                          0) - \
                          2 * session.config.get('migration_large_shock_size', 0)
            shock_size = 0

        res = dict(
            skip_game=player.participant.vars.get('skip_game', False),
            income_diff=income_diff,
            size_market=size_market,
            num_employers=num_employers,
            num_workers=num_workers,
            is_employer=player.participant.vars.get('is_employer'),
            shock_size=shock_size,
            name_low_effort=name_low_effort,
            name_high_effort=name_high_effort,
            num_rounds_left=C.NUM_ROUNDS - (session.config.get('shock_after_rounds', C.NUM_ROUNDS)),
            migrant=player.participant.vars.get('migrant'),
            average_wage=average_wage,
            average_effort=average_effort,
            predicted_effort=predicted_effort,
            large_market=player.participant.vars.get('large_market'),
        )
        pprint(res)
        print('$' * 100)
        return res

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if (player.session.config.get('shock_after_rounds') + 1 == player.round_number and
                player.participant.vars.get('skip_game')):
            player.skip_game = True

    @staticmethod
    def app_after_this_page(player, upcoming_apps):

        if (player.session.config.get('shock_after_rounds') + 1 == player.round_number and
                player.participant.vars.get('skip_game')):
            return upcoming_apps[0]


class AnotherWaitPage(WaitPage):
    template_name = '_templates/includes/My_WaitPage.html'
    body_text = "Please wait, part 2 will begin shortly."

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == player.session.config['shock_after_rounds'] + 1


page_sequence = [
    AnotherIntroduction,
    AnotherInstruction,
    AnotherWaitPage,
    CheckReemploy,
    Reemploy,
    WaitToStart,
    Countdown,
    MarketPage,
    WorkPage,
    ResultsWaitPage,
    Results,

]


def custom_export(players):
    # top row
    yield ['session_code', 'group.id_in_subsession', 'marketID', 'round', 'job_id', 'employer_id', 'worker_id',
           'private',
           'wage_points', 'wage_tokens', 'effort', 'effort_given', 'status', 'timestamp_created', 'timestamp_accepted',
           'timestamp_cancelled']

    # data rows
    offers = Offer.filter()
    for offer in offers:
        yield [offer.group.session.code, offer.group.id_in_subsession, offer.marketID, offer.round_number, offer.job_id,
               offer.employer_id, offer.worker_id, offer.private, offer.wage_points, offer.wage_tokens,
               offer.effort, offer.effort_given, offer.status, offer.timestamp_created, offer.timestamp_accepted,
               offer.timestamp_cancelled]
