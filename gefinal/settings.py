from os import environ

ROOMS = [
    dict(
        name='SSEL_B',
        display_name='SSEL Lab B',
        participant_label_file='_rooms/SSEL_LabB.txt',
    ),
]

SESSION_CONFIGS = [
    dict(
         name='Main',
         display_name="Main",
         app_sequence=['intro',
                       'part1',
                       'quiz',
                       'midbreak',
                       'part2',
                       'questionnaire',
                       'end'],
         num_demo_participants=9,
         final=False,                                                              # Display instructions
         market_timeout_seconds=180,                                               # Duration of market stage in seconds
         countdown_seconds=3,                                                      # Duration of countdown in seconds
         showup_fee=5.0,                                                           # Participation show-up fee
         payout_rate=0.1,                                                          # Payout rate: 1 point = X Euros
         exchange_rate=2,                                                          # Exchange rate: 1 point = X tokens
         employer_outside_option=0,                                                # Outside option for employer
         worker_outside_option=0,                                                  # Outside option for worker
         MPL=[10, 7],                                                              # Productivity for 1 or 2 workers
         effort_costs_points=[0, 1, 2, 4, 6, 8, 10, 12, 15, 18],                   # Effort costs for 1 - 10 choices, in points
         total_rounds=2,                                                           # Total number of market rounds
         shock_after_rounds=1,                                                     # Number of rounds before migration shock
         size_large_market=3,                                                      # Number of players in each large market (note: large and small does not mean anything)
         size_small_market=3,                                                      # Number of players in small market
         num_employers_large_market=1,                                             # Number of employers in large market
         num_employers_small_market=1,                                             # Number of employers in small market
         migration_small_shock_size=1,                                             # Number of migrants in small migration shock
         migration_large_shock_size=1,                                             # Number of migrants in large migration shock (note: large and small shock should be equal to workers in small market)
    )]


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=5.00, doc=""
)

PARTICIPANT_FIELDS = ['large_market',
                      'large_market_1',
                      'large_market_2',
                      'small_market',
                      'is_employer',
                      'playerID',
                      'string_role',
                      'migrant',
                      'move_to_market_1',
                      'move_to_market_2',
                      'total_points',
                      'total_tokens',
                      'currency_is_points',
                      'round_for_points',
                      ]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'Euro'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '3687679433801'
