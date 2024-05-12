from sqlmodel import Session, select
import datetime
from collections import defaultdict
from typing import List
from trains.database import Availability, Check, Database, TicketPrice, Train, Ticket, TrainChecks, TrainTicketCheck, Availability, AvailabilityInfo
from itertools import groupby


def get_trains(train_name: str, db: Database) -> List[Train]:
    with Session(db.engine) as session:
        statement = select(Train).where(Train.train == train_name) 
        results = session.exec(statement)
        return list(results)


def get_train_checks(train: Train, db: Database) -> TrainChecks:
    with Session(db.engine) as session:
        last_check_statement = select(Check) \
            .where(Check.train_id == train.id) \
            .order_by(Check.created_at.desc()) \
            .limit(1) 
        last_checks = list(session.exec(last_check_statement))

        last_check = None
        if len(last_checks) > 0:
            last_check = last_checks[0]


        statement = select(Train, Check, Ticket) \
            .where(Train.id == Check.train_id) \
            .where(Ticket.check_id == Check.id) \
            .where(Train.id == train.id) \

        results = session.exec(statement)
        train_tickets = []
        for train, check, ticket in list(results):
            train_tickets.append(TrainTicketCheck(
                train=train,
                check=check,
                ticket=ticket
            ))
        #print(f"Found {len(train_tickets)} train ticket")
        

        ticket_identifers = set(list(map(lambda x: x.ticket.identifier, train_tickets)))

        ticket_availability: dict[str, List[TicketPrice | None]] = defaultdict(list) 
        for _, ticket_group in groupby(train_tickets, lambda x: x.check.id):
            ticket_group = list(ticket_group)
            check = ticket_group[0].check
            tickets = list(map(lambda x: x.ticket, ticket_group))
            ticket_types = {ticket.identifier: ticket for ticket in tickets}
            for identifier in ticket_identifers:
                price = ticket_types[identifier].price if identifier in ticket_types else None

                ticket_availability[identifier].append(TicketPrice(
                        date=check.created_at,
                        price=round(price, 2) if price is not None else None,
                    ))

        sorted_dict = {key: sorted(value, key=lambda a: a.date) for key, value in ticket_availability.items()}

        return TrainChecks(
            train=train,
            availability=sorted_dict,
            last_check=last_check
        )

def train_info(trains: List[TrainChecks]) -> List[Availability]:
    availabilities: List[Availability] = []
    for train in trains:
        if not train.last_check or (datetime.datetime.now() - train.last_check.created_at).days > 7:
            # do not include trains that do not have recent updates
            continue
        ticket_types = {}
        for ticket_type, ticket_prices in train.availability.items():
            availability: List[TicketPrice] = sorted(
                    filter(lambda ticket_price: ticket_price is not None, ticket_prices), 
                    key=lambda ticket_price: ticket_price.date)
            ticket_price = availability[-1] if len(availability) > 0 else None
            if ticket_price is None or ticket_price.date < datetime.datetime.now() - datetime.timedelta(days=1):
                ticket_price = TicketPrice(
                        date = datetime.datetime.now(),
                        price = None
                )

            ticket_types[ticket_type] = AvailabilityInfo(
                        prices = availability,
                        price = ticket_price,
                        last_sold =  next(filter(lambda a: a and a.price is not None, reversed(availability))),
                        first_sold = next(filter(lambda a: a and a.price is not None, availability)),
                        max_price = max(filter(lambda a: a and a.price is not None, availability), key=lambda a: a.price),
                        min_price = max(filter(lambda a: a and a.price is not None, availability), key=lambda a: -a.price),
                    )
        availabilities.append(Availability(
                train = train,
                ticket_types = ticket_types,
                last_checked = None if train.last_check is None else train.last_check.created_at    
            ))
    return availabilities
            

