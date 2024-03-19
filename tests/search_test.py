from trains.search import parse_search
from datetime import datetime
from trains.models import Train
import json

def test_parse_search_results():
    with open('tests/data/search.json', 'r') as file:
        data = json.load(file)
    trains = parse_search(data)
    assert trains == [
        Train(from_name='Berlin Hbf (Tiefgeschoß)', to_name='Paris Est', depart_dt=1715019480000, train='NJ 40424', duration_format='14 Std 6 Min ', depart=datetime(2024, 5, 6, 20, 18)), 
        Train(from_name='Berlin Hbf (Tiefgeschoß)', to_name='Paris Est', depart_dt=1715192280000, train='NJ 40424', duration_format='14 Std 6 Min ', depart=datetime(2024, 5, 8, 20, 18)), 
        Train(from_name='Berlin Hbf (Tiefgeschoß)', to_name='Paris Est', depart_dt=1715365080000, train='NJ 40424', duration_format='14 Std 6 Min ', depart=datetime(2024, 5, 10, 20, 18))
    ]
