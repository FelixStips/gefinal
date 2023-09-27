from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

class PlayerBot(Bot):
    def play_round(self):
        yield SocioDemographic, dict(age=20, gender="Female", education="High school", education_field="Law",
                                     country_of_birth="Other European")
        yield Behavioral1, dict(AF21=1, AF32='No present')
        yield Behavioral2, dict(AF31=5, AF41=5)
        yield Behavioral3, dict(AF42=5, AF43=5)

