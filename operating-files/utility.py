def get_coordinates(city_name):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
    response = requests.get(geo_url, params=params)
    if response.status_code != 200:
        sys.exit("Error: Could not fetch geolocation.")
    data = response.json()
    if not data.get("results"):
        sys.exit(f"Location not found: {city_name}")
    loc = data["results"][0]
    return loc["latitude"], loc["longitude"], loc["name"]