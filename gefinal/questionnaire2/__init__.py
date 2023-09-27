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
    playerID = models.IntegerField()
    Q1 = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
              and the same 50 percent chance of receiving nothing, or the amount of 160£ as a sure payment?<br>""",
        widget=widgets.RadioSelect,
        choices=[
                    [1, '50 percent chance of receiving 300£'],
                    [0, '160£ as a sure payment'],
                ])
    Q2A = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
              and the same 50 percent chance of receiving nothing, or the amount of 240£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '240£ as a sure payment']])
    Q2B = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
              and the same 50 percent chance of receiving nothing, or the amount of 80£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '80£ as a sure payment']])
    Q3AA = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
              and the same 50 percent chance of receiving nothing, or the amount of 280£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '280£ as a sure payment']])
    Q3AB = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
                and the same 50 percent chance of receiving nothing, or the amount of 200£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '200£ as a sure payment']])
    Q3BA = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
              and the same 50 percent chance of receiving nothing, or the amount of 120£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '120£ as a sure payment']])
    Q3BB = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
              and the same 50 percent chance of receiving nothing, or the amount of 40£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '40£ as a sure payment']])
    Q4AAA = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
              and the same 50 percent chance of receiving nothing, or the amount of 300£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '300£ as a sure payment']])
    Q4AAB = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
              and the same 50 percent chance of receiving nothing, or the amount of 260£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '260£ as a sure payment']])
    Q4ABA = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
              and the same 50 percent chance of receiving nothing, or the amount of 220£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '220£ as a sure payment']])
    Q4ABB = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
              and the same 50 percent chance of receiving nothing, or the amount of 180£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '180£ as a sure payment']])
    Q4BAA = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
              and the same 50 percent chance of receiving nothing, or the amount of 140£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '140£ as a sure payment']])
    Q4BAB = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
              and the same 50 percent chance of receiving nothing, or the amount of 100£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '100£ as a sure payment']])
    Q4BBA = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
              and the same 50 percent chance of receiving nothing, or the amount of 60£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '60£ as a sure payment']])
    Q4BBB = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
              and the same 50 percent chance of receiving nothing, or the amount of 20£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '20£ as a sure payment']])
    Q5AAAA = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
                 and the same 50 percent chance of receiving nothing, or the amount of 310£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '310£ as a sure payment']])
    Q5AAAB = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
                 and the same 50 percent chance of receiving nothing, or the amount of 290£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '290£ as a sure payment']])
    Q5AABA = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
                 and the same 50 percent chance of receiving nothing, or the amount of 270£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '270£ as a sure payment']])
    Q5AABB = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
                 and the same 50 percent chance of receiving nothing, or the amount of 250£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '250£ as a sure payment']])
    Q5ABAA = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
                 and the same 50 percent chance of receiving nothing, or the amount of 230£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '230£ as a sure payment']])
    Q5ABAB = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
                 and the same 50 percent chance of receiving nothing, or the amount of 210£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '210£ as a sure payment']])
    Q5ABBA = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
                 and the same 50 percent chance of receiving nothing, or the amount of 190£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '190£ as a sure payment']])
    Q5ABBB = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
                 and the same 50 percent chance of receiving nothing, or the amount of 170£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '170£ as a sure payment']])
    Q5BAAA = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
                 and the same 50 percent chance of receiving nothing, or the amount of 150£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '150£ as a sure payment']])
    Q5BAAB = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
                 and the same 50 percent chance of receiving nothing, or the amount of 130£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '130£ as a sure payment']])
    Q5BABA = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
                 and the same 50 percent chance of receiving nothing, or the amount of 110£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '110£ as a sure payment']])
    Q5BABB = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
                 and the same 50 percent chance of receiving nothing, or the amount of 90£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '90£ as a sure payment']])
    Q5BBAA = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
                 and the same 50 percent chance of receiving nothing, or the amount of 70£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '70£ as a sure payment']])
    Q5BBAB = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
                 and the same 50 percent chance of receiving nothing, or the amount of 50£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '50£ as a sure payment']])
    Q5BBBA = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
                 and the same 50 percent chance of receiving nothing, or the amount of 30£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '30£ as a sure payment']])
    Q5BBBB = models.StringField(
        label="""What would you prefer: a draw with a 50 percent chance of receiving amount 300£
                 and the same 50 percent chance of receiving nothing, or the amount of 10£ as a sure payment?""",
        widget=widgets.RadioSelect,
        choices=[[1, '50 percent chance of receiving 300£'],
                 [0, '10£ as a sure payment']])

# PAGES
class Q1(Page):
    form_model = 'player'
    form_fields = ['Q1']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        session = player.session
        player.playerID = player.participant.vars['playerID']

class Q2A(Page):
    form_model = 'player'
    form_fields = ['Q2A']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q1') == '1'


class Q2B(Page):
    form_model = 'player'
    form_fields = ['Q2B']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q1') == '0'

class Q3AA(Page):
    form_model = 'player'
    form_fields = ['Q3AA']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q2A') == '1'

class Q3AB(Page):
    form_model = 'player'
    form_fields = ['Q3AB']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q2A') == '0'

class Q3BA(Page):
    form_model = 'player'
    form_fields = ['Q3BA']
    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q2B') == '1'

class Q3BB(Page):
    form_model = 'player'
    form_fields = ['Q3BB']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q2B') == '0'

class Q4AAA(Page):
    form_model = 'player'
    form_fields = ['Q4AAA']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q3AA') == '1'

class Q4AAB(Page):
    form_model = 'player'
    form_fields = ['Q4AAB']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q3AA') == '0'

class Q4ABA(Page):
    form_model = 'player'
    form_fields = ['Q4ABA']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q3AB') == '1'

class Q4ABB(Page):
    form_model = 'player'
    form_fields = ['Q4ABB']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q3AB') == '0'

class Q4BAA(Page):
    form_model = 'player'
    form_fields = ['Q4BAA']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q3BA') == '1'

class Q4BAB(Page):
    form_model = 'player'
    form_fields = ['Q4BAB']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q3BA') == '0'


class Q4BBA(Page):
    form_model = 'player'
    form_fields = ['Q4BBA']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q3BB') == '1'


class Q4BBB(Page):
    form_model = 'player'
    form_fields = ['Q4BBB']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q3BB') == '0'


class Q5AAAA(Page):
    form_model = 'player'
    form_fields = ['Q5AAAA']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q4AAA') == '1'

class Q5AAAB(Page):
    form_model = 'player'
    form_fields = ['Q5AAAB']
    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q4AAA') == '0'

class Q5AABA(Page):
    form_model = 'player'
    form_fields = ['Q5AABA']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q4AAB') == '1'


class Q5AABB(Page):
    form_model = 'player'
    form_fields = ['Q5AABB']
    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q4AAB') == '0'



class Q5ABAA(Page):
    form_model = 'player'
    form_fields = ['Q5ABAA']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q4ABA') == '1'


class Q5ABAB(Page):
    form_model = 'player'
    form_fields = ['Q5ABAB']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q4ABA') == '0'


class Q5ABBA(Page):
    form_model = 'player'
    form_fields = ['Q5ABBA']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q4ABB') == '1'


class Q5ABBB(Page):
    form_model = 'player'
    form_fields = ['Q5ABBB']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q4ABB') == '0'


class Q5BAAA(Page):
    form_model = 'player'
    form_fields = ['Q5BAAA']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q4BAA') == '1'


class Q5BAAB(Page):
    form_model = 'player'
    form_fields = ['Q5BAAB']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q4BAA') == '0'

class Q5BABA(Page):
    form_model = 'player'
    form_fields = ['Q5BABA']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q4BAB') == '1'


class Q5BABB(Page):
    form_model = 'player'
    form_fields = ['Q5BABB']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q4BAB') == '0'


class Q5BBAA(Page):
    form_model = 'player'
    form_fields = ['Q5BBAA']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q4BBA') == '1'


class Q5BBAB(Page):
    form_model = 'player'
    form_fields = ['Q5BBAB']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q4BBA') == '0'


class Q5BBBA(Page):
    form_model = 'player'
    form_fields = ['Q5BBBA']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q4BBB') == '1'


class Q5BBBB(Page):
    form_model = 'player'
    form_fields = ['Q5BBBB']

    @staticmethod
    def is_displayed(player: Player):
        return player.field_maybe_none('Q4BBB') == '0'





page_sequence = [Q1,
                 Q2A,
                 Q2B,
                 Q3AA,
                 Q3AB,
                 Q3BA,
                 Q3BB,
                 Q4AAA,
                 Q4AAB,
                 Q4ABA,
                 Q4ABB,
                 Q4BAA,
                 Q4BAB,
                 Q4BBA,
                 Q4BBB,
                 Q5AAAA,
                 Q5AAAB,
                 Q5AABA,
                 Q5AABB,
                 Q5ABAA,
                 Q5ABAB,
                 Q5ABBA,
                 Q5ABBB,
                 Q5BAAA,
                 Q5BAAB,
                 Q5BABA,
                 Q5BABB,
                 Q5BBAA,
                 Q5BBAB,
                 Q5BBBA,
                 Q5BBBB]

