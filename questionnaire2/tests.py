from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

class PlayerBot(Bot):
    def play_round(self):
        yield Q1, dict(Q1 = 1)
        yield Q2A, dict(Q2A = 1)
        yield Q3AA, dict(Q3AA = 1)
        yield Q4AAA, dict(Q4AAA = 1)
        yield Q5AAAA, dict(Q5AAAA = 1)

