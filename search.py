import json
import requests
from datetime import datetime
from dataclasses import dataclass
from typing import List
from database import Train


def parse_search(data) -> List[Train]:
    results = data["results"]
    trains = []
    for result in results:
        from_name = result["from"]["name"]
        to_name = result["to"]["name"]
        depart_dt = result["from"]["dep_dt"]
        train = result["train"]
        duration_format = result["duration_fmt"]
        depart = datetime.fromtimestamp(depart_dt / 1000)
        trains.append(
            Train(
                from_name=from_name,
                to_name=to_name,
                depart_dt=depart_dt,
                train=train,
                duration_format=duration_format,
                depart=depart
            )
        );
    return trains

def format_search_result(train: Train):
    return f'{train.depart} [{train.train}] {train.from_name} -> {train.to_name} ({train.duration_format}) [{train.depart_dt}]'


def search(date: datetime) -> List[Train]:
    date_str = date.strftime('%d%m%Y')
    search_url = f"https://www.nightjet.com/nj-booking-ocp/connection/find/8096003/8796001/{date_str}/00:00?skip=0&limit=50&lang=de&backward=false"
    response = requests.get(search_url)

    if response.status_code == 200:
        return parse_search(response.json())
    else:
        raise Exception(f"POST request failed with status code: {response.status_code}")


if __name__ == "__main__":
    with open('search_results.json', 'r') as file:
        data = json.load(file)
    trains = parse_search(data)
    for train in trains:
        print(format_search_result(train))


