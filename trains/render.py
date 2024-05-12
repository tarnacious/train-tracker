from typing import List
from trains.database import Availability, Check, Database, TicketPrice, Train, Ticket, TrainChecks, TrainTicketCheck
from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader("trains"),
    autoescape=select_autoescape()
)

def render_route(name: str, trains: List[Availability]) -> str:
    template = env.get_template("trains.html.jinja")
    return template.render(trains=trains, name=name)

def render_routes(trains: list[tuple[str, str, str]]) -> str:
    template = env.get_template("index.html.jinja")
    return template.render(trains=trains)
    
