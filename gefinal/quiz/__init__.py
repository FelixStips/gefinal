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
        label="""<p style="margin-top:0cm;">
                    How fair do you find this job offer?<br> 
                    <i>Please use a scale from 1 to 5, where 1 means you are “completely unfair” and 5 means "completely fair". 
                    You can also use the values in-between to indicate where you fall on the scale.</i>
                    <table class="table table-bordered table-sm">
                        <thead class="thead-light">
                            <tr class="table-light">
                                <th class="col-3">Job ID</th>
                                <th class="col-3">Wage</th>
                                <th class="col-3">Effort</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="col-3"> 1 </td>
                                <td class="col-3"> 20 </td>
                                <td class="col-3"> 10 </td>
                            </tr>
                        </tbody>
                    </table>
                </p>""",
        choices=['1 - completely unfair',
                 '2 - unfair',
                 '3 - neutral',
                 '4 - fair',
                 '5 - completely fair']
    )
    offer_fair_2 = models.StringField(
        label="""<p style="margin-top:0cm;">
                    How fair do you find this job offer? <br> 
                    <i>Please use a scale from 1 to 5, where 1 means you are “completely unfair” and 5 means "completely fair". 
                    You can also use the values in-between to indicate where you fall on the scale.</i>
                    <table class="table table-bordered table-sm">
                        <thead class="thead-light">
                            <tr class="table-light">
                                <th scope="col">Job ID</th>
                                <th scope="col">Wage</th>
                                <th scope="col">Effort</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td> 1 </td>
                                <td> 50 </td>
                                <td> 10 </td>
                            </tr>
                        </tbody>
                    </table>
                </p>""",
        choices=['1 - completely unfair',
                 '2 - unfair',
                 '3 - neutral',
                 '4 - fair',
                 '5 - completely fair']
    )
    offer_fair_3 = models.StringField(
        label="""<p style="margin-top:0cm;">
                    How fair do you find this job offer? <br> 
                    <i>Please use a scale from 1 to 5, where 1 means you are “completely unfair” and 5 means "completely fair". 
                    You can also use the values in-between to indicate where you fall on the scale.</i>
                    <table class="table table-bordered table-sm">
                        <thead class="thead-light">
                            <tr class="table-light">
                                <th scope="col">Job ID</th>
                                <th scope="col">Wage</th>
                                <th scope="col">Effort</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td> 1 </td>
                                <td> 80 </td>
                                <td> 10 </td>
                            </tr>
                        </tbody>
                    </table>    
                 </p>""",
        choices=['1 - completely unfair',
                 '2 - unfair',
                 '3 - neutral',
                 '4 - fair',
                 '5 - completely fair']
    )


# PAGES
class QuestionsIntro(Page):
    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        return dict(
            rounds_played=session.config['shock_after_rounds'],
        )

class Question1(Page):
    form_model = 'player'
    form_fields = ['offer_fair_1']

    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        return session.config['final']

class Question2(Page):
    form_model = 'player'
    form_fields = ['offer_fair_2']

    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        return session.config['final']

class Question3(Page):
    form_model = 'player'
    form_fields = ['offer_fair_3']

    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        return session.config['final']



page_sequence = [QuestionsIntro,
                 Question1,
                 Question2,
                 Question3,]

