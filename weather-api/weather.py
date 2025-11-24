import requests

API = "https://api.open-meteo.com/v1/forecast"

def get_weather(lat, lon):
    return requests.get(API, params={"latitude": lat, "longitude": lon, "current_weather": True}).json()

if __name__ == "__main__":
    print(get_weather(-25.7, 28.2))