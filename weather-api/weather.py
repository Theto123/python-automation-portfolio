import requests
import csv
import json
import time
from datetime import datetime

API_URL = "https://api.open-meteo.com/v1/forecast"
HEADERS = {"User-Agent": "WeatherClient/1.0"}
RETRIES = 3
LOCATIONS = [
    {"name": "Polokwane", "lat": -23.9, "lon": 29.45},
    {"name": "Johannesburg", "lat": -26.2, "lon": 28.04},
    {"name": "Cape Town", "lat": -33.92, "lon": 18.42}
]
CACHE_FILE = "weather_cache.json"

def fetch_weather(lat, lon):
    """Fetch current weather data with retry logic."""
    for attempt in range(1, RETRIES + 1):
        try:
            response = requests.get(API_URL, headers=HEADERS, params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
                "timezone": "auto"
            }, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Attempt {attempt} failed for ({lat}, {lon}): {e}")
            time.sleep(1)
    return None

def parse_weather(data):
    """Extract relevant weather info from API response."""
    if not data or "current_weather" not in data:
        return None
    weather = data["current_weather"]
    return {
        "temperature": weather.get("temperature"),
        "windspeed": weather.get("windspeed"),
        "winddirection": weather.get("winddirection"),
        "time": weather.get("time")
    }

def save_to_csv(data, filename="weather_data.csv"):
    """Save weather data to a CSV file."""
    if not data:
        return
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def save_cache(data):
    """Save weather data to JSON cache."""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_cache():
    """Load weather data from JSON cache."""
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

if __name__ == "__main__":
    weather_data = load_cache()
    for loc in LOCATIONS:
        print(f"Fetching weather for {loc['name']}...")
        data = fetch_weather(loc["lat"], loc["lon"])
        parsed = parse_weather(data)
        if parsed:
            parsed["location"] = loc["name"]
            parsed["fetched_at"] = datetime.now().isoformat()
            weather_data.append(parsed)
            print(parsed)
        else:
            print(f"Failed to fetch data for {loc['name']}")
        time.sleep(0.5)  # polite pause between requests

    save_to_csv(weather_data)
    save_cache(weather_data)
