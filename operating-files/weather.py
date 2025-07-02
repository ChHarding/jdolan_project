#!/usr/bin/env python3

import argparse
import requests
import sys
from utility import get_coordinates


def get_weather(latitude, longitude):
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "hourly": "temperature_2m,is_day,precipitation,wind_speed_10m,wind_direction_10m,weathercode,uv_index,time",
        "temperature_unit": "fahrenheit",
        "timezone": "auto"
    }
    response = requests.get(weather_url, params=params)
    if response.status_code != 200:
        sys.exit("Error: Could not fetch weather data.")
    return response.json()["current_weather"]  #made a change here based on your suggestion
    print(response.json() ["hourly"])
    return response.json()["hourly"] #also implemented this per your suggestion



def format_weather(city, current):
    temp = current["temperature_2m"]
    wind_speed = current["wind_speed_10m"]
    wind_dir = current["wind_direction_10m"]
    uv = current["uv_index"]
    rain = current["precipitation"]

    # Simplified interpretation
    if rain > 0:
        rain_desc = "light rain"
        suggestion = "Carry an umbrella just in case."
    else:
        rain_desc = "clear skies"
        suggestion = "No umbrella needed."

    wind_dir_str = degrees_to_cardinal(wind_dir)

    return (
        f"Today in {city}: {temp}°F, {rain_desc}, winds {wind_speed} mph {wind_dir_str}. "
        f"UV index: {uv}. {suggestion}"
    )

def degrees_to_cardinal(degrees):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    idx = int((degrees + 22.5) // 45) % 8
    return directions[idx]

def main():
    parser = argparse.ArgumentParser(description="Check the current weather for a city.")
    parser.add_argument("--location", required=True, help="City name (e.g. 'Chicago')")
    args = parser.parse_args()

    lat, lon, city_display = get_coordinates(args.location)
    current_weather = get_weather(lat, lon)
    summary = format_weather(city_display, current_weather)
    print(summary)

def format_weather(city, current):
    temp = current["temperature_2m"]
    wind_speed = current["wind_speed_10m"]
    wind_dir = current["wind_direction_10m"]
    uv = current["uv_index"]
    rain = current["precipitation"]
    local_time = current["time"]

    if rain > 0:
        rain_desc = "light rain"
        suggestion = "Carry an umbrella just in case."
    else:
        rain_desc = "clear skies"
        suggestion = "No umbrella needed."

    wind_dir_str = degrees_to_cardinal(wind_dir)

    return (
        f"Today in {city} at {local_time}: {temp}°F, {rain_desc}, winds {wind_speed} mph {wind_dir_str}. "
        f"UV index: {uv}. {suggestion}"
    )

if __name__ == "__main__":
    main()