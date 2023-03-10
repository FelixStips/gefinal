from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'midbreak'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    offer_fair_1 = models.StringField(
        label="""<p style="margin-top:1cm;">
                    How fair do you find this job offer? Wage=20 and Effort=10. <br> 
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
                    How fair do you find this job offer? Wage=50 and Effort=10. <br> 
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
                    How fair do you find this job offer? Wage=80 and Effort=10. <br> 
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
class Question(Page):
    form_model = 'player'
    form_fields = ['offer_fair_1', 'offer_fair_2', 'offer_fair_3']

class AnotherIntroduction(Page):
    pass

class AnotherInstruction(Page):


    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        return dict(
            size_large_market=session.config['size_large_market'],
            size_small_market=session.config['size_small_market'],
            num_employers_large_market=session.config['num_employers_large_market'],
            num_employers_small_market=session.config['num_employers_small_market'],
            num_workers_large_market=session.config['size_large_market'] - session.config['num_employers_large_market'],
            num_workers_small_market=session.config['size_small_market'] - session.config['num_employers_small_market'],
            migration_shock_size=session.config['migration_shock_size'],
            exchange_rate_large_market=session.config['exchange_rate_large_market'],
            exchange_rate_small_market=session.config['exchange_rate_small_market'],
            income_differential=session.config['exchange_rate_small_market']/session.config['exchange_rate_large_market'],
            example_wage=50,
            example_wage_large_market=50*(session.config['exchange_rate_small_market']/session.config['exchange_rate_large_market']),
            num_rounds_left=session.config['total_rounds'] - session.config['shock_after_rounds'],
            migrant=player.participant.vars['migrant'],
            large_market=player.participant.vars['large_market'],
        )



class AnotherWaitPage(WaitPage):
    body_text = "Please wait, part 2 will begin shortly."


page_sequence = [Question,
                 AnotherIntroduction,
                 AnotherInstruction,
                 AnotherWaitPage]
