import requests
from datetime import datetime
from typing import List
from trains.models import Train


def parse_search(data) -> List[Train]:
    results = data["results"]
    trains = []
    for result in results:
        from_name = result["from"]["name"]
        from_code = result["from"]["number"]
        to_name = result["to"]["name"]
        to_code = result["to"]["number"]
        depart_dt = result["from"]["dep_dt"]
        train = result["train"]
        duration_format = result["duration_fmt"]
        depart = datetime.fromtimestamp(depart_dt / 1000)
        trains.append(
            Train(
                from_name=from_name,
                to_name=to_name,
                from_code=from_code,
                to_code=to_code,
                depart_dt=depart_dt,
                train=train,
                duration_format=duration_format,
                depart=depart
            )
        );
    return trains

def format_search_result(train: Train):
    return f'{train.depart} [{train.train}] {train.from_name} -> {train.to_name} ({train.duration_format}) [{train.depart_dt}]'


def search(from_station: int, to_station: int, date: datetime, limit: int = 5) -> List[Train]:
    date_str = date.strftime('%d%m%Y')
    base_url = "https://www.nightjet.com/nj-booking-ocp/connection/find"
    search_url = f"{base_url}/{from_station}/{to_station}/{date_str}/00:00?skip=0&limit={limit}&lang=de&backward=false"
    response = requests.get(search_url)

    if response.status_code == 200:
        return parse_search(response.json())
    else:
        raise Exception(f"POST request failed with status code: {response.status_code}")


