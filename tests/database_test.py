from datetime import datetime
from trains.database import Database
from trains.database import Check, Train, Ticket
from trains import models
from sqlmodel import create_engine
import pytest
from sqlmodel import Field, Session, SQLModel, create_engine, select

@pytest.fixture
def database():
    engine = create_engine("sqlite:///:memory:", echo=True)
    database = Database(engine)
    yield database


def test_no_trains_database(database):
    trains = database.find_all_trains()
    assert len(list(trains)) == 0


def test_insert_train(database):
    train = models.Train(
        from_name = "1",
        to_name = "2",
        from_code = "100",
        to_code = "200",
        depart_dt = 10202020,
        train = "some train",
        duration_format = "14 hours",
        depart = datetime(2023,10,10)
    )

    saved_train = database.insert_train(train)
    assert saved_train.id == 1 

def test_find_train(database):
    found_train = database.find_train("1", "2", "10202020")
    assert found_train is None

    train = models.Train(
        from_name = "1",
        to_name = "2",
        from_code = "100",
        to_code = "200",
        depart_dt = 10202020,
        train = "some train",
        duration_format = "14 hours",
        depart = datetime(2023,10,10)
    )
    database.insert_train(train)

    found_train = database.find_train("1", "2", "10202020")
    assert found_train is not None
    assert found_train.id == 1

def test_find_trains(database):
    found_trains = database.find_trains("1", "2")
    assert found_trains == []

    train = models.Train(
        from_name = "1",
        to_name = "2",
        from_code = "100",
        to_code = "200",
        depart_dt = 10202020,
        train = "some train",
        duration_format = "14 hours",
        depart = datetime(2023,10,10)
    )
    database.insert_train(train)

    found_trains = database.find_trains("1", "2")
    assert len(found_trains) == 1 

def test_insert_tickets(database):

    train = models.Train(
        from_name = "1",
        to_name = "2",
        from_code = "100",
        to_code = "200",
        depart_dt = 10202020,
        train = "some train",
        duration_format = "14 hours",
        depart = datetime(2023,10,10)
    )
    saved_train = database.insert_train(train)

    tickets = [
        models.BookingTicket(
            ticket_type = "SI",
            identifier = "Sleeper",
            name = "Sleeper for 4",
            price = 400
        ),
        models.BookingTicket(
            ticket_type = "SI",
            identifier = "Class 2",
            name = "Normal wagon",
            price = 100
        )
    ]

    database.insert_tickets(saved_train.id, tickets)

    with Session(database.engine) as session:
        statement = select(Train, Check, Ticket).where(Train.id == Check.train_id).where(Check.id == Ticket.check_id)
        results = session.exec(statement).all()
        mapped_results = list(map( lambda result: [result[0].train, result[1].train_id, result[2].name], results))
        assert mapped_results == [
                ['some train', 1, 'Sleeper for 4'], 
                ['some train', 1, 'Normal wagon']
        ]

