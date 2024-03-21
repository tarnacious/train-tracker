from collections import defaultdict
from dataclasses import asdict
from time import sleep
from typing import List
from trains.search import search, format_search_result
from datetime import datetime
from trains.tokens import get_token
from trains.booking import get_prices, our_train
from sqlmodel import create_engine, Session, select
from trains import database
from trains import models
from sqlalchemy import text
from trains.format import format_relative_time
from trains.database import Check, Train, Ticket
from itertools import groupby

def run_import(from_station: int, to_station: int, date: datetime, db, limit=50):
    date = datetime.now()
    token = get_token()
    print("Searching for trains from", date)
    trains: List[models.Train] = search(from_station, to_station, date, limit=limit)
    print("Found trains", len(trains))
    saved_trains: List[database.Train] = []
    for train in trains:
        existing = db.find_train(train.from_name, train.to_name, train.depart_dt)
        if existing is None:
            print("Inserting new train")
            saved_train = db.insert_train(train)
            saved_trains.append(saved_train)
        else:
            saved_trains.append(existing)

    for train in saved_trains:
        if train.id is None:
            print("Train could be None?")
            continue
        dictret = dict(train.__dict__);
        dictret.pop('_sa_instance_state', None)
        dictret.pop('id', None)
        dictret.pop('created_at', None)
        print(f"## {train.id} {train.train} {train.from_name} -> {train.to_name}")
        tickets = get_prices(models.Train(**dictret), token)
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
        statement = select(Train, Check, Ticket).where(Train.id == Check.train_id).where(Ticket.check_id == Check.id).where(Train.train == 'NJ 40424').order_by(Train.id)
        results = session.execute(statement)
        #allresults = list(results)
        trains = []
        for k, g in groupby(results, lambda x: x[0].id):
            group_items = list(g)
            check_list = sorted(list(map(lambda x: { "check": x[1], "ticket": x[2] }, group_items)), key=lambda x: x["check"].id)

            checks = []
            for check_key, ticket_group in groupby(check_list, lambda x: x["check"].id):
                ticket_group = list(ticket_group)
                check = ticket_group[0]["check"]
                tickets = list(map(lambda x: x["ticket"], ticket_group))
                checks.append({
                    "check": check,
                    "tickets": tickets
                    })

            trains.append({
                "train": group_items[0][0],
                "checks": checks
            })

        for train in trains:
            checks = train["checks"]

            ticket_identifiers = list(map(lambda check: list(map(lambda ticket: ticket.identifier, check["tickets"])), checks))

            ticket_identifiers = [item for sublist in ticket_identifiers for item in sublist]

            train_tickets = defaultdict(list) 
            for check in checks:
                tickets = check["tickets"]
                def key_function(item):
                    return item.identifier
                result_dict = {key_function(ticket): ticket for ticket in tickets}

                for identifier in ticket_identifiers:
                    train_tickets[identifier].append({
                        "date": check["check"].created_at,
                        "price": result_dict[identifier].price if identifier in result_dict else None
                    })

            print( "### ", train["train"])
            for key, value in train_tickets.items():
                prices = list(map(lambda x: x["price"], value))
                price = "sold out" if prices[-1] is None else "{:.2f}€".format(prices[-1]) 
                print(key, price)
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
        



