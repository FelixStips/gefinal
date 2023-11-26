from os import environ

ROOMS = [
    dict(
        name='SSEL_B',
        display_name='SSEL Lab B',
        participant_label_file='_rooms/SSEL_LabB.txt',
    ),
    dict(
        name='CeDEx',
        display_name='CeDEx Lab',
        participant_label_file='_rooms/CeDEx_Lab.txt',
    ),
]

SESSION_CONFIGS = [
    dict(
         name='Main',
         display_name="Main",
         app_sequence=['intro',
                       'part1',
                       'midbreak',
                       'part2',
                       'questionnaire',
                       'questionnaire2',
                       'end'],
         use_browser_bots=False,
         num_demo_participants=9,
         final=False,                                                              # Display instructions
         market_timeout_seconds=150,                                               # Duration of market stage in seconds
         countdown_seconds=3,                                                      # Duration of countdown in seconds
         showup_fee=12.0,                                                          # Participation show-up fee
         payout_rate=0.01,                                                         # Payout rate: 1 point = X Pounds
         exchange_rate=2,                                                          # Exchange rate: 1 point = X tokens
         max_wage=100,                                                             # Maximum wage in points
         employer_outside_option=0,                                                # Outside option for employers in points
         worker_outside_option=0,                                                  # Outside option for workers in points
         MPL_high=[160, 140],                                                      # Revenue high effort for 1 or 2 workers
         MPL_low=[32, 28],                                                         # Revenue low effort for 1 or 2 workers
         effort_names=['Low', 'Normal'],                                           # Names of effort levels
         effort_costs_points=[10, 20],                                             # Effort costs for low and high effort, in points
         total_rounds=4,                                                           # Total number of market rounds
         shock_after_rounds=2,                                                     # Number of rounds before migration shock
         size_large_market=3,                                                      # Number of players in each large market (note: large and small does not mean anything)
         size_small_market=3,                                                      # Number of players in small market
         num_employers_large_market=1,                                             # Number of employers in large market
         num_employers_small_market=1,                                             # Number of employers in small market
         migration_large_shock_size=1,                                             # Number of migrants in large migration shock (note: large and small shock should be equal to workers in small market)
         migration_small_shock_size=1,                                             # Number of migrants in small migration shock
         worker_example_wage=50,                                                   # Wage in the worker example in points
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
                      'round_number',
                      'worker1_wage_points',
                      'worker1_wage_tokens',
                      'worker1_effort',
                      'worker1_effort_given',
                      'worker1_id',
                      'worker1_profit_points',
                      'worker1_profit_tokens',
                      'worker2_wage_points',
                      'worker2_wage_tokens',
                      'worker2_effort',
                      'worker2_effort_given',
                      'worker2_id',
                      'worker2_profit_points',
                      'worker2_profit_tokens',]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'Pounds'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '3687679433801'
