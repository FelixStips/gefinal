from otree.api import *
import random
import datetime

random.seed(10)

doc = """
"""


class C(BaseConstants):
    NAME_IN_URL = 'intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    Q2_WAGE = 70
    Q2_EFFORT_REQUESTED = 1
    Q2_EFFORT_RECEIVED = 1
    Q3_WAGE_1 = 30
    Q3_WAGE_2 = 50
    Q3_EFFORT_RECEIVED_1 = 0
    Q3_EFFORT_RECEIVED_2 = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    playerID = models.IntegerField()
    date = models.StringField()
    quiz1_worker = models.IntegerField(label="Worker profit")
    quiz1_employer = models.IntegerField(label="Employer profit")
    quiz1_tries = models.IntegerField(initial=0)
    quiz2_worker = models.IntegerField(label="Worker profit")
    quiz2_employer = models.IntegerField(label="Employer profit")
    quiz2_tries = models.IntegerField(initial=0)
    quiz3_worker1 = models.IntegerField(label="Worker 1 profit")
    quiz3_worker2 = models.IntegerField(label="Worker 2 profit")
    quiz3_employer = models.IntegerField(label="Employer profit")
    quiz3_tries = models.IntegerField(initial=0)


# FUNCTIONS
def creating_session(subsession: Subsession):
    """
    This function defines which market players will be in, whether they will workers or employers, and which market they will be moved to.
    """
    players = subsession.get_players()
    num_participants = len(players)
    temp_id_list = random.sample(range(1, num_participants + 1), num_participants)
    session = subsession.session
    size_large_market = session.config['size_large_market']
    num_employers_large_market = session.config['num_employers_large_market']
    num_employers_small_market = session.config['num_employers_small_market']
    migration_small_shock_size = session.config['migration_small_shock_size']
    migration_large_shock_size = session.config['migration_large_shock_size']

    for p in players:
        participant_vars = p.participant.vars
        participant_vars['playerID'] = temp_id_list[(p.id_in_group - 1)]
        participant_vars['large_market'] = False
        participant_vars['large_market_1'] = False  # 1st large market will receive small shock
        participant_vars['large_market_2'] = False  # 2nd large market will receive large shock
        participant_vars['small_market'] = False
        participant_vars['migrant'] = False
        participant_vars['move_to_market_1'] = False
        participant_vars['move_to_market_2'] = False
        participant_vars['is_employer'] = False
        participant_vars['currency_is_points'] = False
        participant_vars['total_points'] = []
        participant_vars['total_tokens'] = []
        participant_vars['round_for_points'] = []
        participant_vars['round_number'] = 0
        participant_vars['num_workers'] = []
        participant_vars['worker1_wage_points'] = []
        participant_vars['worker1_wage_tokens'] = []
        participant_vars['worker1_effort'] = []
        participant_vars['worker1_effort_given'] = []
        participant_vars['worker1_id'] = []
        participant_vars['worker1_profit_points'] = []
        participant_vars['worker1_profit_tokens'] = []
        participant_vars['worker2_wage_points'] = []
        participant_vars['worker2_wage_tokens'] = []
        participant_vars['worker2_effort'] = []
        participant_vars['worker2_effort_given'] = []
        participant_vars['worker2_id'] = []
        participant_vars['worker2_profit_points'] = []
        participant_vars['worker2_profit_tokens'] = []
        p.date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if participant_vars['playerID'] <= size_large_market:
            participant_vars['large_market'] = True
            participant_vars['large_market_1'] = True
            participant_vars['currency_is_points'] = True
            if participant_vars['playerID'] <= num_employers_large_market:
                participant_vars['is_employer'] = True
                participant_vars['string_role'] = 'employer'
            else:
                participant_vars['string_role'] = 'worker'
        elif participant_vars['playerID'] <= (2 * size_large_market):
            participant_vars['large_market'] = True
            participant_vars['large_market_2'] = True
            participant_vars['currency_is_points'] = True
            if participant_vars['playerID'] <= (size_large_market + num_employers_large_market):
                participant_vars['is_employer'] = True
                participant_vars['string_role'] = 'employer'
            else:
                participant_vars['string_role'] = 'worker'
        else:
            participant_vars['small_market'] = True
            participant_vars['currency_is_points'] = False
            if participant_vars['playerID'] <= (num_employers_small_market + size_large_market + size_large_market):
                participant_vars['is_employer'] = True
                participant_vars['string_role'] = 'employer'
            else:
                participant_vars['string_role'] = 'worker'
                if participant_vars['playerID'] <= (
                        num_employers_small_market + size_large_market + size_large_market + migration_small_shock_size):
                    participant_vars['migrant'] = True
                    participant_vars['move_to_market_1'] = True
                elif participant_vars['playerID'] <= (
                        num_employers_small_market + size_large_market + size_large_market + migration_small_shock_size + migration_large_shock_size):
                    participant_vars['migrant'] = True
                    participant_vars['move_to_market_2'] = True
        print('Player ID', participant_vars['playerID'], 'is a', participant_vars['string_role'], 'large market 1 is',
              participant_vars['large_market_1'], 'large market 2 is', participant_vars['large_market_2'],
              'small market is', participant_vars['small_market'], 'move to market 1 is',
              participant_vars['move_to_market_1'], 'move to market 2 is', participant_vars['move_to_market_2'])

    """
    size_large_1 = [p.participant.vars['large_market_1'] for p in players].count(True)
    size_large_2 = [p.participant.vars['large_market_2'] for p in players].count(True)
    size_small = [p.participant.vars['small_market'] for p in players].count(True)
    move_to_1 = [p.participant.vars['move_to_market_1'] for p in players].count(True)
    move_to_2 = [p.participant.vars['move_to_market_2'] for p in players].count(True)

    print('Large market 1 will have', size_large_1, 'players and will receive', move_to_1, 'migrants')
    print('Large market 2 will have', size_large_2, 'players and will receive', move_to_2, 'migrants')
    print('Small market will have', size_small, 'players')
    """


# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        return session.config['final']


class WorkerInstruction(Page):

    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        return not player.participant.is_employer and session.config['final']

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session

        if player.participant.large_market:
            players_in_your_group = session.config['size_large_market']
            employers_in_your_group = session.config['num_employers_large_market']
            workers_in_your_group = session.config['size_large_market'] - session.config['num_employers_large_market']
        else:
            players_in_your_group = session.config['size_small_market']
            employers_in_your_group = session.config['num_employers_small_market']
            workers_in_your_group = session.config['size_small_market'] - session.config['num_employers_small_market']

        name_low_effort = session.config['effort_names'][0]
        name_high_effort = session.config['effort_names'][1]
        currency_plural = "points" if player.participant.currency_is_points else "tokens"
        currency = "point" if player.participant.currency_is_points else "token"
        outside_option_workers_points_tokens = session.config['worker_outside_option']
        outside_option_employers_points_tokens = session.config['employer_outside_option']
        low_effort_points_tokens = session.config['effort_costs_points'][0]
        high_effort_points_tokens = session.config['effort_costs_points'][1]
        gain_high_effort_1_worker = session.config['MPL_high'][0]
        gain_low_effort_1_worker = session.config['MPL_low'][0]
        gain_high_effort_2_workers = session.config['MPL_high'][1]
        gain_low_effort_2_workers = session.config['MPL_low'][1]
        exchange_rate = session.config['payout_rate']
        initial_points_tokens = session.config['showup_fee'] * (1 / session.config['payout_rate'])
        max_wage = session.config['max_wage']
        worker_example_wage = session.config['worker_example_wage']

        if player.participant.currency_is_points is False:
            outside_option_workers_points_tokens = outside_option_workers_points_tokens * session.config[
                'exchange_rate']
            outside_option_employers_points_tokens = outside_option_employers_points_tokens * session.config[
                'exchange_rate']
            low_effort_points_tokens = low_effort_points_tokens * session.config['exchange_rate']
            high_effort_points_tokens = high_effort_points_tokens * session.config['exchange_rate']
            gain_high_effort_1_worker = gain_high_effort_1_worker * session.config['exchange_rate']
            gain_low_effort_1_worker = gain_low_effort_1_worker * session.config['exchange_rate']
            gain_high_effort_2_workers = gain_high_effort_2_workers * session.config['exchange_rate']
            gain_low_effort_2_workers = gain_low_effort_2_workers * session.config['exchange_rate']
            exchange_rate = exchange_rate * (1 / session.config['exchange_rate'])
            initial_points_tokens = initial_points_tokens * session.config['exchange_rate']
            max_wage = max_wage * session.config['exchange_rate']
            worker_example_wage = worker_example_wage * session.config['exchange_rate']

        worker_example_profit_high_effort = worker_example_wage - high_effort_points_tokens
        worker_example_profit_low_effort = worker_example_wage - low_effort_points_tokens

        total_gain_high_effort_2_workers = gain_high_effort_2_workers + gain_high_effort_2_workers
        total_gain_mix_effort_2_workers = gain_high_effort_2_workers + gain_low_effort_2_workers
        total_gain_low_effort_2_workers = gain_low_effort_2_workers + gain_low_effort_2_workers
        profit_employer_example_1 = total_gain_high_effort_2_workers - 60 - 40
        profit_employer_example_2 = total_gain_mix_effort_2_workers - 60 - 40

        return dict(
            profit_employer_example_1=profit_employer_example_1,
            profit_employer_example_2=profit_employer_example_2,
            worker_example_profit_high_effort=worker_example_profit_high_effort,
            worker_example_profit_low_effort=worker_example_profit_low_effort,
            worker_example_wage=worker_example_wage,
            players_in_your_group=players_in_your_group,
            employers_in_your_group=employers_in_your_group,
            workers_in_your_group=workers_in_your_group,
            max_wage=max_wage,
            initial_points_tokens=initial_points_tokens,
            exchange_rate=exchange_rate,
            name_low_effort=name_low_effort,
            name_high_effort=name_high_effort,
            currency_plural=currency_plural,
            currency=currency,
            outside_option_workers_points_tokens=outside_option_workers_points_tokens,
            low_effort_points_tokens=low_effort_points_tokens,
            high_effort_points_tokens=high_effort_points_tokens,
            outside_option_employers_points_tokens=outside_option_employers_points_tokens,
            gain_high_effort_1_worker=gain_high_effort_1_worker,
            gain_low_effort_1_worker=gain_low_effort_1_worker,
            gain_high_effort_2_workers=gain_high_effort_2_workers,
            gain_low_effort_2_workers=gain_low_effort_2_workers,
            total_gain_high_effort_2_workers=total_gain_high_effort_2_workers,
            total_gain_mix_effort_2_workers=total_gain_mix_effort_2_workers,
            total_gain_low_effort_2_workers=total_gain_low_effort_2_workers,
            participation_fee=int(session.config['showup_fee']),
            market_time=session.config['market_timeout_seconds'],
            worker_outside_option=session.config['worker_outside_option'],
            employer_outside_option=session.config['employer_outside_option'],
            total_rounds=int(session.config['total_rounds']),
            shock_after_rounds=session.config['shock_after_rounds'],
            rounds_part_two=int(session.config['total_rounds']) - int(session.config['shock_after_rounds']),
        )


class FirmInstruction(Page):

    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        return player.participant.is_employer and session.config['final']

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session

        if player.participant.large_market:
            players_in_your_group = session.config['size_large_market']
            employers_in_your_group = session.config['num_employers_large_market']
            workers_in_your_group = session.config['size_large_market'] - session.config['num_employers_large_market']
        else:
            players_in_your_group = session.config['size_small_market']
            employers_in_your_group = session.config['num_employers_small_market']
            workers_in_your_group = session.config['size_small_market'] - session.config['num_employers_small_market']

        name_low_effort = session.config['effort_names'][0]
        name_high_effort = session.config['effort_names'][1]
        currency_plural = "points" if player.participant.currency_is_points else "tokens"
        currency = "point" if player.participant.currency_is_points else "token"
        outside_option_workers_points_tokens = session.config['worker_outside_option']
        outside_option_employers_points_tokens = session.config['employer_outside_option']
        low_effort_points_tokens = session.config['effort_costs_points'][0]
        high_effort_points_tokens = session.config['effort_costs_points'][1]
        gain_high_effort_1_worker = session.config['MPL_high'][0]
        gain_low_effort_1_worker = session.config['MPL_low'][0]
        gain_high_effort_2_workers = session.config['MPL_high'][1]
        gain_low_effort_2_workers = session.config['MPL_low'][1]
        exchange_rate = session.config['payout_rate']
        initial_points_tokens = session.config['showup_fee'] * (1 / session.config['payout_rate'])
        max_wage = session.config['max_wage']
        worker_example_wage = session.config['worker_example_wage']

        if player.participant.currency_is_points is False:
            outside_option_workers_points_tokens = outside_option_workers_points_tokens * session.config[
                'exchange_rate']
            outside_option_employers_points_tokens = outside_option_employers_points_tokens * session.config[
                'exchange_rate']
            low_effort_points_tokens = low_effort_points_tokens * session.config['exchange_rate']
            high_effort_points_tokens = high_effort_points_tokens * session.config['exchange_rate']
            gain_high_effort_1_worker = gain_high_effort_1_worker * session.config['exchange_rate']
            gain_low_effort_1_worker = gain_low_effort_1_worker * session.config['exchange_rate']
            gain_high_effort_2_workers = gain_high_effort_2_workers * session.config['exchange_rate']
            gain_low_effort_2_workers = gain_low_effort_2_workers * session.config['exchange_rate']
            exchange_rate = exchange_rate * (1 / session.config['exchange_rate'])
            initial_points_tokens = initial_points_tokens * session.config['exchange_rate']
            max_wage = max_wage * session.config['exchange_rate']
            worker_example_wage = worker_example_wage * session.config['exchange_rate']

        worker_example_profit_high_effort = worker_example_wage - high_effort_points_tokens
        worker_example_profit_low_effort = worker_example_wage - low_effort_points_tokens

        total_gain_high_effort_2_workers = gain_high_effort_2_workers + gain_high_effort_2_workers
        total_gain_mix_effort_2_workers = gain_high_effort_2_workers + gain_low_effort_2_workers
        total_gain_low_effort_2_workers = gain_low_effort_2_workers + gain_low_effort_2_workers
        profit_employer_example_1 = total_gain_high_effort_2_workers - 60 - 40
        profit_employer_example_2 = total_gain_mix_effort_2_workers - 60 - 40

        return dict(
            profit_employer_example_1=profit_employer_example_1,
            profit_employer_example_2=profit_employer_example_2,
            worker_example_profit_high_effort=worker_example_profit_high_effort,
            worker_example_profit_low_effort=worker_example_profit_low_effort,
            worker_example_wage=worker_example_wage,
            players_in_your_group=players_in_your_group,
            employers_in_your_group=employers_in_your_group,
            workers_in_your_group=workers_in_your_group,
            max_wage=max_wage,
            initial_points_tokens=initial_points_tokens,
            exchange_rate=exchange_rate,
            name_low_effort=name_low_effort,
            name_high_effort=name_high_effort,
            currency_plural=currency_plural,
            currency=currency,
            outside_option_workers_points_tokens=outside_option_workers_points_tokens,
            low_effort_points_tokens=low_effort_points_tokens,
            high_effort_points_tokens=high_effort_points_tokens,
            outside_option_employers_points_tokens=outside_option_employers_points_tokens,
            gain_high_effort_1_worker=gain_high_effort_1_worker,
            gain_low_effort_1_worker=gain_low_effort_1_worker,
            gain_high_effort_2_workers=gain_high_effort_2_workers,
            gain_low_effort_2_workers=gain_low_effort_2_workers,
            total_gain_high_effort_2_workers=total_gain_high_effort_2_workers,
            total_gain_mix_effort_2_workers=total_gain_mix_effort_2_workers,
            total_gain_low_effort_2_workers=total_gain_low_effort_2_workers,
            participation_fee=int(session.config['showup_fee']),
            market_time=session.config['market_timeout_seconds'],
            worker_outside_option=session.config['worker_outside_option'],
            employer_outside_option=session.config['employer_outside_option'],
            total_rounds=int(session.config['total_rounds']),
            shock_after_rounds=session.config['shock_after_rounds'],
            rounds_part_two=int(session.config['total_rounds']) - int(session.config['shock_after_rounds']),
        )


class quiz1(Page):
    form_model = 'player'
    form_fields = ['quiz1_worker', 'quiz1_employer']

    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        return session.config['final']

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session

        name_low_effort = session.config['effort_names'][0]
        name_high_effort = session.config['effort_names'][1]
        currency_plural = "points" if player.participant.currency_is_points else "tokens"
        currency = "point" if player.participant.currency_is_points else "token"
        outside_option_workers_points_tokens = session.config['worker_outside_option']
        outside_option_employers_points_tokens = session.config['employer_outside_option']
        low_effort_points_tokens = session.config['effort_costs_points'][0]
        high_effort_points_tokens = session.config['effort_costs_points'][1]
        gain_high_effort_1_worker = session.config['MPL_high'][0]
        gain_low_effort_1_worker = session.config['MPL_low'][0]
        gain_high_effort_2_workers = session.config['MPL_high'][1]
        gain_low_effort_2_workers = session.config['MPL_low'][1]

        if player.participant.currency_is_points is False:
            outside_option_workers_points_tokens = outside_option_workers_points_tokens * session.config[
                'exchange_rate']
            outside_option_employers_points_tokens = outside_option_employers_points_tokens * session.config[
                'exchange_rate']
            low_effort_points_tokens = low_effort_points_tokens * session.config['exchange_rate']
            high_effort_points_tokens = high_effort_points_tokens * session.config['exchange_rate']
            gain_high_effort_1_worker = gain_high_effort_1_worker * session.config['exchange_rate']
            gain_low_effort_1_worker = gain_low_effort_1_worker * session.config['exchange_rate']
            gain_high_effort_2_workers = gain_high_effort_2_workers * session.config['exchange_rate']
            gain_low_effort_2_workers = gain_low_effort_2_workers * session.config['exchange_rate']

        total_gain_high_effort_2_workers = gain_high_effort_2_workers + gain_high_effort_2_workers
        total_gain_mix_effort_2_workers = gain_high_effort_2_workers + gain_low_effort_2_workers
        total_gain_low_effort_2_workers = gain_low_effort_2_workers + gain_low_effort_2_workers

        return dict(
            name_low_effort=name_low_effort,
            name_high_effort=name_high_effort,
            currency_plural=currency_plural,
            currency=currency,
            outside_option_workers_points_tokens=outside_option_workers_points_tokens,
            low_effort_points_tokens=low_effort_points_tokens,
            high_effort_points_tokens=high_effort_points_tokens,
            outside_option_employers_points_tokens=outside_option_employers_points_tokens,
            gain_high_effort_1_worker=gain_high_effort_1_worker,
            gain_low_effort_1_worker=gain_low_effort_1_worker,
            gain_high_effort_2_workers=gain_high_effort_2_workers,
            gain_low_effort_2_workers=gain_low_effort_2_workers,
            total_gain_high_effort_2_workers=total_gain_high_effort_2_workers,
            total_gain_mix_effort_2_workers=total_gain_mix_effort_2_workers,
            total_gain_low_effort_2_workers=total_gain_low_effort_2_workers,
        )

    @staticmethod
    def error_message(player: Player, values):
        session = player.session
        worker_profit = session.config['employer_outside_option']
        employer_profit = session.config['worker_outside_option']
        if values['quiz1_worker'] != worker_profit or values['quiz1_employer'] != employer_profit:
            player.quiz1_tries += 1
            return 'Incorrect. Please try again.'

    @staticmethod
    def js_vars(player: Player):
        return dict(
            employer=player.participant.vars['is_employer'],
        )


class quiz2(Page):
    form_model = 'player'
    form_fields = ['quiz2_worker', 'quiz2_employer']

    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        return session.config['final']

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session

        q2_effort_requested = session.config['effort_names'][C.Q2_EFFORT_REQUESTED]
        q2_effort_received = session.config['effort_names'][C.Q2_EFFORT_RECEIVED]
        name_low_effort = session.config['effort_names'][0]
        name_high_effort = session.config['effort_names'][1]
        currency_plural = "points" if player.participant.currency_is_points else "tokens"
        currency = "point" if player.participant.currency_is_points else "token"

        outside_option_workers_points_tokens = session.config['worker_outside_option']
        outside_option_employers_points_tokens = session.config['employer_outside_option']
        low_effort_points_tokens = session.config['effort_costs_points'][0]
        high_effort_points_tokens = session.config['effort_costs_points'][1]
        gain_high_effort_1_worker = session.config['MPL_high'][0]
        gain_low_effort_1_worker = session.config['MPL_low'][0]
        gain_high_effort_2_workers = session.config['MPL_high'][1]
        gain_low_effort_2_workers = session.config['MPL_low'][1]
        q2_wage = C.Q2_WAGE

        if player.participant.currency_is_points is False:
            outside_option_workers_points_tokens = outside_option_workers_points_tokens * session.config[
                'exchange_rate']
            outside_option_employers_points_tokens = outside_option_employers_points_tokens * session.config[
                'exchange_rate']
            low_effort_points_tokens = low_effort_points_tokens * session.config['exchange_rate']
            high_effort_points_tokens = high_effort_points_tokens * session.config['exchange_rate']
            gain_high_effort_1_worker = gain_high_effort_1_worker * session.config['exchange_rate']
            gain_low_effort_1_worker = gain_low_effort_1_worker * session.config['exchange_rate']
            gain_high_effort_2_workers = gain_high_effort_2_workers * session.config['exchange_rate']
            gain_low_effort_2_workers = gain_low_effort_2_workers * session.config['exchange_rate']
            q2_wage = q2_wage * session.config['exchange_rate']

        total_gain_high_effort_2_workers = gain_high_effort_2_workers + gain_high_effort_2_workers
        total_gain_mix_effort_2_workers = gain_high_effort_2_workers + gain_low_effort_2_workers
        total_gain_low_effort_2_workers = gain_low_effort_2_workers + gain_low_effort_2_workers

        return dict(
            name_low_effort=name_low_effort,
            name_high_effort=name_high_effort,
            currency_plural=currency_plural,
            currency=currency,
            outside_option_workers_points_tokens=outside_option_workers_points_tokens,
            low_effort_points_tokens=low_effort_points_tokens,
            high_effort_points_tokens=high_effort_points_tokens,
            outside_option_employers_points_tokens=outside_option_employers_points_tokens,
            gain_high_effort_1_worker=gain_high_effort_1_worker,
            gain_low_effort_1_worker=gain_low_effort_1_worker,
            gain_high_effort_2_workers=gain_high_effort_2_workers,
            gain_low_effort_2_workers=gain_low_effort_2_workers,
            total_gain_high_effort_2_workers=total_gain_high_effort_2_workers,
            total_gain_mix_effort_2_workers=total_gain_mix_effort_2_workers,
            total_gain_low_effort_2_workers=total_gain_low_effort_2_workers,
            q2_effort_received=q2_effort_received,
            q2_effort_requested=q2_effort_requested,
            q2_wage=q2_wage,
        )

    @staticmethod
    def error_message(player: Player, values):
        print('values', values)
        session = player.session

        # Calculate answers in points
        q2_wage = C.Q2_WAGE
        effort_cost = session.config['effort_costs_points'][C.Q2_EFFORT_RECEIVED]
        if C.Q2_EFFORT_RECEIVED == 1:
            effort_worth = session.config['MPL_high'][0]
        elif C.Q2_EFFORT_RECEIVED == 0:
            effort_worth = session.config['MPL_low'][0]

        # Convert to tokens if needed
        if player.participant.currency_is_points is False:
            q2_wage = q2_wage * session.config['exchange_rate']
            effort_cost = effort_cost * session.config['exchange_rate']
            effort_worth = effort_worth * session.config['exchange_rate']

        worker_profit = q2_wage - effort_cost
        employer_profit = effort_worth - q2_wage

        if values['quiz2_worker'] != worker_profit or values['quiz2_employer'] != employer_profit:
            player.quiz2_tries += 1
            return 'Incorrect. Please try again.'


class quiz3(Page):
    form_model = 'player'
    form_fields = ['quiz3_worker1', 'quiz3_worker2', 'quiz3_employer']

    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        return session.config['final']

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session

        q3_wage_1 = C.Q3_WAGE_1
        q3_wage_2 = C.Q3_WAGE_2
        q3_effort_received_1 = session.config['effort_names'][C.Q3_EFFORT_RECEIVED_1]
        q3_effort_received_2 = session.config['effort_names'][C.Q3_EFFORT_RECEIVED_2]

        name_low_effort = session.config['effort_names'][0]
        name_high_effort = session.config['effort_names'][1]
        currency_plural = "points" if player.participant.currency_is_points else "tokens"
        currency = "point" if player.participant.currency_is_points else "token"
        outside_option_workers_points_tokens = session.config['worker_outside_option']
        outside_option_employers_points_tokens = session.config['employer_outside_option']
        low_effort_points_tokens = session.config['effort_costs_points'][0]
        high_effort_points_tokens = session.config['effort_costs_points'][1]
        gain_high_effort_1_worker = session.config['MPL_high'][0]
        gain_low_effort_1_worker = session.config['MPL_low'][0]
        gain_high_effort_2_workers = session.config['MPL_high'][1]
        gain_low_effort_2_workers = session.config['MPL_low'][1]

        if player.participant.currency_is_points is False:
            outside_option_workers_points_tokens = outside_option_workers_points_tokens * session.config[
                'exchange_rate']
            outside_option_employers_points_tokens = outside_option_employers_points_tokens * session.config[
                'exchange_rate']
            low_effort_points_tokens = low_effort_points_tokens * session.config['exchange_rate']
            high_effort_points_tokens = high_effort_points_tokens * session.config['exchange_rate']
            gain_high_effort_1_worker = gain_high_effort_1_worker * session.config['exchange_rate']
            gain_low_effort_1_worker = gain_low_effort_1_worker * session.config['exchange_rate']
            gain_high_effort_2_workers = gain_high_effort_2_workers * session.config['exchange_rate']
            gain_low_effort_2_workers = gain_low_effort_2_workers * session.config['exchange_rate']
            q3_wage_1 = q3_wage_1 * session.config['exchange_rate']
            q3_wage_2 = q3_wage_2 * session.config['exchange_rate']

        total_gain_high_effort_2_workers = gain_high_effort_2_workers + gain_high_effort_2_workers
        total_gain_mix_effort_2_workers = gain_high_effort_2_workers + gain_low_effort_2_workers
        total_gain_low_effort_2_workers = gain_low_effort_2_workers + gain_low_effort_2_workers

        return dict(
            name_low_effort=name_low_effort,
            name_high_effort=name_high_effort,
            currency_plural=currency_plural,
            currency=currency,
            outside_option_workers_points_tokens=outside_option_workers_points_tokens,
            low_effort_points_tokens=low_effort_points_tokens,
            high_effort_points_tokens=high_effort_points_tokens,
            outside_option_employers_points_tokens=outside_option_employers_points_tokens,
            gain_high_effort_1_worker=gain_high_effort_1_worker,
            gain_low_effort_1_worker=gain_low_effort_1_worker,
            gain_high_effort_2_workers=gain_high_effort_2_workers,
            gain_low_effort_2_workers=gain_low_effort_2_workers,
            total_gain_high_effort_2_workers=total_gain_high_effort_2_workers,
            total_gain_mix_effort_2_workers=total_gain_mix_effort_2_workers,
            total_gain_low_effort_2_workers=total_gain_low_effort_2_workers,
            q3_wage_1=q3_wage_1,
            q3_wage_2=q3_wage_2,
            q3_effort_received_1=q3_effort_received_1,
            q3_effort_received_2=q3_effort_received_2,
        )

    @staticmethod
    def error_message(player: Player, values):
        session = player.session

        # Calculate answers in points
        effort_cost_1 = session.config['effort_costs_points'][C.Q3_EFFORT_RECEIVED_1]
        effort_cost_2 = session.config['effort_costs_points'][C.Q3_EFFORT_RECEIVED_2]
        q3_wage_1 = C.Q3_WAGE_1
        q3_wage_2 = C.Q3_WAGE_2
        if C.Q3_EFFORT_RECEIVED_1 == 1 and C.Q3_EFFORT_RECEIVED_2 == 1:
            effort_worth = session.config['MPL_high'][1] + session.config['MPL_high'][1]
        elif C.Q3_EFFORT_RECEIVED_1 == 0 and C.Q3_EFFORT_RECEIVED_2 == 0:
            effort_worth = session.config['MPL_low'][1] + session.config['MPL_low'][1]
        else:
            effort_worth = session.config['MPL_high'][1] + session.config['MPL_low'][1]

        # Convert to tokens if needed
        if player.participant.currency_is_points is False:
            q3_wage_1 = q3_wage_1 * session.config['exchange_rate']
            q3_wage_2 = q3_wage_2 * session.config['exchange_rate']
            effort_cost_1 = effort_cost_1 * session.config['exchange_rate']
            effort_cost_2 = effort_cost_2 * session.config['exchange_rate']
            effort_worth = effort_worth * session.config['exchange_rate']

        # Calculate profits
        worker1_profit = q3_wage_1 - effort_cost_1
        worker2_profit = q3_wage_2 - effort_cost_2
        employer_profit = effort_worth - q3_wage_1 - q3_wage_2

        if values['quiz3_worker1'] != worker1_profit or values['quiz3_worker2'] != worker2_profit or values[
            'quiz3_employer'] != employer_profit:
            player.quiz3_tries += 1
            print("Correct answer:", worker1_profit, worker2_profit, employer_profit)
            return 'Incorrect. Please try again.'


class WaitToStart(WaitPage):
    wait_for_all_groups = True
    template_name = '_templates/includes/My_WaitPage.html'
    body_text = "Waiting for other participants to finish the quiz."

    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        return session.config['final']


page_sequence = [
    # Introduction,
    # WorkerInstruction,
    # FirmInstruction,
    # quiz1,
    # quiz2,
    # quiz3,
    # WaitToStart
]
