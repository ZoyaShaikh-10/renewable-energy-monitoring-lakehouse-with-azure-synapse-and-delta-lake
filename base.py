"""
A base script which stores the information of the locations, which will be consumed further..
"""

class WeatherLocationBase:
    def __init__(self):
        # Storing weather and location data
        self.locations_data ={
                "Boston": {
                    "weather": {
                        "temperature": -5.53,
                        "humidity": 47
                    },
                    "location": {
                        "latitude": 42.3601,
                        "longitude": -71.0589,
                        "country": "USA"
                    }
                },
                "New York": {
                    "weather": {
                        "temperature": 2.0,
                        "humidity": 60
                    },
                    "location": {
                        "latitude": 40.7128,
                        "longitude": -74.0060,
                        "country": "USA"
                    }
                },
                "San Francisco": {
                    "weather": {
                        "temperature": 15.0,
                        "humidity": 75
                    },
                    "location": {
                        "latitude": 37.7749,
                        "longitude": -122.4194,
                        "country": "USA"
                    }
                },
                "Chicago": {
                    "weather": {
                        "temperature": -3.0,
                        "humidity": 55
                    },
                    "location": {
                        "latitude": 41.8781,
                        "longitude": -87.6298,
                        "country": "USA"
                    }
                }
            }

    def get_weather_details(self, location_name):
        """
        Fetch weather details (temperature, humidity) for a given location.
        """
        location_data = self.locations_data.get(location_name)
        if location_data:
            return location_data["weather"]
        else:
            return f"Weather data for {location_name} not found."

    def get_location_details(self, location_name):
        """
        Fetch location details (latitude, longitude, country) for a given location.
        """
        location_data = self.locations_data.get(location_name)
        if location_data:
            return location_data["location"]
        else:
            return f"Location {location_name} not found."