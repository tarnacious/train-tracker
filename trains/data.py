from sqlmodel import Session, select
import datetime
from collections import defaultdict
from typing import List
from trains.database import Availability, Check, Database, TicketPrice, Train, Ticket, TrainChecks, TrainTicketCheck, Availability, AvailabilityInfo
from itertools import groupby

def get_trains(train_name: str, db: Database) -> List[TrainChecks]:
    with Session(db.engine) as session:
        statement = select(Train, Check, Ticket) \
            .where(Train.id == Check.train_id) \
            .where(Ticket.check_id == Check.id) \
            .where(Train.train == train_name) \
            .order_by(Train.id)

        results = session.exec(statement)
        train_tickets = []
        for train, check, ticket in list(results):
            train_tickets.append(TrainTicketCheck(
                train=train,
                check=check,
                ticket=ticket
            ))
        print(f"Found {len(train_tickets)} train ticket")
        
        trains = []
        for _, g in groupby(train_tickets, lambda x: x.train.id):
            check_list = sorted(g, key=lambda x: x.check.id)

            ticket_identifers = set(list(map(lambda x: x.ticket.identifier, check_list)))

            ticket_availability: dict[str, List[TicketPrice | None]] = defaultdict(list) 
            for _, ticket_group in groupby(check_list, lambda x: x.check.id):
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


            trains.append(TrainChecks(
                train=check_list[0].train,
                availability=sorted_dict
            ))
        return sorted(trains, key=lambda train: train.train.depart, reverse=True)

def train_info(trains: List[TrainChecks]) -> List[Availability]:
    availabilities: List[Availability] = []
    for train in trains:
        ticket_types = {}
        for ticket_type, availability_ in train.availability.items():
            availability: List[TicketPrice | None] = availability_ 
            ticket_price = availability[-1] if len(availability) > 0 else None
            if ticket_price is None or ticket_price.date < datetime.datetime.now() - datetime.timedelta(days=1):
                ticket_price = TicketPrice(
                        date = datetime.datetime.now(),
                        price = None
                )

            #if price.date < datetime.datetime.now() - datetime.timedelta(days=1):
            #    price = 1

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
                ticket_types = ticket_types
            
            ))
    return availabilities
            

