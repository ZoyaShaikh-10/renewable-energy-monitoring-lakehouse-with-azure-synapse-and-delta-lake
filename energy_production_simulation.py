"""
This script simulates (estimates) energy production data for solar, wind, and hydro power by utilizing weather forecast data (e.g., solar radiation, wind speed, precipitation).
It calculates estimated energy outputs based on predefined models and assumptions, generating synthetic datasets for multiple locations and time intervals. 
This data is useful for forecasting, analysis, and planning energy production scenarios
"""

from astral import LocationInfo
from astral.sun import sun
import json
from datetime import datetime, timedelta

# Function to calculate daylight hours
def calculate_daylight_hours(location_name, latitude, longitude, date):
    location = LocationInfo(location_name, "USA", "UTC", latitude, longitude)
    sun_times = sun(location.observer, date=date)
    sunrise = sun_times["sunrise"]
    sunset = sun_times["sunset"]
    daylight_hours = (sunset - sunrise).seconds / 3600  # Convert to hours
    return daylight_hours

# Load weather data
with open("weather_forecast_multiple_locations.json", "r") as file:
    weather_data = json.load(file)

# Define location coordinates
locations = {
    "Boston": {"latitude": 42.3478, "longitude": -71.0466},
    "New York": {"latitude": 40.7128, "longitude": -74.0060},
    "San Francisco": {"latitude": 37.7749, "longitude": -122.4194},
    "Chicago": {"latitude": 41.8781, "longitude": -87.6298}
}

# Parameters for energy production
def simulate_solar_power(cloud_cover, uv_index, daylight_hours):
    max_output = 1000  # kWh, assume max output
    efficiency = (1 - cloud_cover / 100) * (uv_index / 10)
    return max_output * efficiency * daylight_hours / 24

def simulate_wind_power(wind_speed):
    max_output = 500  # kWh
    optimal_speed = 12  # m/s
    if wind_speed > 20:
        return max_output * 0.2  # Turbines shut down partially
    return max_output * (wind_speed / optimal_speed)

def simulate_hydro_power(rain_accumulation):
    max_output = 800  # kWh
    return max_output * (rain_accumulation / 50)

# Simulate energy production
energy_data = {}
for location, coords in locations.items():
    energy_data[location] = []
    forecasts = weather_data.get(location, {}).get("timelines", {}).get("minutely", [])
    for forecast in forecasts:
        time = forecast["time"]
        values = forecast["values"]

        # Parse date for daylight calculation
        date = datetime.fromisoformat(time[:-1]).date()
        daylight_hours = calculate_daylight_hours(location, coords["latitude"], coords["longitude"], date)

        # Simulate energy production
        solar_power = simulate_solar_power(values["cloudCover"], values["uvIndex"], daylight_hours)
        wind_power = simulate_wind_power(values["windSpeed"])
        hydro_power = simulate_hydro_power(values.get("rainIntensity", 0))

        # Store the data
        energy_data[location].append({
            "time": time,
            "solar_power": round(solar_power, 2),
            "wind_power": round(wind_power, 2),
            "hydro_power": round(hydro_power, 2)
        })

# # Save simulated energy data
# with open("energy_production_simulation.json", "w") as file:
#     json.dump(energy_data, file, indent=4)

print(json.dumps(energy_data, indent=4))
print("Energy production simulation data generated!")
