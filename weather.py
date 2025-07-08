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
        "current_weather": "true", # <-- as string, not boolea
        #"hourly": "temperature_2m,is_day,precipitation,wind_speed_10m,wind_direction_10m,weathercode,uv_index,time",
        "temperature_unit": "fahrenheit",
        "timezone": "auto"
    }
    #---For troublshooting---
    #print("Requesting:", weather_url)
    #print("Params:", params)

    response = requests.get(weather_url, params=params)
    if response.status_code != 200:
        sys.exit("Error: Could not fetch weather data.")
    
    return response.json()["current_weather"]

def format_weather(city, current):
    temp = current["temperature"]
    wind_speed = current["windspeed"]
    wind_dir = current["winddirection"]
    uv = current.get("uv_index", "N/A")  # fallback if not in current_weather
    rain = current.get("precipitation", 0)
    local_time = current.get("time", "unknown time")

    rain_desc = "light rain" if rain > 0 else "clear skies"
    suggestion = "Carry an umbrella just in case." if rain > 0 else "No umbrella needed."

    wind_dir_str = degrees_to_cardinal(wind_dir)

    return (
        f"Today in {city} at {local_time}: {temp}°F, {rain_desc}, "
        f"winds {wind_speed} mph {wind_dir_str}. UV index: {uv}. {suggestion}"
    )

def degrees_to_cardinal(degrees):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    idx = int((degrees + 22.5) // 45) % 8
    return directions[idx]

def main():
    # --- Production argument parsing (keep for later) ---
    # parser = argparse.ArgumentParser(description="Check the current weather for a city.")
    # parser.add_argument("--location", required=True, help="City name (e.g. 'Chicago')")
    # args = parser.parse_args()
    # location = args.location
    # lat, lon, city_display = get_coordinates(location)
    
    # --- Hardcoded testing mode ---
    location = "Orem, UT"
    lat, lon = 40.2969, -111.6946  # Orem, UT
    city_display = "Orem, UT"
    current_weather = get_weather(lat, lon)
    summary = format_weather(city_display, current_weather)
    print(summary)

if __name__ == "__main__":
    main()