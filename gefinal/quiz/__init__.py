from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'quiz'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    offer_fair_1 = models.StringField(
        label="""<p style="margin-top:1cm;">
                    How fair do you find this job offer?<br> 
                    <ul class="list-group">
                      <li class="list-group-item">Job 3</li>
                      <li class="list-group-item">Wage: 20</li>
                      <li class="list-group-item">Effort requested: 10</li>
                    </ul>
                    <i>Please use a scale from 1 to 5, where 1 means you are “completely unfair” and 5 means "completely fair". 
                    You can also use the values in-between to indicate where you fall on the scale.</i>
                </p>""",
        choices=['1 - completely unfair',
                 '2 - unfair',
                 '3 - neutral',
                 '4 - fair',
                 '5 - completely fair']
    )
    offer_fair_2 = models.StringField(
        label="""<p style="margin-top:1cm;">
                    How fair do you find this job offer? <br> 
                    <ul class="list-group">
                      <li class="list-group-item">Job 3</li>
                      <li class="list-group-item">Wage: 50</li>
                      <li class="list-group-item">Effort requested: 10</li>
                    </ul>
                    <i>Please use a scale from 1 to 5, where 1 means you are “completely unfair” and 5 means "completely fair". 
                    You can also use the values in-between to indicate where you fall on the scale.</i>
                </p>""",
        choices=['1 - completely unfair',
                 '2 - unfair',
                 '3 - neutral',
                 '4 - fair',
                 '5 - completely fair']
    )
    offer_fair_3 = models.StringField(
        label="""<p style="margin-top:1cm;">
                    How fair do you find this job offer? <br> 
                    <ul class="list-group">
                      <li class="list-group-item">Job 3</li>
                      <li class="list-group-item">Wage: 80</li>
                      <li class="list-group-item">Effort requested: 10</li>
                    </ul>
                    <i>Please use a scale from 1 to 5, where 1 means you are “completely unfair” and 5 means "completely fair". 
                    You can also use the values in-between to indicate where you fall on the scale.</i>
                </p>""",
        choices=['1 - completely unfair',
                 '2 - unfair',
                 '3 - neutral',
                 '4 - fair',
                 '5 - completely fair']
    )


# PAGES
class QuestionsIntro(Page):
    pass

class Questions(Page):
    form_model = 'player'
    form_fields = ['offer_fair_1', 'offer_fair_2', 'offer_fair_3']



page_sequence = [QuestionsIntro,
                 Questions]

