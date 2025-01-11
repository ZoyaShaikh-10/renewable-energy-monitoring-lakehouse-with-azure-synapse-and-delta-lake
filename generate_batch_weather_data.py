import pandas as pd
import random
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

    def save_to_csv(self, df, file_name):
        df.to_csv(file_name, index=False)
        print(f"Data saved to {file_name}")

# Usage

generator = BatchDataGenerator(start_date="2024-12-01", end_date="2024-12-31")

# Generate and save weather data
weather_data = generator.generate_weather_data()
generator.save_to_csv(weather_data, "batch-output/weather_batch_data.csv")

# Generate and save production data
production_data = generator.generate_production_data()
generator.save_to_csv(production_data, "batch-output/production_batch_data.csv")

# Generate and save consumption data
consumption_data = generator.generate_consumption_data()
generator.save_to_csv(consumption_data, "batch-output/consumption_batch_data.csv")
