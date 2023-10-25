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
    email = models.StringField(label="""Please enter <b>your PayPal email address</b> below, so that we can transfer the money to your account.""",)
    feedback = models.StringField(label="""If you want to provide some feedback on the experiment, use the field below.""",)


# PAGES
class PreResults(Page):
    form_model = 'player'


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        session = player.session
        print('Player', player.participant.playerID, 'had total payoff of', player.participant.vars['total_points'],
              'points and', player.participant.vars['total_tokens'], 'tokens.')

        total_points_filtered = filter(lambda x: x is not None, player.participant.vars['total_points'])
        total_tokens_filtered = filter(lambda x: x is not None, player.participant.vars['total_tokens'])

        print('Player', player.participant.playerID, 'had total payoff of', total_points_filtered, 'points and',
              total_tokens_filtered, 'tokens.')

        player.total_points = sum(filter(lambda x: x is not None, player.participant.vars['total_points']))
        player.total_tokens = sum(filter(lambda x: x is not None, player.participant.vars['total_tokens']))
        player.total_euros = round(
            session.config['payout_rate'] * player.total_points + session.config['showup_fee'],
            2) if player.total_points > 0 else round(session.config['showup_fee'], 2)
        player.large_market = player.participant.vars['large_market']
        player.small_market = player.participant.vars['small_market']
        player.is_employer = player.participant.vars['is_employer']
        player.playerID = player.participant.vars['playerID']
        player.string_role = player.participant.vars['string_role']


class Results(Page):
    form_model = 'player'
    form_fields = ['email']

    @staticmethod
    def vars_for_template(player: Player):

        return dict(
            total_points=player.total_points,
            total_tokens=player.total_tokens,
            total_euros=player.total_euros,
            currency_is_points=player.participant.vars['currency_is_points'],
        )


class End(Page):
    form_model = 'player'
    form_fields = ['feedback']


class Close(Page):
    pass

page_sequence = [PreResults,
                 Results,
                 End,
                 Close]
