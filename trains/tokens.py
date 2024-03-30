import json
import os
from dataclasses import asdict
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
    token_path = os.environ.get("TOKEN_PATH", "token.json")
    try:
        with open(token_path, 'r') as file:
            print("Found existing token")
            data = json.load(file)
            return Token(**data)
    except FileNotFoundError:
        print("No token found, requesting a new token")
        token = request_token()
        print(token)
        with open(token_path, 'w') as file:
            token_json = json.dumps(asdict(token))
            file.write(token_json)
        return token

    

