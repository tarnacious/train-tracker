from typing import Optional, Sequence
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime
from sqlmodel import SQLModel
from trains import models
from dataclasses import asdict 

SQLModel.__table_args__ = {'extend_existing': True}

class Train(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    from_name: str
    to_name: str
    depart_dt: int
    train: str
    duration_format: str
    depart: datetime
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)

    @classmethod
    def from_model(cls, train: models.Train):
        return cls(**asdict(train))

class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticket_type: str
    identifier: str
    name: str
    price: float
    train_id: Optional[int] = Field(default=None, foreign_key="train.id")
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)

class Database:
    def __init__(self, engine):
        self.engine = engine
        SQLModel.metadata.create_all(engine)

    def find_train(self, from_name: str, to_name: str, timestamp: int) -> Optional[Train]:
        with Session(self.engine) as session:
            statement = select(Train).where(Train.from_name == from_name).where(Train.to_name == to_name).where(Train.depart_dt == timestamp)
            results = session.exec(statement)
            return results.first()

    def insert_train(self, train: models.Train) -> Train:
        with Session(self.engine) as session:
            db_train = Train.from_model(train)
            session.add(db_train)
            session.commit()
            session.refresh(db_train)
            session.close()
            return db_train

    def find_all_trains(self) -> Sequence[Train]:
        with Session(self.engine) as session:
            statement = select(Train)
            results = session.exec(statement)
            return results.all()

    def find_trains(self, from_name: str, to_name: str) -> Sequence[Train]:
        with Session(self.engine) as session:
            statement = select(Train).where(Train.from_name == from_name).where(Train.to_name == to_name)
            print(statement)
            results = session.exec(statement)
            return results.all()
