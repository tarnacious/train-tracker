from dataclasses import dataclass
from datetime import datetime

@dataclass
class BookingTicket:
    ticket_type: str
    identifier: str
    name: str
    price: float

@dataclass
class Train:
    from_name: str
    to_name: str
    depart_dt: int
    train: str
    duration_format: str
    depart: datetime

