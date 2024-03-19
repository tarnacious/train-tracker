from datetime import datetime
from trains.database import Database, Train
from sqlmodel import create_engine
import pytest

@pytest.fixture
def database():
    engine = create_engine("sqlite:///:memory:", echo=True)
    database = Database(engine)
    yield database


def test_no_trains_database(database):
    trains = database.find_all_trains()
    assert len(list(trains)) == 0


def test_insert_train(database):
    train = Train(
        from_name = "1",
        to_name = "2",
        depart_dt = "10202020",
        train = "some train",
        duration_format = "14 hours",
        depart = datetime(2023,10,10)
    )

    database.insert_train(train)
    assert train.id == 1 

def test_find_train(database):
    found_train = database.find_train("1", "2", "10202020")
    assert found_train is None

    train = Train(
        from_name = "1",
        to_name = "2",
        depart_dt = "10202020",
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

    train = Train(
        from_name = "1",
        to_name = "2",
        depart_dt = "10202020",
        train = "some train",
        duration_format = "14 hours",
        depart = datetime(2023,10,10)
    )
    database.insert_train(train)

    found_trains = database.find_trains("1", "2")
    assert found_trains == [train]
