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
    parents_education = models.StringField(
        label="What is the highest level of education one or both of your parents completed?",
        choices=['Less than high school', 'High school', 'Some college', 'Bachelor’s degree', 'Master’s degree', 'Doctorate', 'Other', 'Prefer not to say'])
    R3 = models.StringField(
        label="""<p style="margin-top:1cm;">
                <b>Are you a person who is generally willing to take risks, or do you try avoid taking risks? </b>
                <br>
                <i>Please answer on a scale from 0 to 10, where 0 means you are "completely unwilling to take risks"
                 and 10 means you are "very willing to take risks". You can also use any numbers in between 0 and 10 
                 to indicate your willingness to take risks.</i>
                 </p>""",
        widget=widgets.RadioSelectHorizontal,
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "Don't know"]
    )
    bat_question = models.FloatField(
        label="A bat and a ball cost $1.10 in total. The bat costs $1 more than the ball. <br> How much does the ball cost? Please type only the number, without the dollar sign.",
        min=0,
    )
    widgets_question = models.IntegerField(
        label="If it takes five machines five minutes to make five widgets, how long would it take 100 machines to make 100 widgets?",
        min=0,
    )
    lake_question = models.IntegerField(
        label="""In a lake, there is a patch of lily pads. Every day, the patch doubles in size. <br>
              If it takes 48 days for the patch to cover the entire lake, how long would it take for the patch to cover half of the lake?""",
        min=0,
    )
    PR9 = models.StringField(
        label="""<p style="margin-top:1cm;">
                    <b>Imagine the following situation:</b> <br>
                    <i>You are shopping in an unfamiliar city and realize you lost your way. You ask a stranger for directions. 
                    The stranger offers to take you with their car to your destination. The ride takes about 20 minutes 
                    and costs the stranger about 20 Euro in total. The stranger does not want money for it. You carry 
                    six bottles of wine with you. The cheapest bottle costs 5 Euro, the most expensive one 30 Euro. 
                    You decide to give one of the bottles to the stranger as a thank-you gift.</i>
                </p> 
                    Which bottle do you give?""",
        choices=['The bottle for 5', 'The bottle for 10', 'The bottle for 15', 'The bottle for 20', 'The bottle for 25', 'The bottle for 30', "Don't know"],
    )
    NR11 = models.IntegerField(
        label="""
                 <p style="margin-top:1cm;">
                     <b>Please consider what you would do in the following situation</b>: 
                     <i>you and a stranger are involved in a car accident. You are not to blame for the accident, 
                     but the stranger claims that you ran a red light even though it was the stranger himself 
                     who ran the red light. Even though the stranger’s claim is false, the claim is believed 
                     to be correct and you have to pay a fine of 300 Euro. There was an eyewitness who saw what really happened.
                     If the eyewitness testifies, you don’t have to pay the fine but the stranger has to instead. 
                     In addition the stranger will then have to pay a fine for making a false testimony. 
                     Assume that there is detective who will definitely find the eyewitness, and that the eyewitness 
                     will testify if the detective finds him. </i>
                 </p> 
                 What is the maximum amount of money that you are willing to spend on hiring the detective?
                        """,
        min=0,
    )
    NR1 = models.StringField(
        label="""<p style="margin-top:1cm;">
                    <b>How do you see yourself: Are you a person who is generally willing to punish unfair behavior even if this is costly?</b> <br> 
                    <i>Please use a scale from 0 to 10, where 0 means you are “not willing at all to incur costs to punish unfair behavior” 
                    and a 10 means you are “very willing to incur costs to punish unfair behavior”. You can also use the values in-between to
                    indicate where you fall on the scale.</i>
                </p>""",
        widget=widgets.RadioSelectHorizontal,
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "Don't know"]
    )
    PR1 = models.StringField(
        label="""<b>Are you a person who is generally willing to go out of their way to return a favor or a help even if it is costly, or are you not willing to do so?</b> <br><br> 
                <i>Please use a scale from 0 to 10, where 0 means you are “not willing at all to incur costs to punish unfair behavior” 
                and a 10 means you are “very willing to incur costs to punish unfair behavior”. You can also use the values in-between to
                indicate where you fall on the scale.</i>""",
        widget=widgets.RadioSelectHorizontal,
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "Don't know"]
    )
    RA1 = models.StringField(
        label="""If you’re running a race and you pass the person in second place, what place are you in? """,
        choices=['1st', '2nd', '3rd']
    )
    RA2 = models.StringField(
        label="""A farmer had 15 sheep and all but 8 died. How many are left?""")
    RA3 = models.StringField(
        label="""A High-End Smartphone and a pair of Wireless Earbuds cost 1100 £ together, 
        and the High-End Smartphone costs 1000 £ more than the pair of Wireless Earbuds, how much does the pair of Wireless Earbuds cost?""")


# PAGES
class SocioDemographic(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'education_field', 'country_of_birth', 'country_of_residence']

class CognitiveReflection(Page):
    form_model = 'player'
    form_fields = ['RA1', 'RA2', 'RA3']

class Behavioral(Page):
    form_model = 'player'
    form_fields = ['R3', 'NR1', 'PR9']


page_sequence = [SocioDemographic,
                 CognitiveReflection,
                 Behavioral]