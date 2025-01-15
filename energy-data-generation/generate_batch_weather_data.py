import pandas as pd
import random
import os
from datetime import datetime, timedelta

class BatchDataGenerator:
    def __init__(self, start_date, end_date):
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        self.locations = ["Boston", "New York", "San Francisco", "Chicago"]

    def generate_weather_data(self):
        data = []
        current_date = self.start_date
        while current_date <= self.end_date:
            for location in self.locations:
                data.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "location": location,
                    "temperature": round(random.uniform(-10, 35), 2),
                    "humidity": random.randint(20, 90),
                    "wind_speed": round(random.uniform(0, 20), 2)
                })
            current_date += timedelta(days=1)
        return pd.DataFrame(data)

    def generate_production_data(self):
        data = []
        current_date = self.start_date
        while current_date <= self.end_date:
            for location in self.locations:
                data.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "location": location,
                    "solar_energy": round(random.uniform(100, 1000), 2),  # kWh
                    "wind_energy": round(random.uniform(50, 500), 2),   # kWh
                    "hydro_energy": round(random.uniform(200, 2000), 2) # kWh
                })
            current_date += timedelta(days=1)
        return pd.DataFrame(data)

    def generate_consumption_data(self):
        data = []
        current_date = self.start_date
        while current_date <= self.end_date:
            for location in self.locations:
                data.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "location": location,
                    "residential_consumption": round(random.uniform(500, 2000), 2),  # kWh
                    "commercial_consumption": round(random.uniform(2000, 5000), 2), # kWh
                    "industrial_consumption": round(random.uniform(1000, 10000), 2) # kWh
                })
            current_date += timedelta(days=1)
        return pd.DataFrame(data)

    def save_location_data(self, df, location, data_type):
        """
        Filter data for a specific location and save it to a CSV file.
        """
        location_data = df[df['location'] == location]
        
        # Ensure the directory exists for saving the file
        location_dir = f"batch-output/{location}"
        if not os.path.exists(location_dir):
            os.makedirs(location_dir)
        
        # Save filtered data to a CSV file specific to the location
        location_data.to_csv(f"{location_dir}/{location}_{data_type}_batch_data.csv", index=False)
        print(f"Data for {location} saved to {location_dir}/{location}_{data_type}_batch_data.csv")

    def save_all_data(self, weather_df, production_df, consumption_df):
        """
        Save the data for all locations by calling save_location_data for each location and data type.
        """
        for location in self.locations:
            self.save_location_data(weather_df, location, "weather")
            self.save_location_data(production_df, location, "production")
            self.save_location_data(consumption_df, location, "consumption")

# Usage

generator = BatchDataGenerator(start_date="2024-12-01", end_date="2024-12-31")

# Generate data for weather, production, and consumption
weather_data = generator.generate_weather_data()
production_data = generator.generate_production_data()
consumption_data = generator.generate_consumption_data()

# Save the generated data
generator.save_all_data(weather_data, production_data, consumption_data)
