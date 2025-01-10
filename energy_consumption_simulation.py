"""
The script simulates (estimates) energy consumption based on weather data for multiple locations.
It calculates the energy consumption for heating or cooling needs by considering temperature, humidity, and specific formulas for each location.
The results can be used to model energy demand based on real-time weather conditions.
"""


import random
import pandas as pd
import json
from datetime import datetime, timedelta

# Simulating energy consumption based on weather and time of day
def simulate_energy_consumption(location, weather_data, time_interval):
    # Constants for simulation (could be adjusted based on real data or models)
    base_consumption_rate = 100  # Base energy consumption rate in kWh (for residential buildings)
    temperature_factor = 10  # Energy consumption increases by 10% for each degree below 0°C
    humidity_factor = 5  # Energy consumption increases by 5% for each 10% humidity above 80%
    
    # Initialize list to store energy consumption data
    consumption_data = []

    # Start simulation for the given time interval
    start_time = datetime.now()
    for i in range(time_interval):
        current_time = start_time + timedelta(hours=i)
        hour = current_time.hour

        # Adjust consumption based on time of day (higher in the evening)
        time_of_day_factor = 1 + (0.2 if 18 <= hour < 22 else 0)  # Evening peak consumption

        # Adjust consumption based on temperature and humidity
        temperature = weather_data["temperature"]
        humidity = weather_data["humidity"]

        # Calculate consumption based on weather and time
        consumption = base_consumption_rate * time_of_day_factor
        consumption += (temperature_factor * max(0, 0 - temperature))  # Heating demand if temperature is low
        consumption += (humidity_factor * max(0, humidity - 80))  # Cooling demand if humidity is high
        
        # Add the simulation data for this time point
        consumption_data.append({
            "time": current_time.isoformat(),
            "location": location,
            "energy_consumption_kWh": round(consumption, 2)
        })
    
    return consumption_data

# Example usage for multiple locations
locations = ["Boston", "New York", "San Francisco", "Chicago"]

weather_data = {
    "Boston": {"temperature": -5.53, "humidity": 47},
    "New York": {"temperature": 2.0, "humidity": 60},  # Sample temperature and humidity
    "San Francisco": {"temperature": 15.0, "humidity": 75},  # Sample temperature and humidity
    "Chicago": {"temperature": -3.0, "humidity": 55}  # Sample temperature and humidity
}

time_interval = 24  # Simulate for 24 hours

# Simulate energy consumption for all locations
all_consumption_data = []
for location in locations:
    consumption_data = simulate_energy_consumption(location, weather_data[location], time_interval)
    all_consumption_data.extend(consumption_data)

# Convert to JSON
json_data = json.dumps(all_consumption_data, indent=4)

# # Output to a file
# with open("energy_consumption_simulation.json", "w") as file:
#     file.write(json_data)

# Optional: Print the JSON output
print(json_data)
