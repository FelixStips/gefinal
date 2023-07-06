from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'questionnaire2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Q1 = models.StringField(
        label="What would you prefer: a draw with a 50 percent chance of receiving amount 300, "
              "and the same 50 percent chance of receiving nothing, or the amount of 160 as a sure payment? ",
        choices=['Less than high school', 'High school', 'Some college', 'Bachelor’s degree', 'Master’s degree', 'Doctorate', 'Other', 'Prefer not to say'])


# PAGES
class Q1(Page):
    form_model = 'player'
    form_fields = ['Q1']

class Q2(Page):
    form_model = 'player'
    form_fields = ['Q1']

class Q3(Page):
    form_model = 'player'
    form_fields = ['Q1']

class Q4(Page):
    form_model = 'player'
    form_fields = ['Q1']

class Q5(Page):
    form_model = 'player'
    form_fields = ['Q1']


page_sequence = [Q1,
                 Q2,
                 Q3,
                 Q4,
                 Q5]