from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

class PlayerBot(Bot):
    def play_round(self):
        if self.is_employer == True:
            yield InstructionsFirms
        else:
            yield InstructionsWorkers

