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

def get_forecast_summary(city_name): #Updated to better display in V2
    if city_name.lower() == "orem":
        latitude = 40.2969
        longitude = -111.6946
    else:
        raise ValueError("Only 'Orem' is supported.")

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,weather_code",
        "temperature_unit": "fahrenheit",
        "timezone": "auto"
    }
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return []

    data = response.json()
    daily = data.get("daily", {})
    dates = daily.get("time", [])
    temps_max = daily.get("temperature_2m_max", [])
    temps_min = daily.get("temperature_2m_min", [])
    codes = daily.get("weather_code", [])

    forecast_list = []
    for i in range(len(dates)):
        forecast_list.append({
            "date": dates[i],
            "temp_high": temps_max[i],
            "temp_low": temps_min[i],
            "description": _weather_code_to_description(codes[i])
        })

    return forecast_list

def _weather_code_to_description(code):
    code_map = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle", 53: "Moderate drizzle",
        55: "Dense drizzle", 56: "Light freezing drizzle", 57: "Dense freezing drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain", 66: "Light freezing rain",
        67: "Heavy freezing rain", 71: "Slight snow fall", 73: "Moderate snow fall",
        75: "Heavy snow fall", 77: "Snow grains", 80: "Slight rain showers",
        81: "Moderate rain showers", 82: "Violent rain showers", 85: "Slight snow showers",
        86: "Heavy snow showers", 95: "Thunderstorm", 96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return code_map.get(code, "Unknown")

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