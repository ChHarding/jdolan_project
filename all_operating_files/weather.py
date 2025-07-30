#!/usr/bin/env python3

import argparse
import requests
import sys
from all_operating_files.utility import get_coordinates

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

def get_current_weather(city_name):
    # Hardcoded for Orem; in production, you'd use a geocoding API
    if city_name.lower() == "orem":
        latitude = 40.2969
        longitude = -111.6946
    else:
        raise ValueError("Only 'Orem' is supported in this example.")

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,weather_code,wind_speed_10m,relative_humidity_2m",
        "temperature_unit": "fahrenheit",  # ← THIS sets temp to °F
        "windspeed_unit": "mph",           # Optional: wind speed in mph
        "timezone": "auto"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json().get("current", {})
        return {
            "temperature": data.get("temperature_2m"),
            "description": _weather_code_to_description(data.get("weather_code")),
            "humidity": data.get("relative_humidity_2m"),
            "wind_speed": data.get("wind_speed_10m")
        }
    else:
        print(f"Error: {response.status_code}")
        return None

def _weather_code_to_description(code):
    # Mapping from Open-Meteo weather codes to descriptions
    code_map = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return code_map.get(code, "Unknown")