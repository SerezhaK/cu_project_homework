from flask import Flask
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
ACCUWEATHER_API_KEY = os.getenv("ACCUWEATHER_API_KEY")

"""
get requests:

1. get_current_weather
This function retrieves the current weather conditions for a specified location using its unique location_key.
Parameters:
    location_key: A string representing the unique identifier for a specific location.
Process:
    Constructs a request URL to access current weather conditions.
    Sends a GET request to the AccuWeather API.
    Parses the JSON response and returns the first element if data is available; otherwise, it returns None.

2. get_geo_position_of_location
This function finds the location key based on geographic coordinates (latitude and longitude).
Parameters:
    latitude: A float representing the latitude of the location.
    longitude: A float representing the longitude of the location.
Process:
    Constructs a request URL to search for a city based on its geographic position.
    Sends a GET request to the AccuWeather API.
    Parses the JSON response and returns the location key if data is available; otherwise, it returns None.

3. get_location
This function retrieves the location key for a specified city name.
Parameters:
    city_name: A string representing the name of the city.
Process:
    Constructs a request URL to search for a city by name.
    Sends a GET request to the AccuWeather API.
    Parses the JSON response and returns the first element's key if data is available; otherwise, it returns None.

4. get_weather_conditions
This function retrieves the daily weather forecast for a specified location using its unique location_key.
Parameters:
    location_key: A string representing the unique identifier for a specific location.
Process:
    Constructs a request URL to access daily forecast data.
    Sends a GET request with parameters including API key and language settings.
    Parses the JSON response and returns it if data is available; otherwise, it returns None.
"""

def get_current_weather(location_key):
    request_url = (
        f"http://dataservice.accuweather.com/currentconditions/v1/"
        f"{location_key}?apikey={ACCUWEATHER_API_KEY}&language={'ru'}&details=true"
    )
    data = requests.get(request_url).json()
    if data:
        return data[0]
    return None


def get_geo_position_of_location(latitude, longitude):
    request_url = (
        f"https://dataservice.accuweather.com/locations/v1/cities/geoposition/"
        f"search?apikey={ACCUWEATHER_API_KEY}&q={latitude}%2C{longitude}&details=true"
    )
    data = requests.get(request_url).json()
    if data:
        return data["Key"]
    return None


def get_city_location(city_name):
    request_url = (
        f"http://dataservice.accuweather.com/locations/v1/cities/"
        f"search?apikey={ACCUWEATHER_API_KEY}&q={city_name}&language={'ru'}"
    )
    data = requests.get(request_url).json()
    if data:
        return data[0]["Key"]
    return None


def get_forecast_data(location_key):
    request_url = (
        f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}"
    )
    response = requests.get(
        request_url,
        params={
            "apikey": ACCUWEATHER_API_KEY,
            "language": "ru",
            "details": "true",
            "metric": "true",
        }
    )
    data = response.json()
    if data:
        return data
    return None


def get_weather_status(temperature, wind_speed, precipitation_probability):
    warnings = []
    if temperature < -10 or temperature > 40:
        warnings.append("экстремальная температура")
    elif wind_speed > 55:
        warnings.append("сильный ветер")
    elif precipitation_probability > 65:
        warnings.append("вероятность осадков")
    if warnings:
        return "Неблагоприятные погодные условия: " + ", ".join(warnings) + "."
    return "Благоприятный погодные условия."
