from flask import Flask
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
ACCUWEATHER_API_KEY = os.getenv("ACCUWEATHER_API_KEY")


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
