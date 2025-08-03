#!/usr/bin/env python3

import requests
from all_operating_files.utility import get_coordinates  # Used to get lat/lon from a city name

# Fetch current weather for a given location
def get_current_weather(city_name, latitude, longitude):
    """
    Queries the Open-Meteo API for current weather based on coordinates.
    Returns a dictionary with temperature, weather description, wind, humidity, and time.
    """
    url = "https://api.open-meteo.com/v1/forecast"

    # Query parameters sent to the Open-Meteo API
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,weather_code,wind_speed_10m,relative_humidity_2m",
        "temperature_unit": "fahrenheit",   # Return temperature in °F
        "windspeed_unit": "mph",            # Return wind speed in mph
        "timezone": "auto"                  # Automatically detect local timezone
    }

    # Make the HTTP GET request to the API
    response = requests.get(url, params=params)

    # Handle response
    if response.status_code == 200:
        # Extract data from the JSON response
        data = response.json().get("current", {})
        return {
            "city": city_name,
            "temperature": data.get("temperature_2m"),
            "description": _weather_code_to_description(data.get("weather_code")),
            "humidity": data.get("relative_humidity_2m"),
            "wind_speed": data.get("wind_speed_10m"),
            "time": data.get("time")
        }
    else:
        # If the request failed, print an error and return None
        print(f"Error fetching weather data: {response.status_code}")
        return None

# Convert Open-Meteo's weather codes to human-readable text
def _weather_code_to_description(code):
    """
    Maps weather condition codes from Open-Meteo to readable descriptions.
    """
    code_map = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        56: "Light freezing drizzle", 57: "Dense freezing drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        66: "Light freezing rain", 67: "Heavy freezing rain",
        71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
        77: "Snow grains", 80: "Slight rain showers", 81: "Moderate rain showers",
        82: "Violent rain showers", 85: "Slight snow showers", 86: "Heavy snow showers",
        95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
    }
    return code_map.get(code, "Unknown")

# Format weather data nicely for printing or Streamlit display
def format_weather(data):
    """
    Formats the current weather data into a user-friendly string.
    Suitable for display in CLI or Streamlit.
    """
    city = data["city"]
    temp = data["temperature"]
    desc = data["description"]
    wind = data["wind_speed"]
    humidity = data["humidity"]
    local_time = data["time"]

    return (
        f"Weather in **{city}** at {local_time}:\n"
        f"🌡️ {temp}°F — {desc}\n"
        f"💨 Wind: {wind} mph\n"
        f"💧 Humidity: {humidity}%"
    )