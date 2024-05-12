from typing import Optional, Sequence, List
from sqlmodel import Field, Session, SQLModel, select
from datetime import datetime
from sqlmodel import SQLModel
from trains import models
from dataclasses import asdict, dataclass 

SQLModel.__table_args__ = {'extend_existing': True}

class Train(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    from_name: str
    to_name: str
    from_code: str
    to_code: str
    depart_dt: int
    train: str
    duration_format: str
    depart: datetime
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)

    def __str__(self) -> str:
        return f"{self.id} {self.depart} {self.train} {self.from_name} -> {self.to_name}"

    @classmethod
    def from_model(cls, train: models.Train):
        return cls(**asdict(train))

    def to_model(self):
        dictret = dict(self.__dict__);
        dictret.pop('_sa_instance_state', None)
        dictret.pop('id', None)
        dictret.pop('created_at', None)
        return models.Train(**dictret)


class Check(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    train_id: int = Field(default=None, foreign_key="train.id")
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)

class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticket_type: str
    identifier: str
    name: str
    price: float
    check_id: int = Field(default=None, foreign_key="check.id")

    @classmethod
    def from_model(cls, train: models.BookingTicket, check: Check):
        return cls(**asdict(train), check_id=check.id)

@dataclass 
class TrainTicketCheck:
    train: Train
    check: Check
    ticket: Ticket

@dataclass 
class CheckTickets:
    check: Check
    tickets: List[Ticket]

@dataclass
class TicketPrice:
    date: datetime
    price: float  | None

@dataclass
class AvailabilityInfo:
    prices: List[TicketPrice | None]
    price: TicketPrice | None
    last_sold: TicketPrice | None
    first_sold: TicketPrice | None
    max_price: TicketPrice | None
    min_price: TicketPrice | None


@dataclass 
class Availability: 
    train: Train
    ticket_types: dict[str, AvailabilityInfo]
    last_checked: datetime | None

@dataclass
class TrainChecks:
    train: Train
    availability: dict[str, List[TicketPrice | None]]
    last_check: Check | None


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

    def insert_tickets(self, train_id: int, tickets: List[models.BookingTicket]):
        with Session(self.engine) as session:
            train_check = Check(train_id=train_id)
            session.add(train_check)
            session.commit()
            if len(tickets) > 0:
                for ticket in tickets:
                    session.add(Ticket.from_model(ticket, train_check))
                session.commit()
