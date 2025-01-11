"""
This script simulates (estimates) energy production data for solar, wind, and hydro power by utilizing weather forecast data (e.g., solar radiation, wind speed, precipitation).
It calculates estimated energy outputs based on predefined models and assumptions, generating synthetic datasets for multiple locations and time intervals. 
This data is useful for forecasting, analysis, and planning energy production scenarios
"""
import csv
import json
from astral.sun import sun
from astral import LocationInfo
from datetime import datetime, timedelta
from base import WeatherLocationBase
from fetch_weather_data import WeatherFetcher


class EnergyProduction(WeatherLocationBase):
    def __init__(self):
        super().__init__()  # Initialize Base Class

    def calculate_daylight_hours(self, location_name, latitude, longitude, date):
        """
        Calculate daylight hours for a given location and date.
        """
        location = LocationInfo(location_name, "USA", "UTC", latitude, longitude)
        sun_times = sun(location.observer, date=date)
        sunrise = sun_times["sunrise"]
        sunset = sun_times["sunset"]
        daylight_hours = (sunset - sunrise).seconds / 3600  # Convert to hours
        return daylight_hours

    def simulate_solar_power(self, cloud_cover, uv_index, daylight_hours):
        """
        Simulate solar power generation based on weather conditions.
        """
        max_output = 1000  # kWh, assume max output
        efficiency = (1 - cloud_cover / 100) * (uv_index / 10)
        return max_output * efficiency * daylight_hours / 24

    def simulate_wind_power(self, wind_speed):
        """
        Simulate wind power generation based on wind speed.
        """
        max_output = 500  # kWh
        optimal_speed = 12  # m/s
        if wind_speed > 20:
            return max_output * 0.2  # Turbines shut down partially
        return max_output * (wind_speed / optimal_speed)

    def simulate_hydro_power(self, rain_accumulation):
        """
        Simulate hydro power generation based on rain accumulation.
        """
        max_output = 800  # kWh
        return max_output * (rain_accumulation / 50)

    def simulate_energy_production(self, weather_data, time_interval=24):
        """
        Simulate energy production for all locations in the base data.

        Args:
            weather_data (dict): Weather data including forecasts for each location.
            time_interval (int): Number of hours to simulate. Default is 24 hours.

        Returns:
            dict: A dictionary containing simulated energy production data.
        """
        energy_data = []

        for location_name, location_info in self.locations_data.items():
            coords = location_info["location"]
            latitude = coords["latitude"]
            longitude = coords["longitude"]

            forecasts = weather_data.get(location_name, {}).get("timelines", {}).get("minutely", [])

            for forecast in forecasts[:time_interval]:
                time = forecast["time"]
                values = forecast["values"]

                # Parse date for daylight calculation
                date = datetime.fromisoformat(time[:-1]).date()
                daylight_hours = self.calculate_daylight_hours(location_name, latitude, longitude, date)

                # Simulate energy production
                solar_power = self.simulate_solar_power(values["cloudCover"], values["uvIndex"], daylight_hours)
                wind_power = self.simulate_wind_power(values["windSpeed"])
                hydro_power = self.simulate_hydro_power(values.get("rainIntensity", 0))

                # Store the data for CSV output
                energy_data.append({
                    "time": time,
                    "location": location_name,
                    "solar_power": round(solar_power, 2),
                    "wind_power": round(wind_power, 2),
                    "hydro_power": round(hydro_power, 2)
                })
            


        return energy_data


    def save_to_csv(self, energy_data, output_file):
        """
        Save the energy production data to a CSV file.

        Args:
            energy_data (list): List of dictionaries containing energy production data.
            output_file (str): Path to the CSV file where data will be saved.
        """
        print("ENERGY", energy_data)
        print(output_file)
        
        fieldnames = ["time", "location", "solar_power", "wind_power", "hydro_power"]
        # Directly pass the data to save_to_csvf
        self.save_to_csvf(energy_data, output_file, fieldnames)
       

if __name__ == "__main__":
    # Initialize the EnergyProduction class
    energy_production = EnergyProduction()

    # Load weather data from a JSON file or API Data
    # fetch_weatherinfo = WeatherFetcher()
    # weather_data = fetch_weatherinfo.fetch_weather_data()
    # print(weather_data)
    
    with open("weather_forecast_multiple_locations.json", "r") as file:
        weather_data = json.load(file)


    # Simulate energy production
    time_interval = 24  # Simulate for 24 hours
    energy_production_data = energy_production.simulate_energy_production(weather_data, time_interval)
    
    print("Saving Output..")
    # Save simulated energy data to a CSV file
    output_file = "realtime-output/energy_production_simulation.csv"
    energy_production.save_to_csv(energy_production_data, output_file)

    print(f"Energy production simulation data saved to {output_file}")
