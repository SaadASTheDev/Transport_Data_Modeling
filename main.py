import requests
import folium
import pandas as pd
from sodapy import Socrata
import re
from geopy.distance import distance


import requests.exceptions
from api_passwords import APP_TOKEN, password

MAX_RETRIES = 3
retry_count = 0
client = Socrata("data.cityofnewyork.us",
                 APP_TOKEN,
                 username="saadahmadsabri03@gmail.com",
                 password=password, timeout=500)
while retry_count < MAX_RETRIES:
    try:
        results = client.get("i4gi-tjb9", limit=10)
        break  # Break the loop if the request is successful
    except requests.exceptions.ReadTimeout:
        retry_count += 1
        print(f"Request timed out. Retrying... (Attempt {retry_count}/{MAX_RETRIES})")

results_df = pd.DataFrame.from_records(results)
print(results_df)
# Initialize the map centered around NYC
map_nyc = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

# Create a color dictionary based on traffic speed ranges
color_dict = {
    'low': 'green',
    'medium': 'yellow',
    'high': 'red'
}
max_length_threshold = 5

# Plot road segments on the map with different colors based on traffic speed
for _ , row in results_df.iterrows():
    try:
        link_points = re.split(r'[, ]', row['link_points'])
        points = [(float(link_points[0]), float(link_points[1])), (float(link_points[2]), float(link_points[3]))]
        speed = float(row['speed'])

        line_length = 0.0
        for i in range(len(link_points)):
            coord1 = link_points[i],link_points[i + 1]
            coord2 = link_points[i + 2], link_points[i + 3]
            line_length += distance(coord1, coord2).miles

        if speed < 30.0:
            color = color_dict['low']
        if 30 < speed < 45.0:
            color = color_dict['medium']
        if speed > 45.0:
            color = color_dict['high']
        if line_length > max_length_threshold:
            pass
        folium.PolyLine(points, color=color, weight=10).add_to(map_nyc)

    except Exception as e:
        # Print the error message
        print(f"An error occurred: {str(e)}")

# Display the map
map_nyc.save('traffic_map.html')
