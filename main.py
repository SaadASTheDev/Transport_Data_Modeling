import requests
import folium
import pandas as pd
from sodapy import Socrata

import requests.exceptions
from api_passwords import APP_TOKEN

client = Socrata("data.cityofnewyork.us", None)

MAX_RETRIES = 3
retry_count = 0
 client = Socrata(data.cityofnewyork.us,
                 APP_TOKEN,
                 username="saadahmadsabri03@gmail.com",
                 password="AFakePassword")
while retry_count < MAX_RETRIES:
    try:
        results = client.get("i4gi-tjb9", limit=10)
        break  # Break the loop if the request is successful
    except requests.exceptions.ReadTimeout:
        retry_count += 1
        print(f"Request timed out. Retrying... (Attempt {retry_count}/{MAX_RETRIES})")

results_df = pd.DataFrame.from_records(results)
print(results_df)