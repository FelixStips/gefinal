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
                       'part2',
                       'questionnaire',
                       'end'],
         num_demo_participants=9,
         market_timeout_seconds=30,                                               # Duration of market stage in seconds
         size_large_market=3,                                                      # Number of players in large market
         size_small_market=3,                                                      # Number of players in small market
         num_employers_large_market=1,                                             # Number of employers in large market
         num_employers_small_market=1,                                             # Number of employers in small market
         migration_small_shock_size=1,                                             # Number of migrants in small migration shock
         migration_large_shock_size=1,                                             # Number of migrants in large migration shock
         exchange_rate_large_market=0.5,                                           # Exchange rate for large market
         exchange_rate_small_market=0.1,                                           # Exchange rate for small market
         countdown_seconds=3,                                                      # Duration of countdown in seconds
         total_rounds=2,                                                           # Number of market rounds
         shock_after_rounds=1,                                                     # Number of rounds before migration shock
         rounds_part_2=1,                                                          # Number of rounds in part 2
         MPL=[10, 7, 5],                                                           # Productivity for 1, 2, 3 workers
         employer_outside_option=0,                                                # Outside option for employer
         worker_outside_option=5,                                                  # Outside option for worker
         final=False,                                                              # Displays instructions if true
         showup_fee=5.0,                                                           # Participation showup fee
         use_browser_bots=False,                                                   # Use browser bots
    )]



# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=5.00, doc=""
)

PARTICIPANT_FIELDS = ['large_market', 'large_market_1', 'large_market_2', 'small_market', 'is_employer', 'playerID', 'string_role', 'migrant', 'move_to_market_1', 'move_to_market_2', 'total_points', 'realpay', 'exrate']
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
