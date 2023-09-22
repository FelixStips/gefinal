from otree.api import *
import time
import datetime


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'part2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 15


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    marketID = models.IntegerField()
    large_market = models.BooleanField()
    large_market_1 = models.BooleanField()
    large_market_2 = models.BooleanField()
    is_finished = models.BooleanField(initial=False)
    num_job_offers = models.IntegerField(initial=0)
    job_offer_counter = models.IntegerField(initial=0)
    players_in_group = models.IntegerField()
    employers_in_group = models.IntegerField()
    num_unmatched_workers = models.IntegerField()
    num_unmatched_jobs = models.IntegerField()
    start_timestamp = models.StringField()
    average_wage_points = models.FloatField()
    average_wage_tokens = models.FloatField()
    average_effort = models.FloatField()
    average_payoff_firms_points = models.FloatField()
    average_payoff_firms_tokens = models.FloatField()
    average_payoff_workers_points = models.FloatField()
    average_payoff_workers_tokens = models.FloatField()

class Player(BasePlayer):
    num_workers_employed = models.IntegerField(initial=0, min=0,
                                               max=2)  # Counter for number of workers the firm employed
    total_wage_paid_tokens = models.FloatField(initial=0)  # Total wage paid by the firm (in tokens)
    total_wage_paid_points = models.FloatField(initial=0)  # Total wage paid by the firm (in points)
    total_effort_received = models.IntegerField(initial=0)  # Total effort received by the firm
    effort_worth = models.IntegerField(initial=0)  # Effort worth of the firm
    payoff_points = models.FloatField(initial=0)  # Payoff of the firm (in points)
    payoff_tokens = models.FloatField(initial=0)  # Payoff of the firm (in tokens)
    is_employed = models.BooleanField(initial=False)  # Boolean for whether the worker is employed
    wage_received_tokens = models.FloatField(min=0)  # Wage the worker received by the firm (in tokens)
    wage_received_points = models.FloatField(min=0)  # Wage the worker received by the firm (in points)
    effort_requested = models.IntegerField(min=0, max=1)  # Effort level the firm requested from the worker
    effort_choice = models.IntegerField(min=0, max=1)  # Effort choice of the worker
    effort_cost_points = models.FloatField()  # Effort cost equivalent to the effort level in points
    effort_cost_tokens = models.FloatField()  # Effort cost equivalent to the effort level in tokens
    matched_with_id = models.IntegerField()  # ID of the firm the worker is matched with
    employer_payoff_points = models.FloatField()  # Payoff of the employer (in points)
    employer_payoff_tokens = models.FloatField()  # Payoff of the employer (in tokens)
    worker_counter = models.IntegerField()
    worker1_id = models.IntegerField()
    worker2_id = models.IntegerField()
    worker1_wage_tokens = models.FloatField()
    worker1_profit_tokens = models.FloatField()
    worker2_wage_tokens = models.FloatField()
    worker2_profit_tokens = models.FloatField()
    worker1_wage_points = models.FloatField()
    worker1_profit_points = models.FloatField()
    worker2_wage_points = models.FloatField()
    worker2_profit_points = models.FloatField()
    worker1_effort = models.IntegerField()
    worker2_effort = models.IntegerField()
    worker1_effort_given = models.IntegerField()
    worker2_effort_given = models.IntegerField()
    done = models.BooleanField(initial=False)
    reemploy = models.IntegerField(initial=0)
    show_private = models.BooleanField(initial=False)
    wait = models.BooleanField(initial=False)  # Show wait page if true (workers)
    invalid = models.BooleanField(initial=False)  # Show job acceptance was invalid alert if true
    offer1 = models.StringField(initial="empty")
    offer2 = models.StringField(initial="empty")
    offer3 = models.StringField(initial="empty")
    offer4 = models.StringField(initial="empty")




class Offer(ExtraModel):
    group = models.Link(Group)
    marketID = models.IntegerField()
    round_number = models.IntegerField()
    job_id = models.IntegerField()
    job_number = models.IntegerField()
    timestamp_created = models.LongStringField()
    timestamp_accepted = models.LongStringField()
    timestamp_cancelled = models.LongStringField()
    status = models.StringField()
    show = models.BooleanField()
    private = models.BooleanField()
    employer_id = models.IntegerField()
    worker_id = models.IntegerField()
    wage_points = models.FloatField()
    wage_tokens = models.FloatField()
    effort = models.IntegerField()
    effort_given = models.IntegerField()



# FUNCTIONS
def creating_session(subsession: Subsession):
    players_in_all_groups = []
    for group in subsession.get_groups():
        players_in_all_groups.extend(group.get_players())

    # group matrix numbers are based on player.id_in_subsession
    players_in_large_market_1 = [p.id_in_subsession for p in players_in_all_groups if p.participant.vars['large_market_1'] is True or p.participant.vars['move_to_market_1'] is True]
    players_in_large_market_2 = [p.id_in_subsession for p in players_in_all_groups if p.participant.vars['large_market_2'] is True or p.participant.vars['move_to_market_2'] is True]
    players_in_small_market = [p.id_in_subsession for p in players_in_all_groups if p.participant.vars['small_market'] is True \
                               and p.participant.vars['move_to_market_1'] is False and p.participant.vars['move_to_market_2'] is False]

    matrix = []
    if players_in_large_market_1 is not []:
        matrix.append(players_in_large_market_1)
    if players_in_large_market_2 is not []:
        matrix.append(players_in_large_market_2)
    if players_in_small_market is not []:
        matrix.append(players_in_small_market)

    print(matrix)

    subsession.set_group_matrix(matrix)

    session = subsession.session
    for group in subsession.get_groups():
        if group.get_players()[0].participant.vars['large_market_1'] or group.get_players()[0].participant.vars['move_to_market_1'] is True:
            group.marketID = 1
            group.large_market = True
            group.large_market_1 = True
            group.large_market_2 = False
            group.players_in_group = session.config['size_large_market'] + session.config['migration_small_shock_size']
            group.employers_in_group = session.config['num_employers_large_market']
            group.num_unmatched_workers = group.players_in_group - session.config['num_employers_large_market']
            group.num_unmatched_jobs = session.config['num_employers_large_market'] * 2
        elif group.get_players()[0].participant.vars['large_market_2'] or group.get_players()[0].participant.vars['move_to_market_2'] is True:
            group.marketID = 2
            group.large_market = True
            group.large_market_1 = False
            group.large_market_2 = True
            group.players_in_group = session.config['size_large_market'] + session.config['migration_large_shock_size']
            group.employers_in_group = session.config['num_employers_large_market']
            group.num_unmatched_workers = group.players_in_group - session.config['num_employers_large_market']
            group.num_unmatched_jobs = session.config['num_employers_large_market'] * 2
        else:
            group.marketID = 3
            group.large_market = False
            group.large_market_1 = False
            group.large_market_2 = False
            group.players_in_group = session.config['size_small_market'] - session.config['migration_large_shock_size'] - session.config['migration_small_shock_size']
            group.employers_in_group = session.config['num_employers_small_market']
            group.num_unmatched_workers = group.players_in_group - session.config['num_employers_small_market']
            group.num_unmatched_jobs = session.config['num_employers_small_market'] * 2

def to_dict(offer: Offer):
    return dict(
        group_id=offer.group_id,
        marketID=offer.marketID,
        round_number=offer.round_number,
        job_id=offer.job_id,
        employer_id=offer.employer_id,
        worker_id=offer.worker_id,
        private=offer.private,
        wage_points=offer.wage_points,
        wage_tokens=offer.wage_tokens,
        effort=offer.effort,
        effort_given=offer.effort_given,
        status=offer.status,
        show=offer.show,
        job_number=offer.job_number,
        timestamp_created=offer.timestamp_created,
        timestamp_accepted=offer.timestamp_accepted,
        timestamp_cancelled=offer.timestamp_cancelled,
    )



# PAGES

class CheckReemploy(Page):
    form_model = 'player'
    form_fields = ['reemploy']

    @staticmethod
    def is_displayed(player: Player):
        if player.participant.is_employer and player.round_number > 1:
            num_workers = player.participant.vars['num_workers'][player.round_number - 2]
            if num_workers > 0:
                return True


class Reemploy(Page):
    timeout_seconds = 120
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        if player.participant.is_employer and player.reemploy == 1:
            return True


    @staticmethod
    def js_vars(player: Player):
        session = player.session
        if player.participant.currency_is_points:
            max_wage = session.config['max_wage']
        else:
            max_wage = session.config['max_wage'] * session.config['exchange_rate']

        return dict (
            my_id = player.participant.vars['playerID'],
            worker_id_1 = player.participant.vars['worker1_id'][player.round_number - 2],
            worker_id_2 = player.participant.vars['worker2_id'][player.round_number - 2],
            currency_is_points = player.participant.vars['currency_is_points'],
            max_wage = max_wage,
        )

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session

        num_workers = player.participant.vars['num_workers'][player.round_number - 2]
        if num_workers == 1:
            effort_given_1 = player.participant.vars['worker1_effort_given'][player.round_number - 2]
            effort_given_1_string = session.config['effort_names'][effort_given_1]
            effort_given_2 = 999
            effort_given_2_string = ''
            if player.participant.currency_is_points:
                max_wage = session.config['max_wage']
                wage_1 = player.participant.vars['worker1_wage_points'][player.round_number - 2]
                wage_2 = 999
            else:
                max_wage = session.config['max_wage'] * session.config['exchange_rate']
                wage_1 = player.participant.vars['worker1_wage_tokens'][player.round_number - 2]
                wage_2 = 999
        if num_workers == 2:
            effort_given_1 = player.participant.vars['worker1_effort_given'][player.round_number - 2]
            effort_given_1_string = session.config['effort_names'][effort_given_1]
            effort_given_2 = player.participant.vars['worker2_effort_given'][player.round_number - 2]
            effort_given_2_string = session.config['effort_names'][effort_given_2]
            if player.participant.currency_is_points:
                max_wage = session.config['max_wage']
                wage_1 = player.participant.vars['worker1_wage_points'][player.round_number - 2]
                wage_2 = player.participant.vars['worker2_wage_points'][player.round_number - 2]
            else:
                max_wage = session.config['max_wage'] * session.config['exchange_rate']
                wage_1 = player.participant.vars['worker1_wage_tokens'][player.round_number - 2]
                wage_2 = player.participant.vars['worker2_wage_tokens'][player.round_number - 2]

        name_low_effort = session.config['effort_names'][0]
        name_high_effort = session.config['effort_names'][1]
        currency_plural = "points" if player.participant.currency_is_points else "tokens"

        return dict(
            currency_plural=currency_plural,
            max_wage=int(max_wage),
            wage_1=int(wage_1),
            wage_2=int(wage_2),
            effort_given_1_string=effort_given_1_string,
            effort_given_2_string=effort_given_2_string,
            num_workers=num_workers,
            name_low_effort=name_low_effort,
            name_high_effort=name_high_effort,
        )

    @staticmethod
    def live_method(player: Player, data):
        session = player.session
        group = player.group
        if data['information_type'] == 'private_offer':
            if data['currency_is_points'] is True:
                wage_points = data['wage']
                wage_tokens = session.config['exchange_rate'] * wage_points
            else:
                wage_tokens = data['wage']
                wage_points = wage_tokens / session.config['exchange_rate']
            current_datetime = datetime.datetime.now()
            Offer.create(
                group=group,
                marketID=group.marketID,
                round_number=player.round_number,
                private=True,
                employer_id=data['employer_id'],
                worker_id=data['worker_id'],
                wage_points=wage_points,
                wage_tokens=wage_tokens,
                effort=data['effort'],
                status='open',
                show=True,
                effort_given=None,
                job_id=int(str(group.marketID) + str(player.round_number) + str(group.prvt_job_offer_counter) + str(0)),
                job_number=data['job_number'],
                timestamp_created=current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            )
        string_effort = session.config['effort_names'][data['effort']]
        players = group.get_players()
        group.prvt_job_offer_counter += 1

        for p in players:
            if p.participant.playerID == data['employer_id']:
                id = p.id_in_group

        return {id:
            {'information_type': 'received',
            'wage_points': wage_points,
            'wage_tokens': wage_tokens,
            'effort': data['effort'],
            'string_effort': string_effort,
            'job_number': data['job_number']}
        }



class WaitToStart(WaitPage):
    template_name = '_templates/includes/My_WaitPage.html'
    body_text = "Waiting for other players in your group to arrive."


class Countdown(Page):
    timer_text = 'The next market phase will start in:'

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['countdown_seconds']

class MarketPage(Page):
    timer_text = 'The market phase will end in:'

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['market_timeout_seconds']

    @staticmethod
    def after_all_players_arrive(group: Group):
        current_datetime = datetime.datetime.now()
        group.start_timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        group = player.group
        players_in_group = group.players_in_group
        employers_in_group = group.employers_in_group

        if player.participant.vars['currency_is_points'] is True:
            max_wage = session.config['max_wage']
        else:
            max_wage = session.config['max_wage'] * session.config['exchange_rate']

        name_low_effort = session.config['effort_names'][0]
        name_high_effort = session.config['effort_names'][1]

        return dict(max_wage=max_wage,
                    players_in_group=players_in_group,
                    employers_in_group=employers_in_group,
                    num_workers=players_in_group - employers_in_group,
                    round_number=player.round_number,
                    playerID=player.participant.vars['playerID'],
                    string_role=player.participant.vars['string_role'],
                    name_low_effort=name_low_effort,
                    name_high_effort=name_high_effort,)

    @staticmethod
    def js_vars(player: Player):
        session = player.session
        if player.participant.vars['currency_is_points'] is True:
            max_wage = session.config['max_wage']
        else:
            max_wage = session.config['max_wage'] * session.config['exchange_rate']
        name_low_effort = session.config['effort_names'][0]
        name_high_effort = session.config['effort_names'][1]
        return dict(max_wage=max_wage,
                    my_id=player.participant.vars['playerID'],
                    is_employer=player.participant.vars['is_employer'],
                    string_role=player.participant.vars['string_role'],
                    currency_is_points=player.participant.vars['currency_is_points'],
                    name_low_effort=name_low_effort,
                    name_high_effort=name_high_effort,)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.group.is_finished = True

    @staticmethod
    def live_method(player: Player, data):
        group = player.group
        session = player.session
        player.invalid = False
        current_datetime = datetime.datetime.now()


        if data['information_type'] == 'done':
            """
            'Done' means the employer does not want to send more offers.
             - We need to cancel all his open offers and change his trading scheme to wait mode.
             - If all employers are done we finish the round.
            """

            # Update offers -> Note that here we don't need to loop over players since signal came from employer
            offers = Offer.filter(group=group)
            for o in offers:
                if (o.status == 'open' or o.status == None) and o.employer_id == player.participant.playerID:
                    o.status = 'cancelled'
                    o.show = False
                    o.timestamp_cancelled = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

            # Update player info
            for p in group.get_players():
                if p.participant.playerID == data['employer_id']:
                    p.done = True
                    p.offer1 = 'cancelled' if p.offer1 != 'accepted' else p.offer1
                    p.offer2 = 'cancelled' if p.offer2 != 'accepted' else p.offer2
                    p.offer3 = 'cancelled' if p.offer3 != 'accepted' else p.offer3
                    p.offer4 = 'cancelled' if p.offer4 != 'accepted' else p.offer4

            # Update group
            group.num_unmatched_jobs -= data['jobs_open']
            print('Unmatched jobs: ', group.num_unmatched_jobs)
            if group.num_unmatched_workers == 0 or group.num_unmatched_jobs == 0:
                group.is_finished = True

        elif data['information_type'] == 'offer':
            """ 
            'Offer' means that the employer sent a public offer (private have been done already). We need to
             - Create a new offer in the database
             - Change the employer's trading scheme
             - Update group information
             """

            # Prepare information
            if data['currency_is_points'] is True:
                wage_points = data['wage']
                wage_tokens = session.config['exchange_rate'] * wage_points
            else:
                wage_tokens = data['wage']
                wage_points = wage_tokens / session.config['exchange_rate']

            # Create a new offer: Public offers have 3 digit ID!
            Offer.create(
                group=group,
                marketID=group.marketID,
                round_number=player.round_number,
                job_id=int(str(group.marketID) + str(player.round_number) + str(group.job_offer_counter)),
                employer_id=player.participant.playerID,
                worker_id=None,
                private=False,
                wage_points=wage_points,
                wage_tokens=wage_tokens,
                effort=data['effort'],
                effort_given=None,
                status='open',
                show=True,
                job_number=data["job_number"],
                timestamp_created=current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            )

            # Update player information (even here I don't need the loop, even the if I wouldn't need in theory..)
            if player.participant.playerID == data['employer_id']:
                player.offer1 = 'open' if data['job_number'] == 1 and player.offer1 != 'accepted' else player.offer1
                player.offer2 = 'open' if data['job_number'] == 2 and player.offer2 != 'accepted' else player.offer2
                player.offer3 = 'open' if data['job_number'] == 3 and player.offer3 != 'accepted' else player.offer3
                player.offer4 = 'open' if data['job_number'] == 4 and player.offer4 != 'accepted' else player.offer4

            # Update group information
            group.job_offer_counter += 1
            group.num_job_offers += 1

        elif data['information_type'] == 'accept':
            """
            'Accept' means that a worker accepted an offer. This can be a private or public offer! We need to:
            - Update the offer
            - Update worker and employer includes
            - Copy information to worker and employer
            - Update group information
            """

            # Prepare information
            if data['currency_is_points'] is True:
                wage_points = data['wage']
                wage_tokens = session.config['exchange_rate'] * wage_points
            else:
                wage_tokens = data['wage']
                wage_points = wage_tokens / session.config['exchange_rate']

            # Update the offer
            current_offer = Offer.filter(group=group, job_id=data['job_id'])
            if current_offer[0].status == 'open':
                current_offer[0].wage_points = wage_points if current_offer[0].wage_points is None else current_offer[0].wage_points
                current_offer[0].wage_tokens = wage_tokens if current_offer[0].wage_tokens is None else current_offer[0].wage_tokens
                current_offer[0].status = 'accepted'
                current_offer[0].show = True
                current_offer[0].worker_id = player.participant.playerID
                current_offer[0].timestamp_accepted = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            else:
                print('offer already accepted or cancelled')
                player.invalid = True

            # Update players (this depends on whether the offer is private or not). Here I need the loop!
            for p in group.get_players():
                if p.participant.playerID == data['employer_id']:
                    p.num_workers_employed += 1
                    p.total_wage_paid_tokens += wage_tokens
                    p.total_wage_paid_points += wage_points
                    p.matched_with_id = data['worker_id']
                    p.offer1 = 'accepted' if data['job_number'] == 1 else p.offer1
                    p.offer2 = 'accepted' if data['job_number'] == 2 else p.offer2
                    p.offer3 = 'accepted' if data['job_number'] == 3 else p.offer3
                    p.offer4 = 'accepted' if data['job_number'] == 4 else p.offer4
                elif p.participant.playerID == data['worker_id']:
                    p.is_employed = True
                    p.wait = True
                    p.show_private = False
                    p.wage_received_points = wage_points
                    p.wage_received_tokens = wage_tokens
                    p.effort_requested = data['effort']
                    p.matched_with_id = data['employer_id']

            # Update the group
            group.num_job_offers -= 1
            group.num_unmatched_workers -= 1
            group.num_unmatched_jobs -= 1
            if group.num_unmatched_workers == 0 or group.num_unmatched_jobs == 0:
                group.is_finished = True


        elif data['information_type'] == 'cancel':
            """
            'Cancel' means that the employer cancelled an offer. We need to:
            - Update the offer
            - Update employer view
            """

            # Update the offer
            current_offer = Offer.filter(group=group, job_id=data['job_id'])
            for o in current_offer:
                o.status = 'cancelled'
                o.show = False
                o.timestamp_cancelled = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

            # Update player information
            if player.participant.playerID == data['employer_id']:
                player.offer1 = 'cancelled' if data['job_number'] == 1 and player.offer1 != 'accepted' else player.offer1
                player.offer2 = 'cancelled' if data['job_number'] == 2 and player.offer2 != 'accepted' else player.offer2
                player.offer3 = 'cancelled' if data['job_number'] == 3 and player.offer3 != 'accepted' else player.offer3
                player.offer4 = 'cancelled' if data['job_number'] == 4 and player.offer4 != 'accepted' else player.offer4

            # Update group information
            group.num_job_offers -= 1

        elif data['information_type'] == 'load':
            pass


        else:
            print('unknown message type: ', data['information_type'])

        """
        Now we need to prepare the information to send back to the server. We need to:
         - Make sure offers from employers with two accepted offers are not shown
         - Make sure private offers are only shown to the worker they are intended for
         - Copy list of private and public offers
         - Calculate market information
        """

        # Check whether employer has two accepted offers and remove other offers
        for p in group.get_players():
            if p.participant.is_employer is True and p.num_workers_employed == 2:
                for o in Offer.filter(group=group, employer_id=p.participant.playerID):
                    if o.status == 'open':
                        o.status = 'cancelled'
                        o.show = False

        # Whether to show the private offer
        for p in group.get_players():
            for o in Offer.filter(group=group, private=True):
                if o.worker_id == p.participant.playerID:
                    p.show_private = True if (o.status == 'open' and p.is_employed is False) else False
                if o.employer_id == p.participant.playerID:
                    if o.job_number == 3:
                        p.offer3 = o.status
                    elif o.job_number == 4:
                        p.offer4 = o.status
                    else:
                        print('Wrong job number')

        # Prepare offers list
        offers_to_show = sorted(Offer.filter(group=group, show=True), key=lambda o: o.job_id, reverse=True)
        offers_list = [to_dict(o) for o in offers_to_show]


        # Calculate market information
        public_offers = sorted(Offer.filter(group=group, show=True, private=False), key=lambda o: o.job_id, reverse=True)
        public_offers_list = [to_dict(o) for o in public_offers]

        market_information = dict(workers_left=group.num_unmatched_workers,
                                  open_offers=sum(i['status'] == 'open' for i in public_offers_list),
                                  average_wage_tokens=sum(i['wage_tokens'] for i in public_offers_list) / len(
                                      public_offers_list) if len(public_offers_list) > 0 else 0,
                                  average_wage_points=sum(i['wage_points'] for i in public_offers_list) / len(
                                      public_offers_list) if len(public_offers_list) > 0 else 0,
                                  average_effort=sum(i['effort'] for i in public_offers_list) / len(public_offers_list) if len(
                                      public_offers_list) > 0 else 0,
                                  )


        # Prepare information for page display
        page_information = dict(is_finished=group.is_finished,)

        # Return data
        data_to_return = {
            p.id_in_group: dict(
                page_information=page_information,
                worker_information=dict(wait=p.wait,
                                        invalid=p.invalid,
                                        show_private=p.show_private, ),
                employer_information=dict(done=p.done,
                                        num_workers_employed=p.num_workers_employed,
                                        offer1=p.offer1,
                                        offer2=p.offer2,
                                        offer3=p.offer3,
                                        offer4=p.offer4,),
                market_information=market_information,
                offers=offers_list,
            )
            for p in group.get_players()
        }

        player.invalid = False

        return data_to_return


class WorkPage(Page):
    form_model = 'player'
    form_fields = ['effort_choice']

    @staticmethod
    def is_displayed(player: Player):
        return player.is_employed

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        name_high_effort = session.config['effort_names'][1]
        name_low_effort = session.config['effort_names'][0]
        if player.field_maybe_none('effort_requested') == 1:
            effort_requested = name_high_effort
        elif player.field_maybe_none('effort_requested') == 0:
            effort_requested = name_low_effort
        else:
            print('error: effort_requested not 0 or 1')
            effort_requested = "error"
        return dict(
            is_employer=player.participant.vars['is_employer'],
            string_role=player.participant.vars['string_role'],
            wage_received_points=player.wage_received_points,
            wage_received_tokens=player.wage_received_tokens,
            effort_requested=effort_requested,
            effort_cost_points_0=session.config['effort_costs_points'][0],
            effort_cost_points_1=session.config['effort_costs_points'][1],
            effort_cost_tokens_0=session.config['effort_costs_points'][0] * session.config['exchange_rate'],
            effort_cost_tokens_1=session.config['effort_costs_points'][1] * session.config['exchange_rate'],
            name_low_effort=name_low_effort,
            name_high_effort=name_high_effort,
        )



class ResultsWaitPage(WaitPage):
    body_text = "Waiting for workers to finish the effort stage."

    @staticmethod
    def after_all_players_arrive(group: Group):
        players = group.get_players()
        offers = Offer.filter(group=group)

        group.average_wage_points = sum([p.wage_received_points for p in players if p.is_employed]) / sum([p.is_employed for p in players]) if sum([p.is_employed for p in players]) > 0 else 0
        group.average_wage_tokens = sum([p.wage_received_tokens for p in players if p.is_employed]) / sum([p.is_employed for p in players]) if sum([p.is_employed for p in players]) > 0 else 0
        group.average_effort = sum([p.effort_choice for p in players if p.is_employed]) / sum([p.is_employed for p in players]) if sum([p.is_employed for p in players]) > 0 else 0

        for p in players:                                                                                               # first update the offers
            session = p.session
            for o in offers:
                if p.participant.playerID == o.worker_id and o.status == 'accepted':
                    o.effort_given = p.effort_choice
        for p in players:                                                                                               # then update the players
            p.participant.vars['round_number'] = p.participant.vars['round_number'] + 1
            if p.participant.is_employer is True:
                p.worker_counter = 0
                for o in offers:
                    if p.participant.playerID == o.employer_id and o.status == 'accepted':
                        p.worker_counter += 1
                        p.total_effort_received += o.effort_given
                        #p.total_wage_paid_points += o.wage_points                                                      # I was adding the wage twice, once before in the live_method
                        #p.total_wage_paid_tokens += o.wage_tokens
                        if p.worker_counter == 1:
                            p.worker1_wage_points = o.wage_points
                            p.worker1_wage_tokens = o.wage_tokens
                            p.worker1_effort_given = o.effort_given
                            p.worker1_effort = o.effort
                            p.worker1_id = o.worker_id
                            p.worker1_profit_points = p.worker1_wage_points - session.config['effort_costs_points'][p.worker1_effort_given]
                            print('Worker 1 got wage', p.worker1_wage_points, 'points and provided', p.worker1_effort_given, 'effort, for a cost of',  session.config['effort_costs_points'][p.worker1_effort], 'which gives profit of', p.worker1_profit_points)
                            p.worker1_profit_tokens = p.worker1_wage_tokens - session.config['effort_costs_points'][p.worker1_effort_given] * session.config['exchange_rate']
                        elif p.worker_counter == 2:
                            p.worker2_wage_points = o.wage_points
                            p.worker2_wage_tokens = o.wage_tokens
                            p.worker2_effort = o.effort
                            p.worker2_effort_given = o.effort_given
                            p.worker2_id = o.worker_id
                            p.worker2_profit_points = p.worker2_wage_points - session.config['effort_costs_points'][p.worker2_effort_given]
                            print('Worker 2 got wage', p.worker2_wage_points, 'points and provided', p.worker2_effort_given, 'effort, for a cost of',  session.config['effort_costs_points'][p.worker2_effort], 'which gives profit of', p.worker2_profit_points)
                            p.worker2_profit_tokens = p.worker2_wage_tokens - session.config['effort_costs_points'][p.worker2_effort_given] * session.config['exchange_rate']
                    else:
                        pass
                if p.num_workers_employed == 0:
                    p.payoff_points = 0
                    p.payoff_tokens = 0
                    p.effort_worth = 0
                    p.participant.vars['total_points'].append(p.payoff_points)
                    p.participant.vars['total_tokens'].append(p.payoff_tokens)
                    p.participant.vars['round_for_points'].append(p.participant.vars['currency_is_points'])
                elif p.num_workers_employed == 1:
                    if p.total_effort_received == 0:
                        if p.participant.vars['currency_is_points'] is True:
                            p.effort_worth = session.config['MPL_low'][0]
                        else:
                            p.effort_worth = session.config['MPL_low'][0] * session.config['exchange_rate']
                    elif p.total_effort_received == 1:
                        if p.participant.vars['currency_is_points'] is True:
                            p.effort_worth = session.config['MPL_high'][0]
                        else:
                            p.effort_worth = session.config['MPL_high'][0] * session.config['exchange_rate']
                    else:
                        print('error: effort_received not 0 or 1')
                elif p.num_workers_employed == 2:
                    if p.total_effort_received == 0:                                                                    # if effort_received is 0, then the worker gave low effort
                        if p.participant.vars['currency_is_points'] is True:
                            p.effort_worth = 2 * session.config['MPL_low'][1]
                        else:
                            p.effort_worth = 2 * session.config['MPL_low'][1] * session.config['exchange_rate']
                    elif p.total_effort_received == 1:                                                                  # if effort_received is 1, then one worker gave high effort
                        if p.participant.vars['currency_is_points'] is True:
                            p.effort_worth = session.config['MPL_high'][1] + session.config['MPL_low'][1]
                        else:
                            p.effort_worth = (session.config['MPL_high'][1] + session.config['MPL_low'][1]) * session.config['exchange_rate']
                    elif p.total_effort_received == 2:                                                                  # if effort_received is 2, then both workers gave high effort
                        if p.participant.vars['currency_is_points'] is True:
                            p.effort_worth = 2 * session.config['MPL_high'][1]
                        else:
                            p.effort_worth = 2 * session.config['MPL_high'][1] * session.config['exchange_rate']
                else:
                    print('error: num_workers_employed not 0, 1 or 2')

                if p.participant.vars['currency_is_points'] is True:
                    p.payoff_points = p.effort_worth - p.total_wage_paid_points
                    p.payoff_tokens = p.payoff_points * session.config['exchange_rate']
                    p.participant.vars['total_points'].append(p.payoff_points)
                    p.participant.vars['total_tokens'].append(p.payoff_tokens)
                    p.participant.vars['round_for_points'].append(p.participant.vars['currency_is_points'])
                else:
                    p.payoff_tokens = p.effort_worth - p.total_wage_paid_tokens
                    p.payoff_points = p.payoff_tokens / session.config['exchange_rate']
                    p.participant.vars['total_points'].append(p.payoff_points)
                    p.participant.vars['total_tokens'].append(p.payoff_tokens)
                    p.participant.vars['round_for_points'].append(p.participant.vars['currency_is_points'])
            else:
                if p.is_employed:
                    p.effort_cost_points = session.config['effort_costs_points'][p.effort_choice]
                    p.effort_cost_tokens = session.config['effort_costs_points'][p.effort_choice] * session.config['exchange_rate']
                    p.payoff_tokens = p.wage_received_tokens - p.effort_cost_tokens
                    p.payoff_points = p.wage_received_points - p.effort_cost_points
                    p.participant.vars['total_points'].append(p.payoff_points)
                    p.participant.vars['total_tokens'].append(p.payoff_tokens)
                    p.participant.vars['round_for_points'].append(p.participant.vars['currency_is_points'])
                else:
                    p.payoff_tokens = 0
                    p.payoff_points = 0
                    p.participant.vars['total_points'].append(p.payoff_points)
                    p.participant.vars['total_tokens'].append(p.payoff_tokens)
                    p.participant.vars['round_for_points'].append(p.participant.vars['currency_is_points'])
        for p in players:
            print('Player', p.participant.playerID, 'has had point payoffs of', p.participant.vars['total_points'][p.round_number-1], 'and token payoffs of', p.participant.vars['total_tokens'][p.round_number-1], 'and played for points:', p.participant.vars['round_for_points'][p.round_number-1])

        group.average_payoff_firms_points = sum([p.payoff_points for p in players if p.participant.is_employer is True]) / sum([p.participant.is_employer is True for p in players]) if sum([p.participant.is_employer is True for p in players]) > 0 else 0
        group.average_payoff_firms_tokens = sum([p.payoff_tokens for p in players if p.participant.is_employer is True]) / sum([p.participant.is_employer is True for p in players]) if sum([p.participant.is_employer is True for p in players]) > 0 else 0
        group.average_payoff_workers_points = sum([p.payoff_points for p in players if p.participant.is_employer is False]) / sum([p.participant.is_employer is False for p in players]) if sum([p.participant.is_employer is False for p in players]) > 0 else 0
        group.average_payoff_workers_tokens = sum([p.payoff_tokens for p in players if p.participant.is_employer is False]) / sum([p.participant.is_employer is False for p in players]) if sum([p.participant.is_employer is False for p in players]) > 0 else 0



class Results(Page):
    form_model = 'player'
    timeout_seconds = 60

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        session = player.session
        rounds_part_2 = session.config['total_rounds'] - session.config['shock_after_rounds']
        if player.round_number >= rounds_part_2:
            return "questionnaire"

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        session = player.session
        players = group.get_players()

        if player.participant.is_employer is False:
            others = player.get_others_in_group()
            try:
                player.employer_payoff_points = [p.payoff_points for p in others if
                                                 p.participant.playerID == player.field_maybe_none('matched_with_id')][
                    0]
                player.employer_payoff_tokens = [p.payoff_tokens for p in others if
                                                 p.participant.playerID == player.field_maybe_none('matched_with_id')][
                    0]
            except (KeyError, IndexError) as e:
                player.employer_payoff_points = None
                player.employer_payoff_tokens = None

        name_high_effort = session.config['effort_names'][1]
        name_low_effort = session.config['effort_names'][0]

        total_low_effort = player.num_workers_employed - player.total_effort_received if player.total_effort_received is not None else None
        worker1_effort = name_high_effort if player.field_maybe_none('worker1_effort') == 1 else (
            name_low_effort if player.field_maybe_none('worker1_effort') == 0 else "")
        worker1_effort_given = name_high_effort if player.field_maybe_none('worker1_effort_given') == 1 else (
            name_low_effort if player.field_maybe_none('worker1_effort_given') == 0 else "")
        worker2_effort = name_high_effort if player.field_maybe_none('worker2_effort') == 1 else (
            name_low_effort if player.field_maybe_none('worker2_effort') == 0 else "")
        worker2_effort_given = name_high_effort if player.field_maybe_none('worker2_effort_given') == 1 else (
            name_low_effort if player.field_maybe_none('worker2_effort_given') == 0 else "")
        average_effort = int(group.field_maybe_none('average_effort') * 100) if group.field_maybe_none(
            'average_effort') is not None else None
        effort_string = name_high_effort if player.field_maybe_none('effort_choice') == 1 else (
            name_low_effort if player.field_maybe_none('effort_choice') == 0 else "")
        round_number = player.participant.round_number
        rounds_left = session.config['total_rounds'] - round_number
        part = 2 if round_number > session.config['shock_after_rounds'] else 1
        average_wage_points = round(group.average_wage_points, 1) if group.average_wage_points is not None else None
        average_wage_tokens = round(group.average_wage_tokens, 1) if group.average_wage_tokens is not None else None
        average_profit_points = round(group.average_payoff_firms_points,
                                      1) if group.average_payoff_firms_points is not None else None
        average_profit_tokens = round(group.average_payoff_firms_tokens,
                                      1) if group.average_payoff_firms_tokens is not None else None
        average_income_points = round(group.average_payoff_workers_points,
                                      1) if group.average_payoff_workers_points is not None else None
        average_income_tokens = round(group.average_payoff_workers_tokens,
                                      1) if group.average_payoff_workers_tokens is not None else None

        return dict(
            name_low_effort=name_low_effort,
            name_high_effort=name_high_effort,
            round_number=round_number,
            rounds_left=rounds_left,
            part=part,
            is_employer=player.participant.is_employer,
            is_employed=player.is_employed,
            num_workers=player.num_workers_employed,
            worker_counter=player.field_maybe_none('worker_counter'),
            wage_received_points=player.field_maybe_none('wage_received_points'),
            wage_received_tokens=player.field_maybe_none('wage_received_tokens'),
            total_wage_paid_points=player.field_maybe_none('total_wage_paid_points'),
            total_wage_paid_tokens=player.field_maybe_none('total_wage_paid_tokens'),
            total_effort_received=player.total_effort_received,
            total_low_effort=total_low_effort,
            effort_worth=player.field_maybe_none('effort_worth'),
            effort_choice=effort_string,
            employer_payoff_points=player.field_maybe_none('employer_payoff_points'),
            employer_payoff_tokens=player.field_maybe_none('employer_payoff_tokens'),
            total_payoff_points=sum(player.participant.vars['total_points']),
            total_payoff_tokens=sum(player.participant.vars['total_tokens']),
            average_wage_points=average_wage_points,
            average_wage_tokens=average_wage_tokens,
            average_profit_points=average_profit_points,
            average_profit_tokens=average_profit_tokens,
            average_income_points=average_income_points,
            average_income_tokens=average_income_tokens,
            average_effort=average_effort,
            num_unmatched_workers=group.field_maybe_none('num_unmatched_workers'),
            worker1_wage_points=player.field_maybe_none('worker1_wage_points'),
            worker1_wage_tokens=player.field_maybe_none('worker1_wage_tokens'),
            worker1_payoff_points=player.field_maybe_none('worker1_profit_points'),
            worker1_payoff_tokens=player.field_maybe_none('worker1_profit_tokens'),
            worker1_effort=worker1_effort,
            worker1_effort_given=worker1_effort_given,
            worker1_id=player.field_maybe_none('worker1_id'),
            worker2_wage_points=player.field_maybe_none('worker2_wage_points'),
            worker2_wage_tokens=player.field_maybe_none('worker2_wage_tokens'),
            worker2_payoff_points=player.field_maybe_none('worker2_profit_points'),
            worker2_payoff_tokens=player.field_maybe_none('worker2_profit_tokens'),
            worker2_effort=worker2_effort,
            worker2_effort_given=worker2_effort_given,
            worker2_id=player.field_maybe_none('worker2_id'),
        )


page_sequence = [CheckReemploy,
                 Reemploy,
                 WaitToStart,
                 Countdown,
                 MarketPage,
                 WorkPage,
                 ResultsWaitPage,
                 Results,]



def custom_export(players):
    # top row
    yield ['session_code', 'group.id_in_subsession', 'round', 'job_id', 'employer_id', 'worker_id', 'private',
           'wage_points', 'wage_tokens', 'effort', 'effort_given', 'status', 'timestamp_created', 'timestamp_accepted',
           'timestamp_cancelled']

    # data rows
    offers = Offer.filter()
    for offer in offers:
        yield [offer.group.session.code, offer.group.id_in_subsession, offer.round_number, offer.job_id,
               offer.employer_id, offer.worker_id, offer.private, offer.wage_points, offer.wage_tokens,
               offer.effort, offer.effort_given, offer.status, offer.timestamp_created, offer.timestamp_accepted,
               offer.timestamp_cancelled]
