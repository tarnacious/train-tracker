from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


class Train(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    from_name: str
    to_name: str
    depart_dt: str
    train: str
    duration_format: str
    depart: datetime

#hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
#hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
#hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)


engine = create_engine("sqlite:///trains.db")

def upsert_train(self, train: Train) -> Train:
    with Session(self.engine) as session:
        statement = select(Train).where("from_name" == train.from_name).where("to_name" == train.to_name).where("depart_dt" == train.depart_dt)
        results = session.exec(statement)
        existing = results.first()
        if existing is None:
            session.add(train)
            session.commit()
            return train
        else:
            return existing
        

#with Session(engine) as session:
#    statement = select(Hero).where(Hero.name == "Spider-Boy")
#    hero = session.exec(statement).first()
#    print(hero)
