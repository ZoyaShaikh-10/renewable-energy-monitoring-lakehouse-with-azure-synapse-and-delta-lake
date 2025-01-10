"""
Collecting relevant weather data (e.g., temperature, wind speed, precipitation, cloud cover, etc.)
to simulate renewable energy production (e.g., for wind turbines or solar panels).
"""

import requests
import json

# API endpoint and your API key
url = "https://api.tomorrow.io/v4/weather/forecast"
api_key = "XPr2YBXzq3HoK5loGUvsOAiKuSFHJzsh"  # Replace with your actual API key

# List of locations (latitude, longitude)
locations = [
    {"name": "Boston", "lat": 42.3478, "lon": -71.0466},
    {"name": "New York", "lat": 40.7128, "lon": -74.0060},
    {"name": "San Francisco", "lat": 37.7749, "lon": -122.4194},
    {"name": "Chicago", "lat": 41.8781, "lon": -87.6298}
]

# Fetch weather data for each location
weather_data = {}
for location in locations:
    params = {
        "location": f"{location['lat']},{location['lon']}",
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        weather_data[location["name"]] = response.json()
    else:
        print(f"Failed to fetch data for {location['name']}: {response.status_code}")

# Save data to a file
# with open("weather_forecast_multiple_locations.json", "w") as file:
#     json.dump(weather_data, file, indent=4)

print("Weather data fetched for multiple locations!")
