from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

class PlayerBot(Bot):
    def play_round(self):
        yield SocioDemographic, dict(age=20, gender='Female', education='High School', education_field='Arts',
                                     country_of_birth='Other European')
        yield Behavioral1, dict(AF21=5, AF32=5)
        yield Behavioral2, dict(AF31=5, AF41=5)
        yield Behavioral3, dict(AF42=5, AF43=5)

