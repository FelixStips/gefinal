from otree.api import *
import random
random.seed(10)


doc = """
TO-DO's:
    - Add setting of whether there is income difference --> is this needed? can set exchange rate to 1.
    - Make two pages out of the midbreak instructions
    - Adjust instructions to new word version
    - Adjust quiz questions
    - Add images to instructions
    - Change welcome to part 2 to have a card
    - Add minimum payment
    - Improve design of payment screen
TO-TEST:    
    - Database
    - Payment storage
    - Points & tokens
"""


class C(BaseConstants):
    NAME_IN_URL = 'intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    Q2_WAGE = 70
    Q2_EFFORT_REQUESTED = 8
    Q2_EFFORT_RECEIVED = 8
    Q3_WAGE = 60
    Q3_EFFORT_REQUESTED = 8
    Q3_EFFORT_RECEIVED = 3
    Q4_WAGE_1 = 30
    Q4_WAGE_2 = 40
    Q4_EFFORT_RECEIVED_1 = 4
    Q4_EFFORT_RECEIVED_2 = 6


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    playerID = models.IntegerField()


class QuizResponses(ExtraModel):
    player = models.Link(Player)
    playerID = models.IntegerField()
    question = models.StringField()
    correct = models.BooleanField()


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
        participant_vars['large_market_1'] = False                                                                      # 1st large market will receive small shock
        participant_vars['large_market_2'] = False                                                                      # 2nd large market will receive large shock
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
                if participant_vars['playerID'] <= (num_employers_small_market + size_large_market + size_large_market + migration_small_shock_size):
                    participant_vars['migrant'] = True
                    participant_vars['move_to_market_1'] = True
                elif participant_vars['playerID'] <= (num_employers_small_market + size_large_market + size_large_market + migration_small_shock_size + migration_large_shock_size):
                    participant_vars['migrant'] = True
                    participant_vars['move_to_market_2'] = True
        #print(participant_vars['currency_is_points'])

    """ Proportions seem right at least...
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


class InstructionsWorkers(Page):
    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        return session.config['final']

    @staticmethod
    def js_vars(player: Player):
        return dict(playerID=player.participant.playerID,
                    small_market=player.participant.small_market,)

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session

        currency_plural = "points" if player.participant.currency_is_points else "tokens"
        currency = "point" if player.participant.currency_is_points else "token"

        if player.participant.currency_is_points:
            exchange_rate = session.config['payout_rate']
            initial_points_tokens = session.config['showup_fee'] * (1/session.config['payout_rate'])
            low_effort_points_tokens = session.config['effort_costs_points'][0]
            high_effort_points_tokens = session.config['effort_costs_points'][1]
            outside_option_workers_points_tokens = session.config['worker_outside_option']
            outside_option_employers_points_tokens = session.config['employer_outside_option']
            gain_high_effort_1_worker = session.config['MPL_high'][0]
            gain_high_effort_2_workers = session.config['MPL_high'][1]
            gain_low_effort_1_worker = session.config['MPL_low'][0]
            gain_low_effort_2_workers = session.config['MPL_low'][1]
            worker_example_wage = session.config['worker_example_wage']
        else:
            exchange_rate = session.config['payout_rate'] * (1/session.config['exchange_rate'])
            initial_points_tokens = session.config['showup_fee'] * (1/session.config['payout_rate']) * session.config['exchange_rate']
            low_effort_points_tokens = session.config['effort_costs_points'][0] * session.config['exchange_rate']
            high_effort_points_tokens = session.config['effort_costs_points'][1] * session.config['exchange_rate']
            outside_option_workers_points_tokens = session.config['worker_outside_option'] * session.config['exchange_rate']
            outside_option_employers_points_tokens = session.config['employer_outside_option'] * session.config['exchange_rate']
            gain_high_effort_1_worker = session.config['MPL_high'][0] * session.config['exchange_rate']
            gain_high_effort_2_workers = session.config['MPL_high'][1] * session.config['exchange_rate']
            gain_low_effort_1_worker = session.config['MPL_low'][0] * session.config['exchange_rate']
            gain_low_effort_2_workers = session.config['MPL_low'][1] * session.config['exchange_rate']
            worker_example_wage = session.config['worker_example_wage'] * session.config['exchange_rate']

        worker_example_profit_low_effort = worker_example_wage - low_effort_points_tokens
        worker_example_profit_high_effort = worker_example_wage - high_effort_points_tokens

        if player.participant.large_market:
            players_in_your_group = session.config['size_large_market']
            employers_in_your_group = session.config['num_employers_large_market']
            workers_in_your_group = session.config['size_large_market'] - session.config['num_employers_large_market']
            initial_points_tokens = int(session.config['showup_fee'] * (1/session.config['payout_rate']))
        elif player.participant.small_market:
            players_in_your_group = session.config['size_small_market']
            employers_in_your_group = session.config['num_employers_small_market']
            workers_in_your_group = session.config['size_small_market'] - session.config['num_employers_small_market']
            initial_points_tokens = int(session.config['showup_fee'] * (1 / session.config['payout_rate'])) * session.config['exchange_rate']

        return dict(
            worker_example_profit_high_effort=worker_example_profit_high_effort,
            worker_example_profit_low_effort=worker_example_profit_low_effort,
            worker_example_wage=worker_example_wage,
            gain_high_effort_1_worker=gain_high_effort_1_worker,
            gain_high_effort_2_workers=gain_high_effort_2_workers,
            gain_low_effort_1_worker=gain_low_effort_1_worker,
            gain_low_effort_2_workers=gain_low_effort_2_workers,
            outside_option_employers_points_tokens=outside_option_employers_points_tokens,
            outside_option_workers_points_tokens=outside_option_workers_points_tokens,
            high_effort_points_tokens=high_effort_points_tokens,
            low_effort_points_tokens=low_effort_points_tokens,
            currency=currency,
            currency_plural=currency_plural,
            exchange_rate=exchange_rate,
            players_in_your_group=players_in_your_group,
            employers_in_your_group=employers_in_your_group,
            workers_in_your_group=workers_in_your_group,
            currency_is_points=player.participant.currency_is_points,
            initial_points_tokens=initial_points_tokens,
            total_rounds=int(session.config['total_rounds']),
            shock_after_rounds=session.config['shock_after_rounds'],
            rounds_part_two=int(session.config['total_rounds']) - int(session.config['shock_after_rounds']),
            participation_fee=int(session.config['showup_fee']),
            market_time=session.config['market_timeout_seconds'],
            worker_outside_option=session.config['worker_outside_option'],
            employer_outside_option=session.config['employer_outside_option'],

        )




class WaitToStart(WaitPage):
    body_text = "Waiting for other participants to finish the quiz."

    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        return session.config['final']


page_sequence = [Introduction,
                 InstructionsWorkers,
                 WaitToStart]
def custom_export(player):
    # top row
    yield ['playerID', 'question', 'correct']

    # data rows
    quiz_responses = QuizResponses.filter()
    for response in quiz_responses:
        yield [response.playerID, response.question, response.correct]