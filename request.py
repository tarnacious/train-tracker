from time import sleep
from search import search, format_search_result
from datetime import datetime
from tokens import get_token
from booking import get_prices, our_train

date = datetime(2024, 4, 1)


token = get_token()
search_results = search(date)
for search_result in search_results:
    timestamp = search_result.depart_dt
    tickets = get_prices(timestamp, token)
    print("## ", format_search_result(search_result))
    for ticket in tickets:
        print(ticket)
    print("")
    sleep(1)



