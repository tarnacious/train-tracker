import json

from dataclasses import dataclass
from collections import defaultdict
from typing import List
import requests
import json

@dataclass
class Ticket:
    ticket_type: str
    identifier: str
    name: str
    price: float


def request_booking_json(timestamp: int):
    return {
        "njFrom": 8098160,
        "njDep": timestamp,
        "njTo": 8700011,
        "maxChanges": 0,
        "filter": {
            "njTrain": "NJ 40424",
            "njDeparture": timestamp 
        },
        "objects": [
            {
                "type": "person",
                "gender": "male",
                "birthDate": "2016-03-17",
                "cards": []
            },
            {
                "type": "person",
                "gender": "male",
                "birthDate": "2016-03-17",
                "cards": []
            },
            {
                "type": "person",
                "gender": "female",
                "birthDate": "1994-03-17",
                "cards": []
            },
            {
                "type": "person",
                "gender": "male",
                "birthDate": "1994-03-17",
                "cards": []
            }
        ],
        "relations": [],
        "lang": "de"
    }

def parse_booking(data) -> List[Ticket]:
    if "result" not in data:
        print("No result in data", data)
        return []
    if not data["result"][0]:
        return []
    offers = data["result"][0]["connections"][0]["offers"]
    tickets = []

    for offer in offers:
        compartments = offer["reservation"]["reservationSegments"][0]["compartments"]
        for compartment in compartments:
            name = compartment["name"]["en"]
            accomodation_type = compartment["accommodationType"]
            identifier = compartment["externalIdentifier"]
            if "objects" in compartment:
                objects = compartment["objects"]

                total = sum(map(lambda x: x["price"], objects))
                tickets.append(Ticket(
                    ticket_type = accomodation_type,
                    identifier = identifier,
                    name = name,
                    price = total,
                    ))
            if "privateVariations" in compartment:
                variations = compartment["privateVariations"]
                prices = []
                for variation in variations:
                    allocations = variation["allocations"]
                    for allocation in allocations:
                        objects = allocation["objects"]
                        for obj in objects:
                            if (obj["price"] != 0):
                                prices.append(obj["price"])
                for price in set(prices):
                    tickets.append(Ticket(
                        ticket_type = accomodation_type,
                        identifier = identifier,
                        name = name,
                        price = price,
                        ))
                        
                #print(json.dumps(compartment, indent=2))
            #exit()

    return tickets 

def best_prices(tickets: List[Ticket]) -> List[Ticket]:
    # Group tickets by identifier
    grouped_tickets = defaultdict(list)
    for ticket in tickets:
        grouped_tickets[ticket.identifier].append(ticket)

    # Find the best price for each identifier
    best_prices = []
    for _, ticket_list in grouped_tickets.items():
        best_price_ticket = sorted(ticket_list, key=lambda x: x.price)
        best_prices.append(best_price_ticket[0])

    return best_prices

def our_train(tickets: List[Ticket]) -> Ticket | None:
    return next(filter(lambda ticket: ticket.identifier == 'privateCouchette', tickets), None)

def get_prices(timestamp, token):
    headers = {
            "x-token": token.token 
    }
    url: str = "https://www.nightjet.com/nj-booking-ocp/offer/get"
    data = request_booking_json(timestamp)
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        data = response.json()
        bookings = parse_booking(data)
        bookings = best_prices(bookings)
        return bookings
    else:
        raise Exception(f"POST request failed with status code: {response.status_code}")


if __name__ == "__main__":
    with open('3.json', 'r') as file:
        data = json.load(file)
    bookings = parse_booking(data)
    bookings = best_prices(bookings)
    for booking in bookings:
        print(booking)
    else:
        print("no bookings")
    print("our train", our_train(bookings))


