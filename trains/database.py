from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime
from sqlmodel import SQLModel

SQLModel.__table_args__ = {'extend_existing': True}

class Train(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    from_name: str
    to_name: str
    depart_dt: str
    train: str
    duration_format: str
    depart: datetime

class Database:
    def __init__(self, engine):
        self.engine = engine
        SQLModel.metadata.create_all(engine)

    def find_train(self, from_name: str, to_name: str, timestamp: datetime):
        with Session(self.engine) as session:
            statement = select(Train).where(Train.from_name == from_name).where(Train.to_name == to_name).where(Train.depart_dt == timestamp)
            results = session.exec(statement)
            return results.first()

    def insert_train(self, train: Train):
        with Session(self.engine) as session:
            session.add(train)
            session.commit()
            session.refresh(train)
            session.close()
            return train

    def find_all_trains(self):
        with Session(self.engine) as session:
            statement = select(Train)
            results = session.exec(statement)
            return results.all()

    def find_trains(self, from_name: str, to_name: str):
        with Session(self.engine) as session:
            statement = select(Train).where(Train.from_name == from_name).where(Train.to_name == to_name)
            print(statement)
            results = session.exec(statement)
            return results.all()
