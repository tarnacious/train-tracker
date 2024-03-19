import json
from trains.booking import parse_booking, best_prices, Ticket

def test_parse_booking1():
    with open('tests/data/booking-1.json', 'r') as file:
        data = json.load(file)
    tickets = parse_booking(data)
    assert tickets == [
        Ticket(ticket_type='LE', identifier='couchette4', name='Compartment for 4 passengers', price=549.6), 
        Ticket(ticket_type='LE', identifier='couchette6', name='Compartment for 6 passengers', price=469.6), 
        Ticket(ticket_type='BE', identifier='double', name='Compartment for 2 passengers (Double)', price=869.6), 
        Ticket(ticket_type='BE', identifier='T3', name='Compartment for 3 passengers (Triple)', price=699.6), 
        Ticket(ticket_type='LE', identifier='privateCouchette', name='Private compartment for up to 6 passengers in a couchette coach', price=604.9), 
        Ticket(ticket_type='SE', identifier='privateSeat', name='Private compartment in a 2nd class seated coach', price=424.9), 
        Ticket(ticket_type='LE', identifier='femaleCouchette4', name='Ladies only compartment for 4 passengers', price=549.6), 
        Ticket(ticket_type='LE', identifier='femaleCouchette6', name='Ladies only compartment for 6 passengers', price=469.6), 
        Ticket(ticket_type='SE', identifier='sideCorridorCoach_2', name='Seat 2nd class', price=269.6), 
        Ticket(ticket_type='LE', identifier='couchette4', name='Compartment for 4 passengers', price=489.6), 
        Ticket(ticket_type='LE', identifier='couchette6', name='Compartment for 6 passengers', price=419.6), 
        Ticket(ticket_type='BE', identifier='double', name='Compartment for 2 passengers (Double)', price=789.6), 
        Ticket(ticket_type='BE', identifier='T3', name='Compartment for 3 passengers (Triple)', price=629.6), 
        Ticket(ticket_type='LE', identifier='privateCouchette', name='Private compartment for up to 6 passengers in a couchette coach', price=524.9), 
        Ticket(ticket_type='SE', identifier='privateSeat', name='Private compartment in a 2nd class seated coach', price=354.9), 
        Ticket(ticket_type='LE', identifier='femaleCouchette4', name='Ladies only compartment for 4 passengers', price=489.6), 
        Ticket(ticket_type='LE', identifier='femaleCouchette6', name='Ladies only compartment for 6 passengers', price=419.6), 
        Ticket(ticket_type='SE', identifier='sideCorridorCoach_2', name='Seat 2nd class', price=229.6), 
        Ticket(ticket_type='LE', identifier='privateCouchette', name='Private compartment for up to 6 passengers in a couchette coach', price=499.9), 
        Ticket(ticket_type='SE', identifier='privateSeat', name='Private compartment in a 2nd class seated coach', price=319.9), 
        Ticket(ticket_type='SE', identifier='sideCorridorCoach_2', name='Seat 2nd class', price=159.60000000000002)
    ]

def test_parse_booking2():
    with open('tests/data/booking-2.json', 'r') as file:
        data = json.load(file)
    tickets = parse_booking(data)
    assert tickets == [
    ]

def test_parse_booking3():
    with open('tests/data/booking-3.json', 'r') as file:
        data = json.load(file)
    tickets = parse_booking(data)
    assert tickets == [
        Ticket(ticket_type='SE', identifier='privateSeat', name='Private compartment in a 2nd class seated coach', price=449.9), 
        Ticket(ticket_type='SE', identifier='sideCorridorCoach_2', name='Seat 2nd class', price=284.6), 
        Ticket(ticket_type='SE', identifier='privateSeat', name='Private compartment in a 2nd class seated coach', price=389.9), 
        Ticket(ticket_type='SE', identifier='sideCorridorCoach_2', name='Seat 2nd class', price=244.6), 
        Ticket(ticket_type='SE', identifier='privateSeat', name='Private compartment in a 2nd class seated coach', price=369.9), 
        Ticket(ticket_type='SE', identifier='sideCorridorCoach_2', name='Seat 2nd class', price=184.60000000000002)
    ]

def test_best_prices():
    tickets = [
        Ticket(ticket_type='LE', identifier='couchette4', name='Compartment for 4 passengers', price=549.6), 
        Ticket(ticket_type='LE', identifier='couchette6', name='Compartment for 6 passengers', price=469.6), 
        Ticket(ticket_type='BE', identifier='double', name='Compartment for 2 passengers (Double)', price=869.6), 
        Ticket(ticket_type='BE', identifier='T3', name='Compartment for 3 passengers (Triple)', price=699.6), 
        Ticket(ticket_type='LE', identifier='privateCouchette', name='Private compartment for up to 6 passengers in a couchette coach', price=604.9), 
        Ticket(ticket_type='SE', identifier='privateSeat', name='Private compartment in a 2nd class seated coach', price=424.9), 
        Ticket(ticket_type='LE', identifier='femaleCouchette4', name='Ladies only compartment for 4 passengers', price=549.6), 
        Ticket(ticket_type='LE', identifier='femaleCouchette6', name='Ladies only compartment for 6 passengers', price=469.6), 
        Ticket(ticket_type='SE', identifier='sideCorridorCoach_2', name='Seat 2nd class', price=269.6), 
        Ticket(ticket_type='LE', identifier='couchette4', name='Compartment for 4 passengers', price=489.6), 
        Ticket(ticket_type='LE', identifier='couchette6', name='Compartment for 6 passengers', price=419.6), 
        Ticket(ticket_type='BE', identifier='double', name='Compartment for 2 passengers (Double)', price=789.6), 
        Ticket(ticket_type='BE', identifier='T3', name='Compartment for 3 passengers (Triple)', price=629.6), 
        Ticket(ticket_type='LE', identifier='privateCouchette', name='Private compartment for up to 6 passengers in a couchette coach', price=524.9), 
        Ticket(ticket_type='SE', identifier='privateSeat', name='Private compartment in a 2nd class seated coach', price=354.9), 
        Ticket(ticket_type='LE', identifier='femaleCouchette4', name='Ladies only compartment for 4 passengers', price=489.6), 
        Ticket(ticket_type='LE', identifier='femaleCouchette6', name='Ladies only compartment for 6 passengers', price=419.6), 
        Ticket(ticket_type='SE', identifier='sideCorridorCoach_2', name='Seat 2nd class', price=229.6), 
        Ticket(ticket_type='LE', identifier='privateCouchette', name='Private compartment for up to 6 passengers in a couchette coach', price=499.9), 
        Ticket(ticket_type='SE', identifier='privateSeat', name='Private compartment in a 2nd class seated coach', price=319.9), 
        Ticket(ticket_type='SE', identifier='sideCorridorCoach_2', name='Seat 2nd class', price=159.60000000000002)
    ]

    tickets = best_prices(tickets)

    assert tickets == [
        Ticket(ticket_type='LE', identifier='couchette4', name='Compartment for 4 passengers', price=489.6), 
        Ticket(ticket_type='LE', identifier='couchette6', name='Compartment for 6 passengers', price=419.6), 
        Ticket(ticket_type='BE', identifier='double', name='Compartment for 2 passengers (Double)', price=789.6), 
        Ticket(ticket_type='BE', identifier='T3', name='Compartment for 3 passengers (Triple)', price=629.6), 
        Ticket(ticket_type='LE', identifier='privateCouchette', name='Private compartment for up to 6 passengers in a couchette coach', price=499.9), 
        Ticket(ticket_type='SE', identifier='privateSeat', name='Private compartment in a 2nd class seated coach', price=319.9), 
        Ticket(ticket_type='LE', identifier='femaleCouchette4', name='Ladies only compartment for 4 passengers', price=489.6), 
        Ticket(ticket_type='LE', identifier='femaleCouchette6', name='Ladies only compartment for 6 passengers', price=419.6), 
        Ticket(ticket_type='SE', identifier='sideCorridorCoach_2', name='Seat 2nd class', price=159.60000000000002)
    ]

    
