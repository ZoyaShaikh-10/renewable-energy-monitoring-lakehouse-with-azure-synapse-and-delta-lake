"""
The script simulates (estimates) energy consumption based on weather data for multiple locations.
It calculates the energy consumption for heating or cooling needs by considering temperature, humidity, and specific formulas for each location.
The results can be used to model energy demand based on real-time weather conditions.
"""

import pandas as pd
from datetime import datetime, timedelta
from base import WeatherLocationBase 


class EnergyConsumption(WeatherLocationBase):
    def __init__(self):
        super().__init__()  # Initialize the base class

    def simulate_energy_consumption(self, location_name, time_interval=24):
        """
        Simulate energy consumption based on weather and time of day for a specific location.

        Args:
            location_name (str): Name of the location.
            time_interval (int): Number of hours to simulate. Default is 24 hours.

        Returns:
            list: A list of dictionaries containing simulated energy consumption data.
        """
        # Fetch location and weather details from the base class
        location_data = self.locations_data.get(location_name)

        if not location_data:
            return {"error": f"Location '{location_name}' not found in the base data."}

        weather_data = location_data["weather"]

        # Constants for simulation
        base_consumption_rate = 100  # Base energy consumption rate in kWh (residential)
        temperature_factor = 10  # Energy consumption increases by 10% for each degree below 0°C
        humidity_factor = 5  # Energy consumption increases by 5% for each 10% humidity above 80%

        # Initialize list to store energy consumption data
        consumption_data = [] 

        # Start simulation
        start_time = datetime.now()
        for i in range(time_interval):
            current_time = start_time + timedelta(hours=i)
            hour = current_time.hour

            # Adjust consumption based on time of day (evening peak hours)
            time_of_day_factor = 1 + (0.2 if 18 <= hour < 22 else 0)

            # Extract temperature and humidity
            temperature = weather_data["temperature"]
            humidity = weather_data["humidity"]

            # Calculate energy consumption
            consumption = base_consumption_rate * time_of_day_factor
            consumption += (temperature_factor * max(0, 0 - temperature))  # Heating demand
            consumption += (humidity_factor * max(0, humidity - 80))  # Cooling demand

            # Append the result to the consumption data list
            consumption_data.append({
                "time": current_time.isoformat(),
                "location": location_name,
                "latitude": location_data["location"]["latitude"],
                "longitude": location_data["location"]["longitude"],
                "country": location_data["location"]["country"],
                "energy_consumption_kWh": round(consumption, 2)
            })
            
   

        return consumption_data

    def simulate_for_all_locations(self, time_interval=24):
        """
        Simulate energy consumption for all locations in the base data.

        Args:
            time_interval (int): Number of hours to simulate. Default is 24 hours.

        Returns:
            DataFrame: A Pandas DataFrame containing simulation data for all locations.
        """
        all_consumption_data = []
        for location_name in self.locations_data.keys():
            consumption_data = self.simulate_energy_consumption(location_name, time_interval)
            if isinstance(consumption_data, list):
                all_consumption_data.extend(consumption_data)

        # Convert to a DataFrame
        return pd.DataFrame(all_consumption_data)


# Example usage
if __name__ == "__main__":
    # Initialize the EnergyConsumption class
    energy_simulator = EnergyConsumption()

    # Simulate energy consumption for all locations
    time_interval = 24  # Simulate for 24 hours
    all_data_df = energy_simulator.simulate_for_all_locations(time_interval)

    # Save to a single CSV file
    output_file = "realtime-output/energy_consumption_all_locations.csv"
    all_data_df.to_csv(output_file, index=False)
    print(f"Energy consumption data for all locations saved to {output_file}")
