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
    large_market = models.BooleanField()
    small_market = models.BooleanField()
    is_employer = models.BooleanField()
    playerID = models.IntegerField()
    string_role = models.StringField()


# PAGES
class WaitForOtherPlayers(WaitPage):
    body_text = "Please wait until all participants finished the experiment."


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        all_players = player.participant.in_all_rounds()
        return dict(
            total_payoff=sum([p.payoff for p in all_players]),
            total_euros=sum(e for e in player.participant.vars['realpay'] if e == e),
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.total_payoff = sum([p.payoff for p in player.participant.in_all_rounds()])
        player.total_euros = sum(e for e in player.participant.vars['realpay'] if e == e)
        player.large_market = player.participant.vars['large_market']
        player.small_market = player.participant.vars['small_market']
        player.is_employer = player.participant.vars['is_employer']
        player.playerID = player.participant.vars['playerID']
        player.string_role = player.participant.vars['string_role']



page_sequence = [WaitForOtherPlayers,
                 Results]
