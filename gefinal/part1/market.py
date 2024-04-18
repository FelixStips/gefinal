import datetime
from .logger import logger


def to_dict(offer):
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


def handle_done(player, data, Offer, group, current_datetime):
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
    if group.num_unmatched_workers <= 0 or group.num_unmatched_jobs <= 0:
        group.is_finished = True
    return True


def handle_offer(player, data, Offer, group, current_datetime):
    """
           'Offer' means that the employer sent a public offer (private have been done already). We need to
            - Create a new offer in the database
            - Change the employer's trading scheme
            - Update group information
            """
    session = player.session
    # Prepare information
    if data['currency_is_points'] is True:
        wage_points = data['wage']
        wage_tokens = session.config['exchange_rate'] * wage_points
    else:
        wage_tokens = data['wage']
        wage_points = wage_tokens / session.config['exchange_rate']

    # Create a new offer: Public offers have 3 digit ID!
    offer = Offer.create(
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
    logger.info(f'offer {offer}')

    # Update player information (even here I don't need the loop, even the if I wouldn't need in theory..)
    if player.participant.playerID == data['employer_id']:
        player.offer1 = 'open' if data['job_number'] == 1 and player.offer1 != 'accepted' else player.offer1
        player.offer2 = 'open' if data['job_number'] == 2 and player.offer2 != 'accepted' else player.offer2
        player.offer3 = 'open' if data['job_number'] == 3 and player.offer3 != 'accepted' else player.offer3
        player.offer4 = 'open' if data['job_number'] == 4 and player.offer4 != 'accepted' else player.offer4

    # Update group information
    group.job_offer_counter += 1
    group.num_job_offers += 1
    return True


def handle_accept(player, data, Offer, group, current_datetime):
    logger.info(f'handle_accept {data}')
    """
    'Accept' means that a worker accepted an offer. This can be a private or public offer! We need to:
    - check that the offer has not been accepted
    - Update the offer
    - Update worker and employer includes
    - Copy information to worker and employer
    - Update group information
    """
    session = player.session
    # Prepare information
    if data['currency_is_points'] is True:
        wage_points = data['wage']
        wage_tokens = session.config['exchange_rate'] * wage_points
    else:
        wage_tokens = data['wage']
        wage_points = wage_tokens / session.config['exchange_rate']

    # Check that the employer can still accept workers
    for p in group.get_players():
        if p.participant.playerID == data['employer_id']:
            if p.num_workers_employed >= 2:
                print('Employer already accepted 2 workers')
                player.invalid = True

    # Check that the offer has not been accepted and enter the loop\
    current_offer = Offer.filter(group=group, job_id=data['job_id'])
    if current_offer and current_offer[0].status == 'open' and player.invalid is False:

        print('Offer', data['job_id'], ' accepted, employer', data['employer_id'], 'worker', data['worker_id'])

        # Update offer
        current_offer[0].wage_points = wage_points if current_offer[0].wage_points is None else current_offer[
            0].wage_points
        current_offer[0].wage_tokens = wage_tokens if current_offer[0].wage_tokens is None else current_offer[
            0].wage_tokens
        current_offer[0].status = 'accepted'
        current_offer[0].show = True
        current_offer[0].worker_id = player.participant.playerID
        current_offer[0].timestamp_accepted = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

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
            else:
                pass

        # Update the group
        group.num_job_offers -= 1
        group.num_unmatched_workers -= 1
        group.num_unmatched_jobs -= 1
        if group.num_unmatched_workers == 0 or group.num_unmatched_jobs == 0:
            group.is_finished = True

    else:
        logger.info('Offer', data['job_id'], 'cannot be accepted, employer', data['employer_id'], 'worker',
                    data['worker_id'])

        for o in current_offer:
            o.show = False
        for p in group.get_players():
            if p.participant.playerID == data['worker_id']:
                p.invalid = True
    return True


def handle_cancel(player, data, Offer, group, current_datetime):
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
    return True


def handle_load(player, data, Offer, group, current_datetime):
    """So far not implemented, but we might need it in the future."""
    return True


def live_method(player, data, Offer):
    player.invalid = False
    logger.info(f'live_method {data}')
    group = player.group
    logger.info(f'group size! {len(group.get_players())}')
    current_datetime = datetime.datetime.now()

    # Function dispatch dictionary
    action_handlers = {
        'done': handle_done,
        'offer': handle_offer,
        'accept': handle_accept,
        'cancel': handle_cancel,
        'load': handle_load
    }

    if data['information_type'] in action_handlers:
        res = action_handlers[data['information_type']](player, data, Offer, group, current_datetime)
        if not res:
            raise ValueError(f"Error in handling {data['information_type']}")
    else:
        raise ValueError(f"Unknown information type: {data['information_type']}")

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
                    raise Exception('Wrong job number')

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
                              average_effort=sum(i['effort'] for i in public_offers_list) / len(
                                  public_offers_list) if len(
                                  public_offers_list) > 0 else 0,
                              )

    # Prepare information for page display
    page_information = dict(is_finished=group.is_finished, )

    # Return data
    data_to_return = {
        p.id_in_group: dict(
            page_information=page_information,
            worker_information=dict(wait=p.wait,
                                    invalid=p.invalid,
                                    show_private=p.show_private),
            employer_information=dict(done=p.done,
                                      num_workers_employed=p.num_workers_employed,
                                      offer1=p.offer1,
                                      offer2=p.offer2,
                                      offer3=p.offer3,
                                      offer4=p.offer4),
            market_information=market_information,
            offers=offers_list,
        )
        for p in group.get_players()
    }

    player.invalid = False

    return data_to_return
