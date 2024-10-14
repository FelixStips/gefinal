from otree.api import Bot, Currency as c, currency_range
from . import *

class PlayerBot(Bot):
    def play_round(self):
        # If the player is an employer
        if self.player.is_employer and self.player.large_market:
            yield Employer, dict(
                empl_effort_expectation="somewhat more effort than I expected.",  # Option from choices
                empl_retaining_workers="Moderately important",  # Option from choices
                empl_hiring_confidence="Moderately confident",  # Option from choices
                empl_strategy="I maintained wages to preserve worker effort"  # Option from choices
            )

        # If the player is a native worker
        elif not self.player.is_employer and not self.player.migrant:
            yield Native, dict(
                nat_motivation_change="It slightly motivated me",  # Option from choices
                nat_wage_perception="higher",  # Option from choices
                nat_wage_increase_percentage="10",  # Example input for wage increase
                nat_wage_decrease_percentage="",  # This remains blank since perception is "higher"
                nat_wage_fairness="Neutral",  # Option from choices
                nat_wage_adjustment_reasonable="Yes, somewhat reasonable",  # Option from choices
                nat_unemployment_risk="Yes, somewhat",  # Option from choices
                Threatened=True,
                Confident=False,
                Resentful_employers=False,
                Resentful_workers=False,
                Grateful_employers=True,
                Grateful_workers=False,
                Indifferent=False,
                Other=False,
                No_emotion=False
            )

        # If the player is a migrant
        elif not self.player.is_employer and self.player.migrant:
            yield Migrant, dict(
                mig_wage_perception="lower",  # Option from choices
                mig_wage_increase_percentage="",  # This remains blank since perception is "lower"
                mig_wage_decrease_percentage="5",  # Example input for wage decrease
                mig_motivation_change="My motivation remained the same as before",  # Option from choices
                mig_motivation_evolution="I became more motivated over time",  # Option from choices
                mig_pressure_to_work_harder="Yes, a bit"  # Option from choices
            )
