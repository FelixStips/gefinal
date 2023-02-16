from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'end'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class WaitForOtherPlayers(WaitPage):
    body_text = "Please wait until all participants finished the experiment."


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        all_players = player.participant.in_all_rounds()
        return dict(
            total_payoff=sum([p.payoff for p in all_players]),
        )


page_sequence = [WaitForOtherPlayers,
                 Results]
