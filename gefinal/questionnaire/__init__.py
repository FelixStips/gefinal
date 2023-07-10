from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'questionnaire'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.StringField(
        label="What is your age?")
    gender = models.StringField(label="What is your gender?", choices=['Female', 'Male', 'Other', 'Prefer not to say'])
    education = models.StringField(
        label="What is the highest level of education you have completed?",
        choices=['Less than high school', 'High school', 'Some college', 'Bachelor’s degree', 'Master’s degree', 'Doctorate', 'Other', 'Prefer not to say'])
    education_field = models.StringField(
        label="What is your field of study?",
        choices=['Arts','Business','Economics','Finance','Law','Mathematics','Medicine','Psychology','Natural Sciences','Engineering','Not applicable','Other','Prefer not to say'])
    country_of_birth = models.StringField(
        label="What is your country of birth?",
        choices=['United Kingdom','Other European','Other non-European','Prefer not to say'])
    country_of_residence = models.StringField(
        label="What is your country of residence?",
        choices=['United Kingdom','Other European','Other non-European','Prefer not to say'])
    RA1 = models.StringField(
        label="""If you’re running a race and you pass the person in second place, what place are you in? """,
        choices=['1st', '2nd', '3rd']
    )
    RA2 = models.StringField(
        label="""A farmer had 15 sheep and all but 8 died. How many are left?""")
    RA3 = models.StringField(
        label="""A High-End Smartphone and a pair of Wireless Earbuds cost 1100 £ together,
           and the High-End Smartphone costs 1000 £ more than the pair of Wireless Earbuds, how much does the pair of Wireless Earbuds cost?""")
    AF21 = models.StringField(
        label="""<b>Please tell us, in general, how willing or unwilling you are to take risks.</b> <br> 
                <i>Please use a scale from 0 to 10, where 0 means “completely unwilling to take
                risks” and a 10 means you are “very willing to take risks”. You can also use any numbers
                between 0 and 10 to indicate where you fall on the scale, like 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.</i>""",
        widget=widgets.RadioSelectHorizontal,
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    )
    AF31 = models.StringField(
        label=""" <b>When someone does me a favor I am willing to return it.</b>
                    """,
        widget=widgets.RadioSelectHorizontal,
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    )
    AF32 = models.StringField(
        label="""<b>Please think about what you would do in the following situation.</b><br>
                <i>You are in an area you are not familiar with, and you realize you lost your way. You ask a
                stranger for directions. The stranger offers to take you to your destination. Helping you costs
                the stranger about 20£ in total. However, the stranger says he or she does not want any
                money from you. You have six presents with you. The cheapest present costs 5£, the most
                expensive one costs 30£. Do you give one of the presents to the stranger as a “thank-you”-
                gift? If so, which present do you give to the stranger?</i>""",
        choices=['No present', 'The present worth 5£', 'The present worth 10£', 'The present worth 15£', 'The present worth 20£',
                 'The present worth 25£', 'The present worth 30£'],
    )
    AF41 = models.StringField(
        label=""" <b>If I am treated very unjustly, I will take revenge at the first occasion, even if there is a cost to do so.</b>
                    """,
        widget=widgets.RadioSelectHorizontal,
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    )
    AF42 = models.StringField(
        label=""" <b>How willing are you to punish someone who treats you unfairly, even if there may be costs for you?</b>""",
        widget=widgets.RadioSelectHorizontal,
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    )

    AF43 = models.StringField(
        label=""" <b>How willing are you to punish someone who treats others unfairly, even if there may be costs for you?</b>""",
        widget=widgets.RadioSelectHorizontal,
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    )

    # PAGES
class SocioDemographic(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'education_field', 'country_of_birth', 'country_of_residence']

class CognitiveReflection(Page):
    form_model = 'player'
    form_fields = ['RA1', 'RA2', 'RA3']

class Behavioral1(Page):
    form_model = 'player'
    form_fields = ['AF21', 'AF32']

class Behavioral2(Page):
    form_model = 'player'
    form_fields = ['AF31', 'AF41']

class Behavioral3(Page):
    form_model = 'player'
    form_fields = ['AF42', 'AF43']


page_sequence = [SocioDemographic,
                 CognitiveReflection,
                 Behavioral1,
                 Behavioral2,
                 Behavioral3]