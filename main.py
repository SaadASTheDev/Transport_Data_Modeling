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
                 password=password, timeout=50000)
while retry_count < MAX_RETRIES:
    try:
        results = client.get("i4gi-tjb9", limit=10000)
        break  # Break the loop if the request is successful
    except requests.exceptions.ReadTimeout:
        retry_count += 1
        print(f"Request timed out. Retrying... (Attempt {retry_count}/{MAX_RETRIES})")

results_df = pd.DataFrame.from_records(results)
print(results_df)


def apply_custom_colors(m):
    # Set the primary color for the map
    m.background_color = '#4b4b4b'  # Primary color

    # Set the secondary color for roads and labels
    folium.TileLayer('OpenStreetMap', control=False).add_to(m)  # Use OpenStreetMap as the base map
    folium.TileLayer('cartodbpositron', control=False).add_to(m)  # Add another base map for contrast
    m.options['tileLayerOptions'] = {'opacity': 0.2, 'attribution': 'Custom attribution'}

    # Set the third-rate color for water bodies
    folium.TileLayer('Stamen Watercolor', control=False).add_to(m)  # Use Stamen Watercolor as the water bodies layer


# Initialize the map centered around NYC
map_nyc = folium.Map(location=[40.7128, -74.0060], zoom_start=12, tiles=None, control_scale=True)
# Define the default road style
map_nyc.background_color = '#4b4b4b'

apply_custom_colors(map_nyc)
# Create a color dictionary based on traffic speed ranges
color_dict = {
    'low': 'green',
    'medium': 'yellow',
    'high': '#6f112b'
}
max_length_threshold = 40

# Plot road segments on the map with different colors based on traffic speed
for _, row in results_df.iterrows():
    try:
        link_points = re.split(r"[, ]", row['link_points'])
        points = [(float(link_points[0]), float(link_points[1])), (float(link_points[2]), float(link_points[3]))]
        coord1 = (float(link_points[0]), float(link_points[1]))
        coord2 = (float(link_points[2]), float(link_points[3]))
        speed = float(row['speed'])

        line_length = 0.0

        line_length += distance(coord1, coord2).miles

        if speed < 30.0:
            color = color_dict['low']
        if 30 < speed < 45.0:
            color = color_dict['medium']
        if speed > 45.0:
            color = color_dict['high']
        if line_length > max_length_threshold:
            continue
        folium.PolyLine(points, color=color, weight=5, opacity=0.7).add_to(map_nyc)

    except Exception as e:
        # Print the error message
        print(f"An error occurred: {str(e)}")

# Display the map
map_nyc.save('traffic_map.html')
