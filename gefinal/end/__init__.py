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
    total_points = models.FloatField()
    total_tokens = models.FloatField()
    total_euros = models.FloatField()


# PAGES
class WaitForOtherPlayers(WaitPage):
    body_text = "Please wait until all participants finished the experiment."


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        player.total_points = sum(filter(None, player.participant.vars['total_points']))
        player.total_tokens = sum(filter(None, player.participant.vars['total_tokens']))
        player.total_euros = session.config['exchange_to_euros'] * player.total_points + session.config['showup_fee'] if player.total_points > 0 else session.config['showup_fee']
        return dict(
            total_points=player.total_points,
            total_tokens=player.total_tokens,
            total_euros=player.total_euros,
            currency_is_points=player.participant.vars['currency_is_points'],
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        session = player.session
        player.total_points = sum(filter(None, player.participant.vars['total_points']))
        player.total_tokens = sum(filter(None, player.participant.vars['total_tokens']))
        player.total_euros = session.config['exchange_to_euros'] * player.total_points + session.config['showup_fee'] if player.total_points > 0 else session.config['showup_fee']
        player.large_market = player.participant.vars['large_market']
        player.small_market = player.participant.vars['small_market']
        player.is_employer = player.participant.vars['is_employer']
        player.playerID = player.participant.vars['playerID']
        player.string_role = player.participant.vars['string_role']



page_sequence = [Results]
