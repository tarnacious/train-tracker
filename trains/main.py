from collections import defaultdict
from typing import List
from trains.search import search
from datetime import datetime
from trains.tokens import get_token
from trains.booking import get_prices
from sqlmodel import create_engine, Session, select
from trains import database
from trains import models
from sqlalchemy import text
from trains.format import format_relative_time
from trains.database import Check, CheckTickets, TicketPrice, Train, Ticket, TrainChecks, TrainTicketCheck
from itertools import groupby

def save_trains(trains: List[models.Train], db) -> List[database.Train]:
    saved_trains: List[database.Train] = []
    for train in trains:
        existing = db.find_train(train.from_name, train.to_name, train.depart_dt)
        if existing is None:
            print("Inserting new train")
            saved_train = db.insert_train(train)
            saved_trains.append(saved_train)
        else:
            saved_trains.append(existing)
    return saved_trains

def run_import(from_station: int, to_station: int, date: datetime, db, limit=50):
    date = datetime.now()
    token = get_token()
    print("Searching for trains from", date)
    trains: List[models.Train] = search(from_station, to_station, date, limit=limit)
    print("Found trains", len(trains))
    saved_trains = save_trains(trains, db)

    for train in saved_trains:
        print(f"## {train}")
        if train.id is None:
            print("Train could be None?")
            continue
        tickets = get_prices(train.to_model(), token)
        for ticket in tickets:
            print(ticket)
        print(f"")
        db.insert_tickets(train.id, tickets)


def run():
    engine = create_engine("sqlite:///trains.db")
    db = database.Database(engine)

    # Paris -> Berlin
    #run_import(8796001, 8096003, datetime.now(), db, limit=30)

    # Berlin -> Paris
    #run_import(8096003, 8796001, datetime.now(), db, limit=30)
    

    #trains = db.find_all_trains()
    #print(trains)

    with Session(db.engine) as session:
        statement = select(Train, Check, Ticket) \
            .where(Train.id == Check.train_id) \
            .where(Ticket.check_id == Check.id) \
            .where(Train.train == 'NJ 40424') \
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
                    ticket_availability[identifier].append(TicketPrice(
                            date=check.created_at,
                            price=ticket_types[identifier].price if identifier in ticket_types else None
                        ))
            trains.append(TrainChecks(
                train=check_list[0].train,
                availability=ticket_availability
            ))
            
        print(f"Found {len(trains)} trains")

        for train in trains:
            print( "### ", train.train)
            for k, tickets in train.availability.items():
                price = tickets[-1].price
                price_format = "sold out" if price is None else "{:.2f}€".format(price) 
                print(k, price_format)
            print("")
            

    return
    with Session(db.engine) as session:
        statement = """
            select 
                train.id as train_id, 
                train.depart as departure, 
                ticket.price as price, 
                ticket.identifier as ticket_identifier,
                ticket.ticket_type as ticket_type,
                "check".created_at
            from train 
            join "check" on "check".train_id = train.id
            join "ticket" on "ticket".check_id = "check".id
            WHERE ("check".train_id, "check".created_at) IN (
                SELECT train_id, MAX(created_at)
                FROM "check"
                GROUP BY train_id
            )
            order by train.id



        """
        results = session.execute(text(statement))
        count = 0
        for result in results:
            [train_id, departure, price, identifier, ticket_type, fetched_at] = result
            fetched_at = datetime.strptime(fetched_at, "%Y-%m-%d %H:%M:%S.%f")
            departure = datetime.strptime(departure, "%Y-%m-%d %H:%M:%S.%f")
            formatted_departure = departure.strftime("%Y-%m-%d")
            formatted_price = "{:.2f}€".format(price) 
            print(train_id, formatted_departure, identifier, formatted_price, format_relative_time(fetched_at))
            count = count + 1

        print(count)
        



