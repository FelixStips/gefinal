from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'prequestionnaire'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    EMOTIONS = ['Threatened', 'Confident', 'Resentful_employers', 'Resentful_workers', 'Grateful_employers', 'Grateful_workers', 'Indifferent', 'Other', 'No_emotion']


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    is_employer = models.BooleanField()
    large_market = models.BooleanField()
    small_market = models.BooleanField()
    migrant = models.BooleanField()
    Threatened = models.BooleanField(
        label="Threatened",
        blank=True
    )
    Confident = models.BooleanField(
        label="Confident",
        blank=True
    )
    Resentful_employers = models.BooleanField(
        label="Resentful toward employers",
        blank=True
    )
    Resentful_workers = models.BooleanField(
        label="Resentful toward new workers",
        blank=True
    )
    Grateful_employers = models.BooleanField(
        label="Grateful toward employers",
        blank=True
    )
    Grateful_workers = models.BooleanField(
        label="Grateful toward new workers",
        blank=True
    )
    Indifferent = models.BooleanField(
        label="Indifferent",
        blank=True
    )
    Other = models.BooleanField(
        label="Other",
        blank=True
    )
    No_emotion = models.BooleanField(
        label="I did not experience any particular emotions",
        blank=True
    )

    # For employer
    empl_effort_expectation = models.StringField(
        choices=[
            "a lot more effort than I expected.",
            "somewhat more effort than I expected.",
            "the same level of effort as I expected.",
            "Somewhat less effort than I expected.",
            "a lot less effort than I expected.",
            "I don’t know"
        ],
        label="1. How did the workers’ effort in part 2 compare to what you expected?",
        widget=widgets.RadioSelect
    )
    empl_retaining_workers = models.StringField(
        choices=[
            "Not important",
            "Slightly important",
            "Moderately important",
            "Very important",
            "Extremely important",
            "I don’t know"
        ],
        label="2. How important was retaining your existing worker(s)?",
        widget=widgets.RadioSelect
    )
    empl_hiring_confidence = models.StringField(
        choices=[
            "Not confident",
            "Slightly confident",
            "Moderately confident",
            "Very confident",
            "Extremely confident",
            "I don’t know"
        ],
        label="3. How confident were you in your ability to hire workers in each round?",
        widget=widgets.RadioSelectHorizontal
    )
    empl_strategy = models.StringField(
        choices=[
            "I prioritized cost-saving by lowering wages",
            "I maintained wages to preserve worker effort",
            "I followed other employers’ wage offers",
            "Other",
            "I did not have a clear strategy"
        ],
        label="4. Which of the following best describes your strategy when the number of workers increased in part 2?",
    )
    # For Native Workers
    nat_motivation_change = models.StringField(
        choices=[
            "It highly demotivated me",
            "It slightly demotivated me",
            "It did not impact my motivation",
            "It slightly motivated me",
            "It highly motivated me",
            "I don’t know"
        ],
        label="1. Did the increased number of workers on the market change your motivation to provide effort?",
    )

    nat_wage_perception = models.StringField(
        choices=["higher", "about the same", "lower"],
        label="2. Did you perceive that wages were different in part 2?",
        widget=widgets.RadioSelectHorizontal
    )

    # Separate fields for wage change percentage based on whether wages were perceived to be higher or lower.
    nat_wage_increase_percentage = models.StringField(
        label="2a. How much higher were the wage offers? Enter a percentage or 'NA' if you don’t know.",
        blank=True
    )

    nat_wage_decrease_percentage = models.StringField(
        label="2b. How much lower were the wage offers? Enter a percentage or 'NA' if you don’t know.",
        blank=True
    )

    nat_wage_fairness = models.StringField(
        choices=[
            "I found the new wage very unfair",
            "I found the new wage somewhat unfair",
            "Neutral",
            "I found the new wage somewhat fair",
            "I found the new wage very fair",
            "I don’t know"
        ],
        label="3. How did you personally feel about these new wage offers?",
    )

    nat_wage_adjustment_reasonable = models.StringField(
        choices=[
            "Yes, definitely reasonable",
            "Yes, somewhat reasonable",
            "Neither reasonable nor unreasonable",
            "No, somewhat unreasonable",
            "No, definitely unreasonable",
            "I don’t know"
        ],
        label="4. Do you think it is reasonable for employers to adjust wages when market conditions change?",
    )

    nat_unemployment_risk = models.StringField(
        choices=[
            "Yes, definitely",
            "Yes, somewhat",
            "Unsure",
            "No, unlikely",
            "I don’t know"
        ],
        label="5. Did you consider that there was a higher risk of becoming unemployed in part 2?",
        widget=widgets.RadioSelectHorizontal
    )

    # Wage perception for migrants
    mig_wage_perception = models.StringField(
        choices=["higher", "about the same", "lower"],
        label="1. Did you perceive that wages were different in the new market?",
        widget=widgets.RadioSelectHorizontal
    )

    # Separate fields for wage change percentage based on whether wages were perceived to be higher or lower.
    mig_wage_increase_percentage = models.StringField(
        label="1a. How much higher were the wage offers? Enter a percentage or 'NA' if you don’t know.",
        blank=True
    )

    mig_wage_decrease_percentage = models.StringField(
        label="1b. How much lower were the wage offers? Enter a percentage or 'NA' if you don’t know.",
        blank=True
    )

    # Other migrant-specific questions
    mig_motivation_change = models.StringField(
        choices=[
            "Yes, I was significantly more motivated",
            "Yes, I was somewhat more motivated",
            "My motivation remained the same as before",
            "No, I was less motivated",
            "No, I was significantly less motivated"
        ],
        label="2. Did the wages in the market motivate you to provide more effort?",
    )

    mig_motivation_evolution = models.StringField(
        choices=[
            "I became more motivated over time",
            "My motivation remained the same",
            "I became less motivated over time",
            "I don’t know"
        ],
        label="3. As the rounds progressed, how did your motivation evolve?",
    )

    mig_pressure_to_work_harder = models.StringField(
        choices=[
            "Yes, absolutely",
            "Yes, a bit",
            "No, not so much",
            "No, not at all",
            "I don’t know"
        ],
        label="4. Did you feel any pressure to provide more effort than incumbent workers?",
        widget=widgets.RadioSelectHorizontal
    )

# FUNCTIONS
def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        p.is_employer = p.participant.vars.get('is_employer', False)
        p.large_market = p.participant.vars.get('large_market', False)
        p.small_market = p.participant.vars.get('small_market', False)
        p.migrant = p.participant.vars.get('migrant', False)

# PAGES
class Employer(Page):
    form_model = 'player'
    form_fields = ['empl_effort_expectation', 'empl_retaining_workers', 'empl_hiring_confidence', 'empl_strategy']

    @staticmethod
    def is_displayed(player: Player):
        return player.is_employer and player.large_market


class Native(Page):
    form_model = 'player'
    form_fields = ['nat_motivation_change', 'nat_wage_perception', 'nat_wage_increase_percentage', 'nat_wage_decrease_percentage', 'nat_wage_fairness', 'nat_wage_adjustment_reasonable', 'nat_unemployment_risk', 'Threatened', 'Confident', 'Resentful_employers', 'Resentful_workers', 'Grateful_employers', 'Grateful_workers', 'Indifferent', 'Other', 'No_emotion']

    @staticmethod
    def is_displayed(player: Player):
        return not player.is_employer and not player.migrant



class Migrant(Page):
    form_model = 'player'
    form_fields = ['mig_wage_perception', 'mig_wage_increase_percentage', 'mig_wage_decrease_percentage', 'mig_motivation_change', 'mig_motivation_evolution', 'mig_pressure_to_work_harder']


    @staticmethod
    def is_displayed(player: Player):
        return not player.is_employer and player.migrant


page_sequence = [Employer,
                 Native,
                 Migrant]
