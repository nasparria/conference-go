from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import requests
import json


def get_photo(city, state):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": f"{city}, {state}",
        "per_page": 1,
    }
    url = "https://api.pexels.com/v1/search?query="
    request = requests.get(url, headers=headers, params=params)
    photo_data = json.loads(request.content)

    try:
        return {"picture_url": photo_data["photos"][0]["src"]["large"]}
    except (KeyError, IndexError):
        return {"picture_url": None}


def get_weather_data(city, state):
    params = {
        "q": f"{city}, {state}, US",
        "limit": 1,
        "appid": OPEN_WEATHER_API_KEY,
    }
    url = "https://api.openweathermap.org/geo/1.0/direct"
    request = requests.get(url, params=params)
    location_data = json.loads(request.content)

    try:
        latitude = location_data[0]["lat"]
        longitude = location_data[0]["lon"]
    except(KeyError, IndexError):
        return None

    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "imperial",
    }

    url = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(url, params=params)
    weather_data = json.loads(response.content)

    try:
        return {
            "description": weather_data["weather"][0]["description"],
            "temp": weather_data["main"]["temp"],
        }
    except(KeyError, IndexError):
        return None
