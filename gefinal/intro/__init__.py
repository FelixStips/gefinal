from otree.api import *
import random
random.seed(10)


doc = """
Your app description
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


class Instructions(Page):
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
        if player.participant.large_market:
            exchange_rate = session.config['exchange_rate_large_market']
            players_in_your_group = session.config['size_large_market']
            employers_in_your_group = session.config['num_employers_large_market']
            workers_in_your_group = session.config['size_large_market'] - session.config['num_employers_large_market']
        elif player.participant.small_market:
            exchange_rate = session.config['exchange_rate_small_market']
            players_in_your_group = session.config['size_small_market']
            employers_in_your_group = session.config['num_employers_small_market']
            workers_in_your_group = session.config['size_small_market'] - session.config['num_employers_small_market']

        return dict(
            exchange_rate=exchange_rate,
            players_in_your_group=players_in_your_group,
            employers_in_your_group=employers_in_your_group,
            workers_in_your_group=workers_in_your_group,
            shock_after_rounds=session.config['shock_after_rounds'],
            total_rounds=int(session.config['total_rounds']),
            participation_fee=int(session.config['showup_fee']),
            initial_points=int(session.config['showup_fee'] * (1 / exchange_rate)),
            market_time=session.config['market_timeout_seconds'],
            worker_outside_option=session.config['worker_outside_option'],
            employer_outside_option=session.config['employer_outside_option'],
            mpl1=session.config['MPL'][0],
            mpl2=session.config['MPL'][1],
            mpl3=session.config['MPL'][2],
            ex_1_wage=50,
            ex_1_effort=7,
            ex_1_employer_profit=session.config['MPL'][0] * 7 - 50,
            ex_2_wage_1=60,
            ex_2_effort_1=8,
            ex_2_wage_2=40,
            ex_2_effort_2=6,
            ex_2_employer_profit=session.config['MPL'][1] * (8 + 6) - (60 + 40),
            ex_3_wage_1=60,
            ex_3_effort_1=8,
            ex_3_wage_2=40,
            ex_3_effort_2=6,
            ex_3_wage_3=50,
            ex_3_effort_3=7,
            ex_3_employer_profit=session.config['MPL'][2] * (8 + 6 + 7) - (60 + 40 + 50),
        )

    @staticmethod
    def live_method(player: Player, data):
        session = player.session
        effort_costs = {1: 0, 2: 1, 3: 2, 4: 4, 5: 6, 6: 8, 7: 10, 8: 12, 9: 15, 10: 18}
        q1_employer_profit = session.config['employer_outside_option']
        q2_employer_profit = session.config['MPL'][0] * C.Q2_EFFORT_RECEIVED - C.Q2_WAGE
        q3_employer_profit = session.config['MPL'][0] * C.Q3_EFFORT_RECEIVED - C.Q3_WAGE
        q4_employer_profit = session.config['MPL'][1] * (C.Q4_EFFORT_RECEIVED_1 + C.Q4_EFFORT_RECEIVED_2) - (C.Q4_WAGE_1 + C.Q4_WAGE_2)
        q1_worker_profit = session.config['worker_outside_option']
        q2_worker_profit = C.Q2_WAGE - effort_costs[C.Q2_EFFORT_RECEIVED]
        q3_worker_profit = C.Q3_WAGE - effort_costs[C.Q3_EFFORT_RECEIVED]
        q4_worker_profit_1 = C.Q4_WAGE_1 - effort_costs[C.Q4_EFFORT_RECEIVED_1]
        q4_worker_profit_2 = C.Q4_WAGE_2 - effort_costs[C.Q4_EFFORT_RECEIVED_2]

        if data['information_type'] == 'submit_answer':
            my_id = player.id_in_group
            print('Received', data)
            if data['question'] == 'q1':
                print('Correct employer profit:', q1_employer_profit, 'Correct worker profit:', q1_worker_profit)
                print('Received employer profit:', data['employer_profit'], 'Received worker profit:', data['worker_profit'])
                if int(data['employer_profit']) == q1_employer_profit and int(data['worker_profit']) == q1_worker_profit:
                    print('correct!')
                    QuizResponses.create(
                        playerID=player.participant.playerID,
                        question=data['question'],
                        correct=True,
                    )
                    return {my_id: dict(correct=True, question=data['question'])}
                else:
                    print('False')
                    QuizResponses.create(
                        playerID=player.participant.playerID,
                        question=data['question'],
                        correct=False,
                    )
                    return {my_id: dict(correct=False, question=data['question'])}
            elif data['question'] == 'q2':
                print('Correct employer profit:', q2_employer_profit, 'Correct worker profit:', q2_worker_profit)
                print('Received employer profit:', data['employer_profit'], 'Received worker profit:', data['worker_profit'])
                if int(data['employer_profit']) == q2_employer_profit and int(data['worker_profit']) == q2_worker_profit:
                    print('correct!')
                    QuizResponses.create(
                        playerID=player.participant.playerID,
                        question=data['question'],
                        correct=True,
                    )
                    return {my_id: dict(correct=True, question=data['question'])}
                else:
                    print('False')
                    QuizResponses.create(
                        playerID=player.participant.playerID,
                        question=data['question'],
                        correct=False,
                    )
                    return {my_id: dict(correct=False, question=data['question'])}
            elif data['question'] == 'q3':
                print('Q2')
                print('Correct employer profit:', q3_employer_profit, 'Correct worker profit:', q3_worker_profit)
                print('Received employer profit:', data['employer_profit'], 'Received worker profit:', data['worker_profit'])
                if int(data['employer_profit']) == int(q3_employer_profit) and int(data['worker_profit']) == int(q3_worker_profit):
                    print('correct!')
                    QuizResponses.create(
                        playerID=player.participant.playerID,
                        question=data['question'],
                        correct=True,
                    )
                    return {my_id: dict(correct=True, question=data['question'])}
                else:
                    print('False')
                    QuizResponses.create(
                        playerID=player.participant.playerID,
                        question=data['question'],
                        correct=False,
                    )
                    return {my_id: dict(correct=False, question=data['question'])}
            elif data['question'] == 'q4':
                print('Correct employer profit:', q4_employer_profit, 'Correct worker 1 profit:', q4_worker_profit_1, 'Correct worker 2 profit:', q4_worker_profit_2)
                print('Received employer profit:', data['employer_profit'], 'Received worker 1 profit:', data['worker_profit'], 'Received worker 2 profit:', data['worker_profit_2'])
                if int(data['employer_profit']) == q4_employer_profit and int(data['worker_profit']) == q4_worker_profit_1 and int(data['worker_profit_2']) == q4_worker_profit_2:
                    QuizResponses.create(
                        playerID=player.participant.playerID,
                        question=data['question'],
                        correct=True,
                    )
                    return {my_id: dict(correct=True, question=data['question'])}
                else:
                    QuizResponses.create(
                        playerID=player.participant.playerID,
                        question=data['question'],
                        correct=False,
                    )
                    return {my_id: dict(correct=False, question=data['question'])}
            else:
                print('received wrong question')
        elif data['information_type'] == 'page_loaded':
            pass
        else:
            print('received wrong information type')

class WaitToStart(WaitPage):
    body_text = "Waiting for other participants to finish the quiz."

    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        return session.config['final']


page_sequence = [Introduction,
                 Instructions,
                 WaitToStart]
def custom_export(player):
    # top row
    yield ['playerID', 'question', 'correct']

    # data rows
    quiz_responses = QuizResponses.filter()
    for response in quiz_responses:
        yield [response.playerID, response.question, response.correct]