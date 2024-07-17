from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot


def quiz2_resp_gen(self):
    session = self.player.session
    player = self.player
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
        effort_worth = effort_worth

    worker_profit = q2_wage - effort_cost
    employer_profit = effort_worth - q2_wage

    if player.participant.currency_is_points:
        return dict(
            quiz2_worker=worker_profit,

            quiz2_employer=employer_profit,
        )
    else:
        return dict(
            quiz2_worker_tokens=worker_profit,

            quiz2_employer_tokens=employer_profit,
        )

def gen_resp_3(player):
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
        effort_worth = effort_worth

    # Calculate profits
    worker1_profit = q3_wage_1 - effort_cost_1
    worker2_profit = q3_wage_2 - effort_cost_2
    employer_profit = effort_worth - q3_wage_1 - q3_wage_2

    if player.participant.currency_is_points:
        return dict(quiz3_worker1=worker1_profit,
                    quiz3_worker2=worker2_profit,
                    quiz3_employer=employer_profit)
    else:
        return dict(quiz3_worker1_tokens=worker1_profit,
                    quiz3_worker2_tokens=worker2_profit,
                    quiz3_employer_tokens=employer_profit)


class PlayerBot(Bot):
    def play_round(self):
        if self.session.config.get('final', False):
            yield Introduction
            if not self.player.participant.is_employer:
                yield WorkerInstruction
            else:
                yield FirmInstruction
            quiz1_responses = dict(
                quiz1_worker=self.session.config['worker_outside_option'],

                quiz1_employer=self.session.config['employer_outside_option'],
            )
            yield quiz1, quiz1_responses

            yield quiz2, quiz2_resp_gen(self)
            resps = ['quiz3_worker1', 'quiz3_worker2', 'quiz3_employer']

            yield quiz3, gen_resp_3(self.player)
