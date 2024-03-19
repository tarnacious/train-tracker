from time import sleep
from typing import List
from trains.search import search, format_search_result
from datetime import datetime
from trains.tokens import get_token
from trains.booking import get_prices, our_train
from sqlmodel import create_engine
from trains import database
from trains import models



def run():
    date = datetime.now()
    engine = create_engine("sqlite:///trains.db")
    db = database.Database(engine)
    token = get_token()
    print("Searching for trains from", date)
    trains: List[models.Train] = search(date)
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
    print("Add trains inserted")


    #jfor train in saved_trains:
    #j    print(train.id)
    #j    #db.insert_train(train)
    #j    #timestamp = search_result.depart_dt
    #j    #tickets = get_prices(timestamp, token)
    #j    #for ticket in tickets:
    #j    #    print(ticket)
    #j    #print("")
    #j    #sleep(1)



