from trains.tokens import parse_token 
from trains.models import Token
import json

def test_parse_search_results():
    with open('tests/data/session.json', 'r') as file:
        data = json.load(file)
    token = parse_token(data)
    assert token == Token(public_id='f5e91d1812964263b7a2e75b8c916dd6', token='eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTEzNjEzMjcsInB1YmxpY0lkIjoiZjVlOTFkMTgxMjk2NDI2M2I3YTJlNzViOGM5MTZkZDYifQ.pRKfrVajPhgOsRHVXvxfIqKAz6I4G8r8AzEKeDCBhPY') 

