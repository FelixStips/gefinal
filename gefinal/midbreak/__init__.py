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
    def app_after_this_page(player, upcoming_apps):
        if player.participant.vars['small_market'] and not player.participant.vars['migrant']:
            return "questionnaire"

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        print(session.config['exchange_rate'])
        income_diff = True if session.config['exchange_rate'] == 1 else False

        if player.participant.vars['large_market_1'] or player.participant.vars['move_to_market_1']:
            size_market = session.config['size_large_market'] + session.config['migration_small_shock_size']
            num_employers = session.config['num_employers_large_market']
            num_workers = session.config['size_large_market'] + session.config['migration_small_shock_size'] - session.config['num_employers_large_market']
            shock_size = session.config['migration_small_shock_size']
        elif player.participant.vars['large_market_2'] or player.participant.vars['move_to_market_2']:
            size_market = session.config['size_small_market'] + session.config['migration_large_shock_size']
            num_employers = session.config['num_employers_large_market']
            num_workers = session.config['size_small_market'] + session.config['migration_large_shock_size'] - session.config['num_employers_large_market']
            shock_size = session.config['migration_large_shock_size']
        else:
            size_market = session.config['size_small_market']
            num_employers = session.config['num_employers_small_market']
            num_workers = session.config['size_small_market'] - session.config['num_employers_small_market'] - session.config['migration_large_shock_size'] - session.config['migration_large_shock_size']
            shock_size = 0
        return dict(
            income_diff=income_diff,
            size_market=size_market,
            num_employers=num_employers,
            num_workers=num_workers,
            is_employer=player.participant.vars['is_employer'],
            shock_size=shock_size,
            num_rounds_left=session.config['total_rounds'] - session.config['shock_after_rounds'],
            migrant=player.participant.vars['migrant'],
            large_market=player.participant.vars['large_market'],
        )



class AnotherWaitPage(WaitPage):
    body_text = "Please wait, part 2 will begin shortly."


page_sequence = [AnotherIntroduction,
                 AnotherInstruction,
                 AnotherWaitPage]
