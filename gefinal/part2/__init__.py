from otree.api import *
import time


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'part2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    large_market = models.BooleanField()
    is_finished = models.BooleanField(initial=False)
    num_job_offers = models.IntegerField(initial=0)
    num_unmatched_workers = models.IntegerField()
    start_timestamp = models.FloatField()
    average_wage = models.CurrencyField()
    average_effort = models.FloatField()


class Player(BasePlayer):
    num_workers_employed = models.IntegerField(initial=0, min=0, max=3)                                                 # Counter for number of workers the firm employed
    max_workers = models.BooleanField(initial=False)                                                                    # Boolean for whether the firm has reached its maximum number of workers
    total_wage_paid = models.IntegerField(initial=0)                                                                    # Total wage paid by the firm
    total_effort_received = models.IntegerField(initial=0)                                                              # Total effort received by the firm
    is_employed = models.BooleanField(initial=False)                                                                    # Boolean for whether the worker is employed
    wage_received = models.IntegerField(min=0, max=100)                                                                 # Wage the worker received by the firm
    effort_requested = models.IntegerField(min=1, max=10)                                                               # Effort level the firm requested from the worker
    effort_choice = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],                                        # Effort choice of the worker
                                        widget=widgets.RadioSelectHorizontal,
                                        label="Please choose an effort level:")
    effort_cost = models.IntegerField()                                                                                 # Effort cost equivalent to the effort level
    matched_with_id = models.IntegerField()                                                                             # ID of the firm the worker is matched with
    wait = models.BooleanField(initial=False)                                                                           # Show wait page if true
    invalid = models.BooleanField(initial=False)                                                                        # Show job acceptance was invalid alert if true
    happy_effort = models.StringField(
        label="""<p style="margin-top:1cm;">
                    How satisfied are you with the effort choice of the workers? <br> 
                    <i>Please use a scale from 1 to 5, where 1 means you are “completely satisfied” amd 5 means "completely unsatisfied". 
                    You can also use the values in-between to indicate where you fall on the scale.</i>
                </p>""",
        widget=widgets.RadioSelectHorizontal,
        choices=[1, 2, 3, 4, 5]
    )
    happy_wage = models.StringField(
        label="""<p style="margin-top:1cm;">
                    How satisfied are you with the wage you received? <br> 
                    <i>Please use a scale from 1 to 5, where 1 means you are “completely satisfied” amd 5 means "completely unsatisfied". 
                    You can also use the values in-between to indicate where you fall on the scale.</i>
                </p>""",
        widget=widgets.RadioSelectHorizontal,
        choices=[1, 2, 3, 4, 5]
    )


class Offer(ExtraModel):
    group = models.Link(Group)
    round_number = models.IntegerField()
    job_id = models.IntegerField()
    employer_id = models.IntegerField()
    worker_id = models.IntegerField()
    wage = models.IntegerField(min=0, max=100)
    effort = models.IntegerField(min=1, max=10)
    effort_given = models.IntegerField(min=1, max=10)
    status = models.StringField()
    timestamp_created = models.FloatField()
    timestamp_accepted = models.FloatField()
    timestamp_cancelled = models.FloatField()


# FUNCTIONS
def creating_session(subsession: Subsession):
    players_in_all_groups = []
    for group in subsession.get_groups():
        players_in_all_groups.extend(group.get_players())
    #print(players_in_all_groups)

    # group matrix numbers are based on player.id_in_subsession
    players_in_large_market = [p.id_in_subsession for p in players_in_all_groups if p.participant.vars['large_market'] is True or p.participant.vars['migrant'] is True]
    players_in_small_market = [p.id_in_subsession for p in players_in_all_groups if p.participant.vars['large_market'] is False and p.participant.vars['migrant'] is False]

    #print(players_in_large_market)
    #print(players_in_small_market)

    matrix = []
    if players_in_large_market is not []:
        matrix.append(players_in_large_market)
    if players_in_small_market is not []:
        matrix.append(players_in_small_market)

    #print(matrix)
    subsession.set_group_matrix(matrix)

    session = subsession.session
    for group in subsession.get_groups():
        if group.get_players()[0].participant.vars['large_market'] is True or group.get_players()[0].participant.vars['migrant'] is True:
            group.large_market = True
            group.num_unmatched_workers = session.config['size_large_market'] + session.config['migration_shock_size'] - session.config['num_employers_large_market']
        elif group.get_players()[0].participant.vars['large_market'] is False and group.get_players()[0].participant.vars['migrant'] is False:
            group.large_market = False
            group.num_unmatched_workers = session.config['size_small_market'] - session.config['migration_shock_size'] - session.config['num_employers_small_market']


def to_dict(offer: Offer):
    return dict(
        group_id=offer.group_id,
        round_number=offer.round_number,
        job_id=offer.job_id,
        employer_id=offer.employer_id,
        worker_id=offer.worker_id,
        wage=offer.wage,
        effort=offer.effort,
        effort_given=offer.effort_given,
        status=offer.status,
        timestamp_created=offer.timestamp_created,
        timestamp_accepted=offer.timestamp_accepted,
        timestamp_cancelled=offer.timestamp_cancelled,
    )


# PAGES
class WaitForever(WaitPage):
    body_text = "Waiting for other players to finish part 2."
    wait_for_all_groups = True

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars['large_market'] is False and player.participant.vars['migrant'] is False

class WaitToStart(WaitPage):
    #group_by_arrival_time = True
    body_text = "Waiting for other players in your group to arrive."

    @staticmethod
    def after_all_players_arrive(group: Group):
        group.start_timestamp = int(time.time())

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars['large_market'] is True or player.participant.vars['migrant'] is True

class Countdown(Page):
    timer_text = 'The next market stage will start in:'

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['countdown_seconds']

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars['large_market'] is True or player.participant.vars['migrant'] is True

class MarketPage(Page):
    timer_text = 'The market stage will end in:'

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars['large_market'] is True or player.participant.vars['migrant'] is True

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['market_timeout_seconds']

    @staticmethod
    def after_all_players_arrive(group: Group):
        group.start_timestamp = int(time.time())

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        if player.participant.vars['large_market'] is True:
            players_in_group = session.config['size_large_market']
            employers_in_group = session.config['num_employers_large_market']
        else:
            players_in_group = session.config['size_small_market']
            employers_in_group = session.config['num_employers_small_market']
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
                    string_role=player.participant.vars['string_role'],)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.group.is_finished = True

    @staticmethod
    def live_method(player: Player, data):
        group = player.group
        if data['information_type'] == 'offer':
            group.num_job_offers += 1
            Offer.create(
                group=group,
                round_number=player.round_number,
                job_id=int(str(player.group.id_in_subsession) + str(group.num_job_offers)),
                employer_id=player.participant.playerID,
                worker_id=None,
                wage=data['wage'],
                effort=data['effort'],
                effort_given=None,
                status='open',
                timestamp_created=int(time.time()),
                timestamp_accepted=None,
                timestamp_cancelled=None,
            )
            for p in group.get_players():
                if p.participant.playerID == data['employer_id']:
                    p.wait = True
        elif data['information_type'] == 'accept':
            current_offer = Offer.filter(group=group, job_id=data['job_id'])
            if current_offer[0].status == 'open':
                group.num_job_offers -= 1
                group.num_unmatched_workers -= 1
                if group.num_unmatched_workers == 0:
                    group.is_finished = True
                for o in current_offer:
                    o.status = 'accepted'
                    o.worker_id = player.participant.playerID
                    o.timestamp_accepted = int(time.time())
                for p in group.get_players():
                    if p.participant.playerID == data['employer_id']:
                        p.num_workers_employed += 1
                        p.total_wage_paid += data['wage']
                        p.wait = False
                        if p.num_workers_employed == 3:
                            p.max_workers = True
                    if p.participant.playerID == data['worker_id']:
                        p.is_employed = True
                        p.wait = True
                        p.wage_received = data['wage']
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
                o.timestamp_cancelled = int(time.time())
            for p in group.get_players():
                if p.participant.playerID == data['employer_id']:
                    p.wait = False
        elif data['information_type'] == 'load':
            pass
        else:
            print('unknown message type: ', data['information_type'])

        offers_to_show = sorted(Offer.filter(group=group), key=lambda o: o.job_id, reverse=True)
        offers_list = [to_dict(o) for o in offers_to_show]

        market_information = dict(workers_left=group.num_unmatched_workers,
                                  open_offers=sum(i['status'] == 'open' for i in offers_list),
                                  average_wage=sum(i['wage'] for i in offers_list) / len(offers_list) if len(offers_list) > 0 else 0,
                                  average_effort=sum(i['effort'] for i in offers_list) / len(offers_list) if len(offers_list) > 0 else 0,
                                  )

        data_to_return = {
            p.id_in_group: dict(
                page_information=dict(is_finished=group.is_finished,
                                      max_workers=p.max_workers,
                                      wait=p.wait,
                                      invalid=p.invalid,
                                      ),
                market_information=market_information,
                offers=offers_list,
            )
            for p in group.get_players()
        }
        return data_to_return

class WorkPage(Page):
    form_model = 'player'
    form_fields = ['effort_choice']

    @staticmethod
    def is_displayed(player: Player):
        if player.is_employed and player.participant.vars['large_market'] is True:
            return True
        elif player.is_employed and player.participant.vars['migrant'] is True:
            return True
        else:
            return False

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            is_employer=player.participant.vars['is_employer'],
            string_role=player.participant.vars['string_role'],
            wage_received=player.wage_received,
            effort_requested=player.effort_requested,
            matched_with_id=player.matched_with_id,
        )


class ResultsWaitPage(WaitPage):
    body_text = "Waiting for workers to finish the effort stage."

    @staticmethod
    def after_all_players_arrive(group: Group):
        players = group.get_players()
        offers = Offer.filter(group=group)
        effort_costs = {1: 0, 2: 1, 3: 2, 4: 4, 5: 6, 6: 8, 7: 10, 8: 12, 9: 15, 10: 18}

        group.average_wage = sum([p.wage_received for p in players if p.is_employed]) / sum([p.is_employed for p in players]) if sum([p.is_employed for p in players]) > 0 else 0
        group.average_effort = sum([p.effort_choice for p in players if p.is_employed]) / sum([p.is_employed for p in players]) if sum([p.is_employed for p in players]) > 0 else 0

        for o in offers:
            o.effort_given = [p.effort_choice for p in players if p.participant.playerID == o.worker_id and o.status == 'accepted'][0]
        for p in players:
            session = p.session
            exchange_rate = session.config['exchange_rate_large_market'] if session.config['large_market'] or session.config['migrant'] else session.config['exchange_rate_small_market']
            if p.participant.is_employer is True:
                p.total_effort_received = sum([o.effort_given for o in offers if o.employer_id == p.participant.playerID])
                p.total_wage_paid = sum([o.wage for o in offers if o.employer_id == p.participant.playerID])
                if p.num_workers_employed == 0:
                    p.payoff = 0
                    real_pay = p.payoff * exchange_rate
                    p.participant.vars['realpay'].append(real_pay)
                elif 0 < p.num_workers_employed < 4:
                    p.payoff = session.config['MPL'][p.num_workers_employed - 1] * p.total_effort_received - p.total_wage_paid
                    real_pay = p.payoff * exchange_rate
                    p.participant.vars['realpay'].append(real_pay)
                else:
                    print('Player', p.participant.playerID, 'had too many workers!')
            else:
                if p.is_employed:
                    effort_cost = effort_costs[p.effort_choice]
                    p.payoff = p.wage_received - effort_cost
                    real_pay = p.payoff * exchange_rate
                    p.participant.vars['realpay'].append(real_pay)
                else:
                    p.payoff = 5
                    real_pay = p.payoff * exchange_rate
                    p.participant.vars['realpay'].append(real_pay)

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars['large_market'] is True or player.participant.vars['migrant'] is True


class Results(Page):
    form_model = 'player'
    form_fields = ['happy_effort', 'happy_wage']

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars['large_market'] is True or player.participant.vars['migrant'] is True

    @staticmethod
    def get_form_fields(player):
        if player.participant.vars['is_employer']:
            return ['happy_effort']
        else:
            return ['happy_wage']

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.round_number >= player.session.config['shock_after_rounds']:
            return "midbreak"

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        #group.average_wage = 0 if group.average_wage is None else group.average_wage
        #group.average_effort = 0 if group.average_effort is None else group.average_effort
        for p in group.get_players():
            player_in_all_rounds = player.in_all_rounds()
        return dict(
            is_employer=player.participant.is_employer,
            is_employed=player.is_employed,
            num_workers=player.num_workers_employed,
            wage_received=player.field_maybe_none('wage_received'),
            total_wage_paid=player.field_maybe_none('total_wage_paid'),
            total_effort_received=player.total_effort_received,
            effort_choice=player.field_maybe_none('effort_choice'),
            total_payoff=sum([p.payoff for p in player_in_all_rounds]),
            average_wage=group.field_maybe_none('average_wage'),
            average_effort=group.field_maybe_none('average_effort'),
            num_unmatched_workers=group.field_maybe_none('num_unmatched_workers'),
        )



page_sequence = [WaitForever,
                 WaitToStart,
                 Countdown,
                 MarketPage,
                 WorkPage,
                 ResultsWaitPage,
                 Results]


def custom_export(players):
    # top row
    yield ['group', 'round', 'job_id', 'employer_id', 'worker_id', 'wage', 'effort', 'effort_given',
           'status', 'timestamp_created', 'timestamp_accepted', 'timestamp_cancelled']

    # data rows
    offers = Offer.filter()
    for offer in offers:
        yield [offer.group, offer.round_number, offer.job_id, offer.employer_id, offer.worker_id, offer.wage, offer.effort,
               offer.effort_given, offer.status, offer.timestamp_created, offer.timestamp_accepted, offer.timestamp_cancelled]
