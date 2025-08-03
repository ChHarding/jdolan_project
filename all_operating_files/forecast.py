import requests

def get_forecast_summary(city_name, latitude, longitude):
    """
    Gets a 7-day weather forecast summary for a given location.
    """
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
        "timezone": "auto"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json().get("daily", {})
        summary = {
            "city": city_name,
            "dates": data.get("time"),
            "temp_max": data.get("temperature_2m_max"),
            "temp_min": data.get("temperature_2m_min"),
            "precip": data.get("precipitation_sum")
        }
        return summary
    else:
        print(f"Error fetching forecast: {response.status_code}")
        return None