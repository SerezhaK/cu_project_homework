from flask import Flask
import requests
import os
from dot import load_dotenv

app = Flask(__name__)

load_dotenv()
ACCUWEATHER_API_KEY = os.getenv("ACCUWEATHER_API_KEY")


def get_current_weather(location_key):
    weather_url = (
        f"http://dataservice.accuweather.com/currentconditions/v1/"
        f"{location_key}?apikey={ACCUWEATHER_API_KEY}&language={"ru"}&details=true"
    )
    data = requests.get(weather_url).json()
    if data:
        return data[0]
    return None


def get_geoposition_of_location(latitude, longitude):
    request_url = (
        f"https://dataservice.accuweather.com/locations/v1/cities/geoposition/"
        f"search?apikey={ACCUWEATHER_API_KEY}&q={latitude}%2C{longitude}&details=true"
    )
    data = requests.get(request_url).json()
    if data:
        return data["Key"]
    return None
