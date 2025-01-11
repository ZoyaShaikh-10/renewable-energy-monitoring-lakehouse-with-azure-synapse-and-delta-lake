"""
Collecting relevant weather data (e.g., temperature, wind speed, precipitation, cloud cover, etc.)
to simulate renewable energy production (e.g., for wind turbines or solar panels).
"""

import requests
import json
from base import WeatherLocationBase


class WeatherFetcher(WeatherLocationBase):
    def __init__(self):
        super().__init__()  # Initialize Base Class
        self.api_key = "XPr2YBXzq3HoK5loGUvsOAiKuSFHJzsh"  # Replace with your actual API key
        self.url = "https://api.tomorrow.io/v4/weather/forecast"

    def fetch_weather_data(self):
        # List of locations (latitude, longitude) defined in the base class
        locations = self.locations_data.keys()

        # Initialize dictionary to store weather data for each location
        weather_data = {}

        for location in locations:
            # Get location coordinates from the base class
            latitude = self.locations_data[location]["location"]["latitude"]
            longitude = self.locations_data[location]["location"]["longitude"]

            params = {
                "location": f"{latitude},{longitude}",
                "apikey": self.api_key
            }

            # Make the API request
            response = requests.get(self.url, params=params)
            if response.status_code == 200:
                # Store the weather data in the dictionary for the location
                weather_data[location] = response.json()
            else:
                print(f"Failed to fetch data for {location}: {response.status_code}")

        return weather_data


# # Usage example
# if __name__ == "__main__":
#     # Instantiate the WeatherFetcher class
#     weather_fetcher = WeatherFetcher()

#     # Fetch weather data for all locations
#     fetched_weather_data = weather_fetcher.fetch_weather_data()
#     import json
#     with open("realtime-output/weather_forecast_multiple_locations.json", "w") as file:
#         json.dump(fetched_weather_data, file, indent=4)

#     # Output the fetched data
#     print(json.dumps(fetched_weather_data, indent=4))
