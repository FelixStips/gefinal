from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'midbreak'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES

class AnotherIntroduction(Page):
    pass

class AnotherInstruction(Page):


    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        return dict(
            size_large_market=session.config['size_large_market'],
            size_small_market=session.config['size_small_market'],
            num_employers_large_market=session.config['num_employers_large_market'],
            num_employers_small_market=session.config['num_employers_small_market'],
            num_workers_large_market=session.config['size_large_market'] - session.config['num_employers_large_market'],
            num_workers_small_market=session.config['size_small_market'] - session.config['num_employers_small_market'],
            migration_small_shock_size=session.config['migration_small_shock_size'],
            migration_large_shock_size=session.config['migration_large_shock_size'],
            exchange_rate_large_market=session.config['exchange_rate_large_market'],
            exchange_rate_small_market=session.config['exchange_rate_small_market'],
            income_differential=session.config['exchange_rate_small_market']/session.config['exchange_rate_large_market'],
            example_wage=50,
            example_wage_large_market=50*(session.config['exchange_rate_small_market']/session.config['exchange_rate_large_market']),
            num_rounds_left=session.config['total_rounds'] - session.config['shock_after_rounds'],
            migrant=player.participant.vars['migrant'],
            move_to_market_1=player.participant.vars['move_to_market_1'],
            move_to_market_2=player.participant.vars['move_to_market_2'],
            large_market=player.participant.vars['large_market'],
        )



class AnotherWaitPage(WaitPage):
    body_text = "Please wait, part 2 will begin shortly."


page_sequence = [AnotherIntroduction,
                 AnotherInstruction,
                 AnotherWaitPage]
