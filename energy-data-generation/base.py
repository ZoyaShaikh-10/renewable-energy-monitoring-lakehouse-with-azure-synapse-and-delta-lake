"""
A base script which stores the information of the locations, which will be consumed further..
"""
import os
import csv
from typing import List

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
        

    def save_to_csvf(self, energy_data: List[str], location : str, output_file: str, output_fields: List[str]):
        """
        Save the energy production data to a CSV file. 
        NOTE : Using csv writer rather than pandas because the datasets are small-to-medium
        so, it is efficient to use csv writer.

        Args:
            energy_data (list): List of dictionaries containing energy production data.
            location (str) : Name of location directory
            output_file (str): Path to the CSV file where data will be saved.
            output_fields (list): List of field names (keys) to include in the CSV.
            
            
        """
        
        # Create the directory for the location if it doesn't exist
        if not os.path.exists(location):
            os.makedirs(location)
            
        ## updating outputfile location
        output_file = f"{location}/{output_file}"
            
        if not energy_data:
            print("No data to save.")
            return
        
        # Validate that all required fields are present in the data
        missing_fields = [field for field in output_fields if field not in energy_data[0]]
        if missing_fields:
            print(f"Warning: Missing fields in data for {', '.join(missing_fields)}")
            return
        
        try:
            # Open the CSV file in write mode
            with open(output_file, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=output_fields)
                
                # Write the header (column names)
                writer.writeheader()
                
                # Write all rows of data
                for row in energy_data:
                    writer.writerow(row)
            
            print(f"Data successfully saved to {output_file}")

        except Exception as e:
            print(f"Error while saving to CSV: {e}")
