import requests
import argparse
import sys
from datetime import datetime

def get_coordinates(city_name):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
    try:
        response = requests.get(geo_url, params=params)
        response.raise_for_status()
        data = response.json()

        # 👇 Add debugging info
        print("🔍 Full request URL:", response.url)
        print("🧾 Response JSON:", data)

        if not data.get("results"):
            print("⚠️ No results found.")
            return None

        loc = data["results"][0]
        return loc["latitude"], loc["longitude"], loc["name"]
    except requests.RequestException as e:
        print(f"❌ Error fetching coordinates: {e}")
        return None