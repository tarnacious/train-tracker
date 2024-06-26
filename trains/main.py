from typing import List
import os
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
from trains.data import get_trains, get_train_checks, train_info
from trains.render import render_route, render_routes
import re

def slugify(s):
  s = s.lower().strip()
  s = re.sub(r'[^\w\s-]', '', s)
  s = re.sub(r'[\s_-]+', '-', s)
  s = re.sub(r'^-+|-+$', '', s)
  return s

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
    token_path = os.environ.get("TOKEN_PATH", "token.json")
    try:
        os.remove(token_path)
    except OSError:
        pass



    output_path = os.environ.get('HTML_PATH', "./out")
    database_path = os.environ.get('DATABASE_PATH', "trains.db")
    engine = create_engine(f"sqlite:///{database_path}")
    db = database.Database(engine)

    if os.environ.get("SKIP_IMPORT", "false") == "false":
        # Paris -> Berlin
        run_import(8796001, 8096003, datetime.now(), db, limit=50)

        # Berlin -> Paris
        run_import(8096003, 8796001, datetime.now(), db, limit=50)

    train_names = [
        ('NJ 40424', "Berlin -> Paris", "nj-40424.html"), 
        ('NJ 40469', "Paris -> Berlin", "nj-40469.html")
    ]

    try:
        print("Creating output directory", output_path)
        os.makedirs(output_path)
    except FileExistsError:
        print("Output path already exists")
    for name, _, _ in train_names:

        all_trains = get_trains(name, db)
        trains = []
        for train in all_trains:
            if not train.id: continue
            trains.append(get_train_checks(train, db))

        trains = sorted(trains, key=lambda train: train.train.depart_dt, reverse=True)

        train_data = train_info(trains)
        html = render_route(name, train_data)
        filename = slugify(name) + ".html"
        filepath = os.path.join(output_path, filename)
        with open(filepath, 'w') as f:
            f.write(html)
            print("Written file", filepath)

    filepath = os.path.join(output_path, "index.html")
    html = render_routes(train_names)
    with open(filepath, 'w') as f:
        f.write(html)
        print("Written file", filepath)
    print("Completed successfully")
