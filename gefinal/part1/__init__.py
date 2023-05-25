from otree.api import *
import time
import math


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'part1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    marketID = models.IntegerField()
    large_market = models.BooleanField()
    large_market_1 = models.BooleanField()
    large_market_2 = models.BooleanField()
    is_finished = models.BooleanField(initial=False)
    num_job_offers = models.IntegerField(initial=0)
    job_offer_counter = models.IntegerField(initial=0)
    players_in_group = models.IntegerField()
    employers_in_group = models.IntegerField()
    num_unmatched_workers = models.IntegerField()
    num_unmatched_jobs = models.IntegerField()
    start_timestamp = models.FloatField()
    average_wage_points = models.FloatField()
    average_wage_tokens = models.FloatField()
    average_effort = models.FloatField()


class Player(BasePlayer):
    num_workers_employed = models.IntegerField(initial=0, min=0, max=2)                                                 # Counter for number of workers the firm employed
    total_wage_paid_tokens = models.FloatField(initial=0)                                                             # Total wage paid by the firm (in tokens)
    total_wage_paid_points = models.FloatField(initial=0)                                                             # Total wage paid by the firm (in points)
    total_effort_received = models.IntegerField(initial=0)                                                              # Total effort received by the firm
    effort_worth = models.IntegerField(initial=0)                                                                       # Effort worth of the firm
    payoff_points = models.FloatField(initial=0)                                                                        # Payoff of the firm (in points)
    payoff_tokens = models.FloatField(initial=0)                                                                        # Payoff of the firm (in tokens)
    is_employed = models.BooleanField(initial=False)                                                                    # Boolean for whether the worker is employed
    wage_received_tokens = models.FloatField(min=0)                                                                   # Wage the worker received by the firm (in tokens)
    wage_received_points = models.FloatField(min=0)                                                                   # Wage the worker received by the firm (in points)
    effort_requested = models.IntegerField(min=0, max=1)                                                               # Effort level the firm requested from the worker
    effort_choice = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],                                        # Effort choice of the worker
                                        widget=widgets.RadioSelectHorizontal,
                                        label="Please choose an effort level:")
    effort_cost_points = models.FloatField()                                                                            # Effort cost equivalent to the effort level in points
    effort_cost_tokens = models.FloatField()                                                                            # Effort cost equivalent to the effort level in tokens
    matched_with_id = models.IntegerField()                                                                             # ID of the firm the worker is matched with
    wait = models.BooleanField(initial=False)                                                                           # Show wait page if true (workers)+
    wait1 = models.BooleanField(initial=False)                                                                          # Show wait page if true (employers)
    wait2 = models.BooleanField(initial=False)                                                                          # Show wait page if true (employers)
    accepted1 = models.BooleanField(initial=False)                                                                      # Show job acceptance page if true (workers)
    accepted2 = models.BooleanField(initial=False)                                                                      # Show job acceptance page if true (workers)
    invalid = models.BooleanField(initial=False)                                                                        # Show job acceptance was invalid alert if true
    worker_counter = models.IntegerField()
    worker1_id = models.IntegerField()
    worker2_id = models.IntegerField()
    worker1_wage_tokens = models.FloatField()
    worker2_wage_tokens = models.FloatField()
    worker1_wage_points = models.FloatField()
    worker2_wage_points = models.FloatField()
    worker1_effort = models.IntegerField()
    worker2_effort = models.IntegerField()
    worker1_effort_given = models.IntegerField()
    worker2_effort_given = models.IntegerField()
    happy_effort = models.StringField(
        label="""<p style="margin-top:1cm;">
                    How satisfied are you with the effort choice of the workers? <br> 
                    <i>Please use a scale from 1 to 5, where 1 means you are “completely unsatisfied” and 5 means "completely satisfied". 
                    You can also use the values in-between to indicate where you fall on the scale.</i>
                </p>""",
        choices=['1 - completely unsatisfied',
                 '2 - unsatisfied',
                 '3 - neutral',
                 '4 - satisfied',
                 '5 - completely satisfied']
    )
    happy_wage = models.StringField(
        label="""<p style="margin-top:1cm;">
                    How satisfied are you with the wage you received? <br> 
                    <i>Please use a scale from 1 to 5, where 1 means you are “completely unsatisfied” and 5 means "completely satisfied". 
                    You can also use the values in-between to indicate where you fall on the scale.</i>
                </p>""",
        choices=['1 - completely unsatisfied',
                 '2 - unsatisfied',
                 '3 - neutral',
                 '4 - satisfied',
                 '5 - completely satisfied']
    )


class Offer(ExtraModel):
    group = models.Link(Group)
    marketID = models.IntegerField()
    round_number = models.IntegerField()
    job_id = models.IntegerField()
    employer_id = models.IntegerField()
    worker_id = models.IntegerField()
    wage_points = models.FloatField()
    wage_tokens = models.FloatField()
    effort = models.IntegerField()
    effort_given = models.IntegerField()
    job_number = models.IntegerField()
    status = models.StringField()
    show = models.BooleanField()
    timestamp_created = models.FloatField()
    timestamp_accepted = models.FloatField()
    timestamp_cancelled = models.FloatField()



# FUNCTIONS
def creating_session(subsession: Subsession):
    players_in_all_groups = []
    for group in subsession.get_groups():
        players_in_all_groups.extend(group.get_players())

    # group matrix numbers are based on player.id_in_subsession
    players_in_large_market_1 = [p.id_in_subsession for p in players_in_all_groups if p.participant.vars['large_market_1'] is True or p.participant.vars['large_market_1'] is None]
    players_in_large_market_2 = [p.id_in_subsession for p in players_in_all_groups if p.participant.vars['large_market_2'] is True or p.participant.vars['large_market_2'] is None]
    players_in_small_market = [p.id_in_subsession for p in players_in_all_groups if p.participant.vars['large_market'] is False]

    matrix = []
    if players_in_large_market_1 is not []:
        matrix.append(players_in_large_market_1)
    if players_in_large_market_2 is not []:
        matrix.append(players_in_large_market_2)
    if players_in_small_market is not []:
        matrix.append(players_in_small_market)

    print(matrix)
    subsession.set_group_matrix(matrix)

    session = subsession.session
    for group in subsession.get_groups():
        if group.get_players()[0].participant.vars['large_market_1'] is True:
            group.marketID = 1
            group.large_market = True
            group.large_market_1 = True
            group.large_market_2 = False
            group.players_in_group = session.config['size_large_market']
            group.employers_in_group = session.config['num_employers_large_market']
            group.num_unmatched_workers = group.players_in_group - session.config['num_employers_large_market']
            group.num_unmatched_jobs = session.config['num_employers_large_market'] * 2
        elif group.get_players()[0].participant.vars['large_market_2'] is True:
            group.marketID = 2
            group.large_market = True
            group.large_market_1 = False
            group.large_market_2 = True
            group.players_in_group = session.config['size_large_market']
            group.employers_in_group = session.config['num_employers_large_market']
            group.num_unmatched_workers = group.players_in_group - session.config['num_employers_large_market']
            group.num_unmatched_jobs = session.config['num_employers_large_market'] * 2
        else:
            group.marketID = 3
            group.large_market = False
            group.large_market_1 = False
            group.large_market_2 = False
            group.players_in_group = session.config['size_small_market']
            group.employers_in_group = session.config['num_employers_small_market']
            group.num_unmatched_workers = group.players_in_group - session.config['num_employers_small_market']
            group.num_unmatched_jobs = session.config['num_employers_small_market'] * 2



def to_dict(offer: Offer):
    return dict(
        group_id=offer.group_id,
        marketID=offer.marketID,
        round_number=offer.round_number,
        job_id=offer.job_id,
        employer_id=offer.employer_id,
        worker_id=offer.worker_id,
        wage_points=offer.wage_points,
        wage_tokens=offer.wage_tokens,
        effort=offer.effort,
        effort_given=offer.effort_given,
        status=offer.status,
        show=offer.show,
        job_number=offer.job_number,
        timestamp_created=offer.timestamp_created,
        timestamp_accepted=offer.timestamp_accepted,
        timestamp_cancelled=offer.timestamp_cancelled,
    )


# PAGES
class WaitToStart(WaitPage):
    #group_by_arrival_time = True
    body_text = "Waiting for other players in your group to arrive."

    @staticmethod
    def after_all_players_arrive(group: Group):
        group.start_timestamp = int(time.time())

class Countdown(Page):
    timer_text = 'The next market phase will start in:'

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['countdown_seconds']


class MarketPage(Page):
    timer_text = 'The market phase will end in:'

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['market_timeout_seconds']

    @staticmethod
    def after_all_players_arrive(group: Group):
        group.start_timestamp = int(time.time())

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        players_in_group = group.players_in_group
        employers_in_group = group.employers_in_group

        return dict(players_in_group=players_in_group,
                    employers_in_group=employers_in_group,
                    num_workers=players_in_group - employers_in_group,
                    round_number=player.round_number,
                    playerID=player.participant.vars['playerID'],
                    string_role=player.participant.vars['string_role'])

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.participant.vars['playerID'],
                    is_employer=player.participant.vars['is_employer'],
                    string_role=player.participant.vars['string_role'],
                    currency_is_points=player.participant.vars['currency_is_points'])

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.group.is_finished = True

    @staticmethod
    def live_method(player: Player, data):
        group = player.group
        session = player.session
        player.invalid = False
        print('Received', data)
        if data['information_type'] == 'offer':
            group.job_offer_counter += 1
            group.num_job_offers += 1
            if data['currency_is_points'] is True:
                wage_points = data['wage']
                wage_tokens = session.config['exchange_rate'] * wage_points
            else:
                wage_tokens = data['wage']
                wage_points = wage_tokens / session.config['exchange_rate']
            Offer.create(
                group=group,
                marketID=group.marketID,
                round_number=player.round_number,
                job_id=int(str(group.marketID) + str(player.round_number) + str(group.job_offer_counter)),
                employer_id=player.participant.playerID,
                worker_id=None,
                wage_points=wage_points,
                wage_tokens=wage_tokens,
                effort=data['effort'],
                effort_given=None,
                status='open',
                show=True,
                job_number=data["job_number"],
                timestamp_created=int(time.time()) - group.start_timestamp,
                timestamp_accepted=None,
                timestamp_cancelled=None,
            )

            for p in group.get_players():
                if p.participant.playerID == data['employer_id']:
                    if data["job_number"] == 1:
                        p.wait1 = True
                        p.accepted1 = False
                    elif data["job_number"] == 2:
                        p.wait2 = True
                        p.accepted2 = False
        elif data['information_type'] == 'accept':
            current_offer = Offer.filter(group=group, job_id=data['job_id'])
            if current_offer[0].status == 'open':
                group.num_job_offers -= 1
                group.num_unmatched_workers -= 1
                group.num_unmatched_jobs -= 1
                if group.num_unmatched_workers == 0 or group.num_unmatched_jobs == 0:
                    group.is_finished = True
                for o in current_offer:
                    o.status = 'accepted'
                    o.show = True
                    o.worker_id = player.participant.playerID
                    o.timestamp_accepted = int(time.time()) - group.start_timestamp
                for p in group.get_players():
                    if data['currency_is_points'] is True:
                        wage_points = data['wage']
                        wage_tokens = session.config['exchange_rate'] * wage_points
                    else:
                        wage_tokens = data['wage']
                        wage_points = wage_tokens / session.config['exchange_rate']
                    if p.participant.playerID == data['employer_id']:
                        p.num_workers_employed += 1
                        p.total_wage_paid_tokens += wage_tokens
                        p.total_wage_paid_points += wage_points
                        if data["job_number"] == 1:
                            p.wait1 = False
                            p.accepted1 = True
                        elif data["job_number"] == 2:
                            p.wait2 = False
                            p.accepted2 = True
                    if p.participant.playerID == data['worker_id']:
                        p.is_employed = True
                        p.wait = True
                        p.wage_received_points = wage_points
                        p.wage_received_tokens = wage_tokens
                        p.effort_requested = data['effort']
                        p.matched_with_id = data['employer_id']
            else:
                print('offer already accepted or cancelled')
                player.invalid = True
        elif data['information_type'] == 'cancel':
            group.num_job_offers -= 1
            current_offer = Offer.filter(group=group, job_id=data['job_id'])
            for o in current_offer:
                o.status = 'cancelled'
                o.show = False
                o.timestamp_cancelled = int(time.time()) - group.start_timestamp
            for p in group.get_players():
                if p.participant.playerID == data['employer_id']:
                    if data["job_number"] == 1:
                        p.wait1 = False
                        p.accepted1 = False
                    elif data["job_number"] == 2:
                        p.wait2 = False
                        p.accepted2 = False
        elif data['information_type'] == 'load':
            pass
        else:
            print('unknown message type: ', data['information_type'])

        offers_to_show = sorted(Offer.filter(group=group, show=True), key=lambda o: o.job_id, reverse=True)
        offers_list = [to_dict(o) for o in offers_to_show]

        market_information = dict(workers_left=group.num_unmatched_workers,
                                  open_offers=sum(i['status'] == 'open' for i in offers_list),
                                  average_wage_tokens=sum(i['wage_tokens'] for i in offers_list) / len(offers_list) if len(offers_list) > 0 else 0,
                                  average_wage_points=sum(i['wage_points'] for i in offers_list) / len(offers_list) if len(offers_list) > 0 else 0,
                                  average_effort=sum(i['effort'] for i in offers_list) / len(offers_list) if len(offers_list) > 0 else 0,
                                  )

        data_to_return = {
            p.id_in_group: dict(
                page_information=dict(is_finished=group.is_finished,
                                      wait=p.wait,
                                      wait1=p.wait1,
                                      wait2=p.wait2,
                                      accepted1=p.accepted1,
                                      accepted2=p.accepted2,
                                      invalid=p.invalid,
                                      ),
                market_information=market_information,
                offers=offers_list,
            )
            for p in group.get_players()
        }

        player.invalid = False

        return data_to_return

class WorkPage(Page):
    form_model = 'player'
    form_fields = ['effort_choice']

    @staticmethod
    def is_displayed(player: Player):
        return player.is_employed

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        if player.field_maybe_none('effort_requested') == 1:
            effort_requested = "high"
        elif player.field_maybe_none('effort_requested') == 0:
            effort_requested = "low"
        else:
            print('error: effort_requested not 0 or 1')
            effort_requested = "error"
        return dict(
            is_employer=player.participant.vars['is_employer'],
            string_role=player.participant.vars['string_role'],
            wage_received_points=player.wage_received_points,
            wage_received_tokens=player.wage_received_tokens,
            effort_requested=effort_requested,
            matched_with_id=player.matched_with_id,
            effort_cost_points_0=session.config['effort_costs_points'][0],
            effort_cost_points_1=session.config['effort_costs_points'][1],
            effort_cost_tokens_0=session.config['effort_costs_points'][0] * session.config['exchange_rate'],
            effort_cost_tokens_1=session.config['effort_costs_points'][1] * session.config['exchange_rate'],
        )



class ResultsWaitPage(WaitPage):
    body_text = "Waiting for workers to finish the effort stage."

    @staticmethod
    def after_all_players_arrive(group: Group):
        players = group.get_players()
        offers = Offer.filter(group=group)

        group.average_wage_points = sum([p.wage_received_points for p in players if p.is_employed]) / sum([p.is_employed for p in players]) if sum([p.is_employed for p in players]) > 0 else 0
        group.average_wage_tokens = sum([p.wage_received_tokens for p in players if p.is_employed]) / sum([p.is_employed for p in players]) if sum([p.is_employed for p in players]) > 0 else 0
        group.average_effort = sum([p.effort_choice for p in players if p.is_employed]) / sum([p.is_employed for p in players]) if sum([p.is_employed for p in players]) > 0 else 0

        for p in players:                                                                                               # first update the offers
            session = p.session
            for o in offers:
                if p.participant.playerID == o.worker_id and o.status == 'accepted':
                    o.effort_given = p.effort_choice
        for p in players:                                                                                               # then update the players
            if p.participant.is_employer is True:
                p.worker_counter = 0
                for o in offers:
                    if p.participant.playerID == o.employer_id and o.status == 'accepted':
                        p.worker_counter += 1
                        p.total_effort_received += o.effort_given
                        #p.total_wage_paid_points += o.wage_points                                                      # I was adding the wage twice, once before in the live_method
                        #p.total_wage_paid_tokens += o.wage_tokens
                        if p.worker_counter == 1:
                            p.worker1_wage_points = o.wage_points
                            p.worker1_wage_tokens = o.wage_tokens
                            p.worker1_effort_given = o.effort_given
                            p.worker1_effort = o.effort
                            p.worker1_id = o.worker_id
                        elif p.worker_counter == 2:
                            p.worker2_wage_points = o.wage_points
                            p.worker2_wage_tokens = o.wage_tokens
                            p.worker2_effort = o.effort
                            p.worker2_effort_given = o.effort_given
                            p.worker2_id = o.worker_id
                    else:
                        pass
                if p.num_workers_employed == 0:
                    p.payoff_points = 0
                    p.payoff_tokens = 0
                    p.effort_worth = 0
                    p.participant.vars['total_points'].append(p.payoff_points)
                    p.participant.vars['total_tokens'].append(p.payoff_tokens)
                    p.participant.vars['round_for_points'].append(p.participant.vars['currency_is_points'])
                elif 0 < p.num_workers_employed < 3:
                    mpl = session.config['MPL'][p.num_workers_employed - 1]
                    p.effort_worth = mpl * p.total_effort_received
                    if p.participant.vars['currency_is_points'] is True:
                        p.payoff_points = p.effort_worth - p.total_wage_paid_points
                        p.payoff_tokens = p.payoff_points * session.config['exchange_rate']
                        p.participant.vars['total_points'].append(p.payoff_points)
                        p.participant.vars['total_tokens'].append(p.payoff_tokens)
                        p.participant.vars['round_for_points'].append(p.participant.vars['currency_is_points'])
                    else:
                        p.payoff_tokens = p.effort_worth - p.total_wage_paid_tokens
                        p.payoff_points = p.payoff_tokens / session.config['exchange_rate']
                        p.participant.vars['total_points'].append(p.payoff_points)
                        p.participant.vars['total_tokens'].append(p.payoff_tokens)
                        p.participant.vars['round_for_points'].append(p.participant.vars['currency_is_points'])
                else:
                    print('Player', p.participant.playerID, 'had too many workers!')
            else:
                if p.is_employed:
                    p.effort_cost_points = session.config['effort_costs_points'][p.effort_choice - 1]
                    p.effort_cost_tokens = session.config['effort_costs_points'][p.effort_choice - 1] * session.config['exchange_rate']
                    p.payoff_tokens = p.wage_received_tokens - p.effort_cost_tokens
                    p.payoff_points = p.wage_received_points - p.effort_cost_points
                    p.participant.vars['total_points'].append(p.payoff_points)
                    p.participant.vars['total_tokens'].append(p.payoff_tokens)
                    p.participant.vars['round_for_points'].append(p.participant.vars['currency_is_points'])
                else:
                    p.payoff_tokens = 0
                    p.payoff_points = 0
                    p.participant.vars['total_points'].append(p.payoff_points)
                    p.participant.vars['total_tokens'].append(p.payoff_tokens)
                    p.participant.vars['round_for_points'].append(p.participant.vars['currency_is_points'])
        for p in players:
            print('Player', p.participant.playerID, 'has had point payoffs of', p.participant.vars['total_points'][p.round_number-1], 'and token payoffs of', p.participant.vars['total_tokens'][p.round_number-1], 'and played for points:', p.participant.vars['round_for_points'][p.round_number-1])


class Results(Page):
    form_model = 'player'
    form_fields = ['happy_effort', 'happy_wage']

    @staticmethod
    def get_form_fields(player):
        if player.participant.vars['is_employer'] and player.num_workers_employed > 0:
            return ['happy_effort']
        elif player.is_employed:
            return ['happy_wage']
        else:
            pass

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.round_number >= player.session.config['shock_after_rounds']:
            return "midbreak"

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        #group.average_wage = 0 if group.average_wage is None else group.average_wage
        #group.average_effort = 0 if group.average_effort is None else group.average_effort
        #for p in group.get_players():
        #    player_in_all_rounds = player.in_all_rounds()
        return dict(
            is_employer=player.participant.is_employer,
            is_employed=player.is_employed,
            num_workers=player.num_workers_employed,
            worker_counter=player.field_maybe_none('worker_counter'),
            wage_received_points=player.field_maybe_none('wage_received_points'),
            wage_received_tokens=player.field_maybe_none('wage_received_tokens'),
            total_wage_paid_points=player.field_maybe_none('total_wage_paid_points'),
            total_wage_paid_tokens=player.field_maybe_none('total_wage_paid_tokens'),
            total_effort_received=player.total_effort_received,
            effort_worth=player.field_maybe_none('effort_worth'),
            effort_choice=player.field_maybe_none('effort_choice'),
            total_payoff_points=sum(player.participant.vars['total_points']),
            total_payoff_tokens=sum(player.participant.vars['total_tokens']),
            average_wage_points=group.field_maybe_none('average_wage_points'),
            average_wage_tokens=group.field_maybe_none('average_wage_tokens'),
            average_effort=group.field_maybe_none('average_effort'),
            num_unmatched_workers=group.field_maybe_none('num_unmatched_workers'),
            worker1_wage_points=player.field_maybe_none('worker1_wage_points'),
            worker1_wage_tokens=player.field_maybe_none('worker1_wage_tokens'),
            worker1_effort=player.field_maybe_none('worker1_effort'),
            worker1_effort_given=player.field_maybe_none('worker1_effort_given'),
            worker1_id=player.field_maybe_none('worker1_id'),
            worker2_wage_points=player.field_maybe_none('worker2_wage_points'),
            worker2_wage_tokens=player.field_maybe_none('worker2_wage_tokens'),
            worker2_effort=player.field_maybe_none('worker2_effort'),
            worker2_effort_given=player.field_maybe_none('worker2_effort_given'),
            worker2_id=player.field_maybe_none('worker2_id'),
        )



page_sequence = [WaitToStart,
                 Countdown,
                 MarketPage,
                 WorkPage,
                 ResultsWaitPage,
                 Results]


def custom_export(players):
    # top row
    yield ['session_code', 'group.id_in_subsession', 'round', 'job_id', 'employer_id', 'worker_id', 'wage_points', 'wage_tokens',
           'effort', 'effort_given', 'status', 'timestamp_created', 'timestamp_accepted', 'timestamp_cancelled']

    # data rows
    offers = Offer.filter()
    for offer in offers:
        yield [offer.group.session.code, offer.group.id_in_subsession, offer.round_number, offer.job_id, offer.employer_id, offer.worker_id, offer.wage_points,
               offer.wage_tokens, offer.effort, offer.effort_given, offer.status, offer.timestamp_created, offer.timestamp_accepted, offer.timestamp_cancelled]

