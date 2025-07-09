#!/usr/bin/env python3

import argparse
import requests
import sys
from utility import get_coordinates

def get_forecast_weather(lat, lon, days=7):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
        "forecast_days": days,
        "timezone": "auto"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        sys.exit("Error fetching forecast data.")
    return response.json()["daily"]

def format_forecast(data, city_display):
    forecast_output = f"\n7-Day Forecast for {city_display}:\n"
    for date, t_max, t_min, rain in zip(data["time"], data["temperature_2m_max"], data["temperature_2m_min"], data["precipitation_sum"]):
        forecast_output += (
            f"{date}: High {t_max}°F, Low {t_min}°F, Rain: {rain} in\n"
        )
    return forecast_output

def main():
    # --- Production argument parsing (keep for later) ---
    # parser = argparse.ArgumentParser(description="Get a 7-day weather forecast.")
    # parser.add_argument("--location", required=True, help="City name (e.g. 'Seattle')")
    # args = parser.parse_args()
    # location = args.location

    # --- Hardcoded testing mode ---
    location = "Orem"
    
    lat, lon, city_display = get_coordinates(location)
    forecast_data = get_forecast_weather(lat, lon)
    forecast_summary = format_forecast(forecast_data, city_display)
    print(forecast_summary)

if __name__ == "__main__":
    main()