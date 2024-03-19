from time import sleep
from trains.search import search, format_search_result
from datetime import datetime
from trains.tokens import get_token
from trains.booking import get_prices, our_train
from sqlmodel import create_engine
from trains import database


def run():
    date = datetime.now()
    engine = create_engine("sqlite:///trains.db")
    db = database.Database(engine)
    token = get_token()
    print("Searching for trains from", date)
    trains = search(date)
    print("Found trains", len(trains))
    saved_trains = []
    for train in trains:
        existing = db.find_train(train.from_name, train.to_name, train.depart_dt)
        if existing is None:
            print("Inserting new train")
            db.insert_train(train)
            saved_trains.append(train)
        else:
            saved_trains.append(existing)
    print("Add trains inserted")


   # for train in saved_trains:
   #     print(train.id)
        #db.insert_train(train)
        #timestamp = search_result.depart_dt
        #tickets = get_prices(timestamp, token)
        #for ticket in tickets:
        #    print(ticket)
        #print("")
        #sleep(1)



