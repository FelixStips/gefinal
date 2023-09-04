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
    Q2_EFFORT_REQUESTED = "standard"
    Q2_EFFORT_RECEIVED = "standard"
    Q3_WAGE_1 = 30
    Q3_WAGE_2 = 50
    Q3_EFFORT_RECEIVED_1 = "low"
    Q3_EFFORT_RECEIVED_2 = "standard"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    playerID = models.IntegerField()
    date = models.StringField()


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
        participant_vars['num_workers'] = []
        participant_vars['worker1_wage_points'] = []
        participant_vars['worker1_wage_tokens'] = []
        participant_vars['worker1_effort_given'] = []
        participant_vars['worker1_effort'] = []
        participant_vars['worker1_id'] = []
        participant_vars['worker2_wage_points'] = []
        participant_vars['worker2_wage_tokens'] = []
        participant_vars['worker2_effort_given'] = []
        participant_vars['worker2_effort'] = []
        participant_vars['worker2_id'] = []
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
        if session.config['final'] is True and player.participant.is_employer is False:
            return True

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session

        name_low_effort = session.config['effort_names'][0]
        name_high_effort = session.config['effort_names'][1]

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
            q2_wage = C.Q2_WAGE
            q3_wage_1 = C.Q3_WAGE_1
            q3_wage_2 = C.Q3_WAGE_2
            max_wage = session.config['max_wage']
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
            q2_wage = C.Q2_WAGE * session.config['exchange_rate']
            q3_wage_1 = C.Q3_WAGE_1 * session.config['exchange_rate']
            q3_wage_2 = C.Q3_WAGE_2 * session.config['exchange_rate']
            max_wage = session.config['max_wage'] * session.config['exchange_rate']

        worker_example_profit_low_effort = worker_example_wage - low_effort_points_tokens
        worker_example_profit_high_effort = worker_example_wage - high_effort_points_tokens
        total_gain_low_effort_2_workers = 2 * gain_low_effort_2_workers
        total_gain_high_effort_2_workers = 2 * gain_high_effort_2_workers
        total_gain_mix_effort_2_workers = gain_low_effort_2_workers + gain_high_effort_2_workers
        gain_mix_effort_2_workers = int(total_gain_mix_effort_2_workers / 2) if total_gain_mix_effort_2_workers % 2 == 0 else total_gain_mix_effort_2_workers / 2
        profit_employer_example_1 = total_gain_high_effort_2_workers - 60 - 40
        profit_employer_example_2 = total_gain_mix_effort_2_workers - 60 - 40

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
        else:
            print('error: no market type')

        return dict(
            name_low_effort = name_low_effort,
            name_high_effort = name_high_effort,
            profit_employer_example_1 = profit_employer_example_1,
            profit_employer_example_2 = profit_employer_example_2,
            max_wage=max_wage,
            q2_effort_requested=C.Q2_EFFORT_REQUESTED,
            q2_effort_received=C.Q2_EFFORT_RECEIVED,
            q3_effort_received_1=C.Q3_EFFORT_RECEIVED_1,
            q3_effort_received_2=C.Q3_EFFORT_RECEIVED_2,
            q2_wage=q2_wage,
            q3_wage_1=q3_wage_1,
            q3_wage_2=q3_wage_2,
            total_gain_mix_effort_2_workers=total_gain_mix_effort_2_workers,
            gain_mix_effort_2_workers=gain_mix_effort_2_workers,
            total_gain_high_effort_2_workers=total_gain_high_effort_2_workers,
            total_gain_low_effort_2_workers=total_gain_low_effort_2_workers,
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

    @staticmethod
    def live_method(player: Player, data):
        session = player.session

        q2_efort_worth = session.config['MPL_high'][0] if C.Q2_EFFORT_RECEIVED == "standard" else session.config['MPL_low'][0]
        q3_efort_worth_1 = session.config['MPL_high'][1] if C.Q3_EFFORT_RECEIVED_1 == "standard" else session.config['MPL_low'][1]
        q3_efort_worth_2 = session.config['MPL_high'][1] if C.Q3_EFFORT_RECEIVED_2 == "standard" else session.config['MPL_low'][1]
        q2_efort_cost = session.config['effort_costs_points'][1] if C.Q2_EFFORT_RECEIVED == "standard" else session.config['effort_costs_points'][0]
        q3_efort_cost_1 = session.config['effort_costs_points'][1] if C.Q3_EFFORT_RECEIVED_1 == "standard" else session.config['effort_costs_points'][0]
        q3_efort_cost_2 = session.config['effort_costs_points'][1] if C.Q3_EFFORT_RECEIVED_2 == "standard" else session.config['effort_costs_points'][0]

        if player.participant.currency_is_points:
            q2_effort_worth = q2_efort_worth
            q3_effort_worth_1 = q3_efort_worth_1
            q3_effort_worth_2 = q3_efort_worth_2
            q2_effort_cost = q2_efort_cost
            q3_effort_cost_1 = q3_efort_cost_1
            q3_effort_cost_2 = q3_efort_cost_2
            q1_employer_profit = session.config['employer_outside_option']
            q1_worker_profit = session.config['worker_outside_option']
            q2_wage = C.Q2_WAGE
            q2_worker_profit = q2_wage - q2_effort_cost
            q2_employer_profit = q2_effort_worth - q2_wage
            q3_wage_1 = C.Q3_WAGE_1
            q3_wage_2 = C.Q3_WAGE_2
            q3_employer_profit = q3_effort_worth_1 + q3_effort_worth_2 - q3_wage_1 - q3_wage_2
            q3_worker_profit_1 = q3_wage_1 - q3_effort_cost_1
            q3_worker_profit_2 = q3_wage_2 - q3_effort_cost_2
        else:
            q2_effort_worth = q2_efort_worth * session.config['exchange_rate']
            q3_effort_worth_1 = q3_efort_worth_1 * session.config['exchange_rate']
            q3_effort_worth_2 = q3_efort_worth_2 * session.config['exchange_rate']
            q2_effort_cost = q2_efort_cost * session.config['exchange_rate']
            q3_effort_cost_1 = q3_efort_cost_1 * session.config['exchange_rate']
            q3_effort_cost_2 = q3_efort_cost_2 * session.config['exchange_rate']
            q1_employer_profit = session.config['employer_outside_option']
            q1_worker_profit = session.config['worker_outside_option']
            q2_wage = C.Q2_WAGE * session.config['exchange_rate']
            q2_worker_profit = q2_wage - q2_effort_cost
            q2_employer_profit = q2_effort_worth - q2_wage
            q3_wage_1 = C.Q3_WAGE_1 * session.config['exchange_rate']
            q3_wage_2 = C.Q3_WAGE_2 * session.config['exchange_rate']
            q3_employer_profit = q3_effort_worth_1 + q3_effort_worth_2 - q3_wage_1 - q3_wage_2
            q3_worker_profit_1 = q3_wage_1 - q3_effort_cost_1
            q3_worker_profit_2 = q3_wage_2 - q3_effort_cost_2

        if data['information_type'] == 'submit_answer':
            my_id = player.id_in_group
            print('Received', data)
            if data['question'] == 'q1':
                print('Correct employer profit:', q1_employer_profit, 'Correct worker profit:', q1_worker_profit)
                print('Received employer profit:', data['employer_profit'], 'Received worker profit:',
                      data['worker_profit'])
                if int(data['employer_profit']) == q1_employer_profit and int(
                        data['worker_profit']) == q1_worker_profit:
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
                print('Received employer profit:', data['employer_profit'], 'Received worker profit:',
                      data['worker_profit'])
                print('Effort worth:', q2_effort_worth, 'Effort cost:', q2_effort_cost, 'Wage:', q2_wage)

                if int(data['employer_profit']) == q2_employer_profit and int(
                        data['worker_profit']) == q2_worker_profit:
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
                    print('Correct employer profit:', q3_employer_profit, 'Correct worker 1 profit:',
                          q3_worker_profit_1, 'Correct worker 2 profit:', q3_worker_profit_2)
                    print('Received employer profit:', data['employer_profit'], 'Received worker 1 profit:',
                          data['worker_profit'], 'Received worker 2 profit:', data['worker_profit_2'])
                    if int(data['employer_profit']) == q3_employer_profit and int(
                            data['worker_profit']) == q3_worker_profit_1 and int(
                            data['worker_profit_2']) == q3_worker_profit_2:
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


class InstructionsFirms(Page):
    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        if session.config['final'] is True and player.participant.is_employer is True:
            return True

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session

        name_low_effort = session.config['effort_names'][0]
        name_high_effort = session.config['effort_names'][1]

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
            q2_wage = C.Q2_WAGE
            q3_wage_1 = C.Q3_WAGE_1
            q3_wage_2 = C.Q3_WAGE_2
            max_wage = session.config['max_wage']
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
            q2_wage = C.Q2_WAGE * session.config['exchange_rate']
            q3_wage_1 = C.Q3_WAGE_1 * session.config['exchange_rate']
            q3_wage_2 = C.Q3_WAGE_2 * session.config['exchange_rate']
            max_wage = session.config['max_wage'] * session.config['exchange_rate']

        worker_example_profit_low_effort = worker_example_wage - low_effort_points_tokens
        worker_example_profit_high_effort = worker_example_wage - high_effort_points_tokens
        total_gain_low_effort_2_workers = 2 * gain_low_effort_2_workers
        total_gain_high_effort_2_workers = 2 * gain_high_effort_2_workers
        total_gain_mix_effort_2_workers = gain_low_effort_2_workers + gain_high_effort_2_workers
        gain_mix_effort_2_workers = int(total_gain_mix_effort_2_workers / 2) if total_gain_mix_effort_2_workers % 2 == 0 else total_gain_mix_effort_2_workers / 2
        profit_employer_example_1 = total_gain_high_effort_2_workers - 60 - 40
        profit_employer_example_2 = total_gain_mix_effort_2_workers - 60 - 40

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
        else:
            print('error: no market type')

        return dict(
            name_low_effort=name_low_effort,
            name_high_effort=name_high_effort,
            profit_employer_example_1=profit_employer_example_1,
            profit_employer_example_2=profit_employer_example_2,
            max_wage=max_wage,
            q2_effort_requested=C.Q2_EFFORT_REQUESTED,
            q2_effort_received=C.Q2_EFFORT_RECEIVED,
            q3_effort_received_1=C.Q3_EFFORT_RECEIVED_1,
            q3_effort_received_2=C.Q3_EFFORT_RECEIVED_2,
            q2_wage=q2_wage,
            q3_wage_1=q3_wage_1,
            q3_wage_2=q3_wage_2,
            total_gain_mix_effort_2_workers=total_gain_mix_effort_2_workers,
            gain_mix_effort_2_workers=gain_mix_effort_2_workers,
            total_gain_high_effort_2_workers=total_gain_high_effort_2_workers,
            total_gain_low_effort_2_workers=total_gain_low_effort_2_workers,
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

    @staticmethod
    def live_method(player: Player, data):
        session = player.session

        q2_efort_worth = session.config['MPL_high'][0] if C.Q2_EFFORT_RECEIVED == "standard" else session.config['MPL_low'][
            0]
        q3_efort_worth_1 = session.config['MPL_high'][1] if C.Q3_EFFORT_RECEIVED_1 == "standard" else \
        session.config['MPL_low'][1]
        q3_efort_worth_2 = session.config['MPL_high'][1] if C.Q3_EFFORT_RECEIVED_2 == "standard" else \
        session.config['MPL_low'][1]
        q2_efort_cost = session.config['effort_costs_points'][1] if C.Q2_EFFORT_RECEIVED == "standard" else \
        session.config['effort_costs_points'][0]
        q3_efort_cost_1 = session.config['effort_costs_points'][1] if C.Q3_EFFORT_RECEIVED_1 == "standard" else \
        session.config['effort_costs_points'][0]
        q3_efort_cost_2 = session.config['effort_costs_points'][1] if C.Q3_EFFORT_RECEIVED_2 == "standard" else \
        session.config['effort_costs_points'][0]

        if player.participant.currency_is_points:
            q2_effort_worth = q2_efort_worth
            q3_effort_worth_1 = q3_efort_worth_1
            q3_effort_worth_2 = q3_efort_worth_2
            q2_effort_cost = q2_efort_cost
            q3_effort_cost_1 = q3_efort_cost_1
            q3_effort_cost_2 = q3_efort_cost_2
            q1_employer_profit = session.config['employer_outside_option']
            q1_worker_profit = session.config['worker_outside_option']
            q2_wage = C.Q2_WAGE
            q2_worker_profit = q2_wage - q2_effort_cost
            q2_employer_profit = q2_effort_worth - q2_wage
            q3_wage_1 = C.Q3_WAGE_1
            q3_wage_2 = C.Q3_WAGE_2
            q3_employer_profit = q3_effort_worth_1 + q3_effort_worth_2 - q3_wage_1 - q3_wage_2
            q3_worker_profit_1 = q3_wage_1 - q3_effort_cost_1
            q3_worker_profit_2 = q3_wage_2 - q3_effort_cost_2
        else:
            q2_effort_worth = q2_efort_worth * session.config['exchange_rate']
            q3_effort_worth_1 = q3_efort_worth_1 * session.config['exchange_rate']
            q3_effort_worth_2 = q3_efort_worth_2 * session.config['exchange_rate']
            q2_effort_cost = q2_efort_cost * session.config['exchange_rate']
            q3_effort_cost_1 = q3_efort_cost_1 * session.config['exchange_rate']
            q3_effort_cost_2 = q3_efort_cost_2 * session.config['exchange_rate']
            q1_employer_profit = session.config['employer_outside_option']
            q1_worker_profit = session.config['worker_outside_option']
            q2_wage = C.Q2_WAGE * session.config['exchange_rate']
            q2_worker_profit = q2_wage - q2_effort_cost
            q2_employer_profit = q2_effort_worth - q2_wage
            q3_wage_1 = C.Q3_WAGE_1 * session.config['exchange_rate']
            q3_wage_2 = C.Q3_WAGE_2 * session.config['exchange_rate']
            q3_employer_profit = q3_effort_worth_1 + q3_effort_worth_2 - q3_wage_1 - q3_wage_2
            q3_worker_profit_1 = q3_wage_1 - q3_effort_cost_1
            q3_worker_profit_2 = q3_wage_2 - q3_effort_cost_2

        if data['information_type'] == 'submit_answer':
            my_id = player.id_in_group
            print('Received', data)
            if data['question'] == 'q1':
                print('Correct employer profit:', q1_employer_profit, 'Correct worker profit:', q1_worker_profit)
                print('Received employer profit:', data['employer_profit'], 'Received worker profit:',
                      data['worker_profit'])
                if int(data['employer_profit']) == q1_employer_profit and int(
                        data['worker_profit']) == q1_worker_profit:
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
                print('Received employer profit:', data['employer_profit'], 'Received worker profit:',
                      data['worker_profit'])
                if int(data['employer_profit']) == q2_employer_profit and int(
                        data['worker_profit']) == q2_worker_profit:
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
                    print('Correct employer profit:', q3_employer_profit, 'Correct worker 1 profit:',
                          q3_worker_profit_1, 'Correct worker 2 profit:', q3_worker_profit_2)
                    print('Received employer profit:', data['employer_profit'], 'Received worker 1 profit:',
                          data['worker_profit'], 'Received worker 2 profit:', data['worker_profit_2'])
                    if int(data['employer_profit']) == q3_employer_profit and int(
                            data['worker_profit']) == q3_worker_profit_1 and int(
                            data['worker_profit_2']) == q3_worker_profit_2:
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
                 InstructionsWorkers,
                 InstructionsFirms,
                 WaitToStart]
def custom_export(player):
    # top row
    yield ['playerID', 'question', 'correct']

    # data rows
    quiz_responses = QuizResponses.filter()
    for response in quiz_responses:
        yield [response.playerID, response.question, response.correct]