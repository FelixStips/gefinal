from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'prequestionnaire'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    is_employer = models.BooleanField()
    large_market = models.BooleanField()
    small_market = models.BooleanField()
    migrant = models.BooleanField()
    email = models.StringField(
        label="""Please enter <b>your PayPal email address</b> below, so that we can transfer the money to your account.""", )
    feedback = models.StringField(
        label="""If you want to provide some feedback on the experiment, use the field below.""", )

    age = models.IntegerField(
        label="What is your age?",
        min=0,
        max=100)
    gender = models.StringField(
        label="What is your gender?",
        choices=['Female', 'Male', 'Other', 'Prefer not to say'])
    country_of_birth = models.StringField(
        label="What is your country of birth?",
        choices=['United Kingdom','Other European','Other non-European','Prefer not to say'])

# FUNCTIONS
def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        p.is_employer = p.participant.vars.get('is_employer', False)
        p.large_market = p.participant.vars.get('large_market', False)
        p.small_market = p.participant.vars.get('small_market', False)
        p.migrant = p.participant.vars.get('migrant', False)

# PAGES
class Employer(Page):
    form_model = 'player'
    form_fields = ['age']

    @staticmethod
    def is_displayed(player: Player):
        return player.is_employer and player.large_market


class Native(Page):
    form_model = 'player'
    form_fields = ['gender']

    @staticmethod
    def is_displayed(player: Player):
        return not player.is_employer and not player.migrant



class Migrant(Page):
    form_model = 'player'
    form_fields = ['country_of_birth']


    @staticmethod
    def is_displayed(player: Player):
        return not player.is_employer and player.migrant


page_sequence = [Employer,
                 Native,
                 Migrant]
