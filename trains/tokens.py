import json
from dataclasses import dataclass, asdict
import requests
from trains.models import Token

def parse_token(data) -> Token: 
    return Token(
            public_id = data["publicId"],
            token = data["token"]
            )

def request_token() -> Token:
   url = "https://www.nightjet.com/nj-booking-ocp/init/start"
   response = requests.post(url, json={ "lang": "de" })
   if response.status_code == 200:
       response_data = response.json()
       return parse_token(response_data)
   else:
       raise Exception(f"POST request failed with status code: {response.status_code}")

def get_token() -> Token:
    try:
        with open('token.json', 'r') as file:
            print("Found existing token")
            data = json.load(file)
            return Token(**data)
    except FileNotFoundError:
        print("No token.json found, requesting a new token")
        token = request_token()
        print(token)
        with open('token.json', 'w') as file:
            token_json = json.dumps(asdict(token))
            print("token json", token_json)
            file.write(token_json)
        return token

    

