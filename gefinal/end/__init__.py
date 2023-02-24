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
    total_payoff = models.IntegerField()
    total_euros = models.FloatField()


# PAGES
class WaitForOtherPlayers(WaitPage):
    body_text = "Please wait until all participants finished the experiment."


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        player.total_payoff = int(sum(filter(None, player.participant.vars['total_points'])))
        player.total_euros = float(sum(filter(None, player.participant.vars['realpay'])))
        player.total_euros = session.config['showup_fee'] if player.total_euros < session.config['showup_fee'] else player.total_euros
        return dict(
            total_payoff=player.total_payoff,
            total_euros=player.total_euros,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        session = player.session
        player.total_payoff = int(sum(filter(None, player.participant.vars['total_points'])))
        player.total_euros = float(sum(filter(None, player.participant.vars['realpay'])))
        player.total_euros = session.config['showup_fee'] if player.total_euros < session.config['showup_fee'] else player.total_euros
        player.large_market = player.participant.vars['large_market']
        player.small_market = player.participant.vars['small_market']
        player.is_employer = player.participant.vars['is_employer']
        player.playerID = player.participant.vars['playerID']
        player.string_role = player.participant.vars['string_role']



page_sequence = [Results]
