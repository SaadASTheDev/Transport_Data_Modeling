import requests
from api_passwords import API_KEY
# Set up TomTom API credentials
api_key = API_KEY

# API endpoint for traffic incidents in NYC
url = f'https://api.tomtom.com/traffic/services/4/incidentDetails/s3/ALL/13/-74/14/-73/json?key={api_key}'

# Send request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Extract traffic incidents from the response
    incidents = response.json()['tm']['poi']

    # Iterate over the incidents and print their coordinates
    for incident in incidents:
        location = incident['point']['coordinates']
        latitude, longitude = location['latitude'], location['longitude']
        print(f"Traffic Jam at Latitude: {latitude}, Longitude: {longitude}")
else:
    print("Error occurred while accessing TomTom API.")