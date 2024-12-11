from flask import Flask, request, render_template
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
        f"https://dataservice.accuweather.com/currentconditions/v1/"
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
        f"https://dataservice.accuweather.com/locations/v1/cities/"
        f"search?apikey={ACCUWEATHER_API_KEY}&q={city_name}&language={'ru'}"
    )
    data = requests.get(request_url).json()
    if data:
        return data[0]["Key"]
    return None


def get_forecast_data(location_key):
    request_url = (
        f"https://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}"
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


@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    origin_city = None
    destination_city = None
    origin_weather_data = None
    destination_weather_data = None

    if request.method == "POST":
        origin_city = request.form.get("start_city")
        destination_city = request.form.get("end_city")
        if not origin_city or not destination_city:
            output = "Пожалуйста, введите названия обоих городов."
        else:
            try:
                origin_key = get_city_location(origin_city)
                destination_key = get_city_location(destination_city)
                if not origin_key:
                    output = f"Не удалось найти город: {origin_city}"
                    return render_template("index.html", result=output)
                if not destination_key:
                    output = f"Не удалось найти город: {destination_city}"
                    return render_template("index.html", result=output)
                origin_weather_now = get_current_weather(origin_key)
                destination_weather_now = get_current_weather(destination_key)
                if not origin_weather_now:
                    output = f"Не удалось получить данные о погоде для города {origin_city}."
                    return render_template("index.html", result=output)
                if not destination_weather_now:
                    output = f"Не удалось получить данные о погоде для города {destination_city}."
                    return render_template("index.html", result=output)
                origin_forecast_data = get_forecast_data(origin_key)
                destination_forecast_data = get_forecast_data(destination_key)
                if not origin_forecast_data:
                    output = f"Не удалось получить прогноз погоды для города {origin_city}."
                    return render_template("index.html", result=output)
                if not destination_forecast_data:
                    output = f"Не удалось получить прогноз погоды для города {destination_city}."
                    return render_template("index.html", result=output)

                origin_weather_data = {
                    "city": origin_city,
                    "current_temperature": origin_weather_now["Temperature"]["Metric"]["Value"],
                    "weather_text": origin_weather_now["WeatherText"],
                    "wind_speed": origin_weather_now["Wind"]["Speed"]["Metric"]["Value"],
                    "humidity": origin_weather_now["RelativeHumidity"],
                    "pressure": origin_weather_now["Pressure"]["Metric"]["Value"],
                    "min_temp": origin_forecast_data["DailyForecasts"][0]["Temperature"]["Minimum"]["Value"],
                    "max_temp": origin_forecast_data["DailyForecasts"][0]["Temperature"]["Maximum"]["Value"],
                    "precipitation_probability": origin_forecast_data["DailyForecasts"][0]["Day"][
                        "PrecipitationProbability"],
                }

                destination_weather_data = {
                    "city": destination_city,
                    "current_temperature": destination_weather_now["Temperature"]["Metric"]["Value"],
                    "weather_text": destination_weather_now["WeatherText"],
                    "wind_speed": destination_weather_now["Wind"]["Speed"]["Metric"]["Value"],
                    "humidity": destination_weather_now["RelativeHumidity"],
                    "pressure": destination_weather_now["Pressure"]["Metric"]["Value"],
                    "min_temp": destination_forecast_data["DailyForecasts"][0]["Temperature"]["Minimum"]["Value"],
                    "max_temp": destination_forecast_data["DailyForecasts"][0]["Temperature"]["Maximum"]["Value"],
                    "precipitation_probability": destination_forecast_data["DailyForecasts"][0]["Day"][
                        "PrecipitationProbability"],
                }

                is_origin_bad_weather = get_weather_status(
                    origin_weather_data["current_temperature"],
                    origin_weather_data["wind_speed"],
                    origin_weather_data["precipitation_probability"],
                )

                is_destination_bad_weather = get_weather_status(
                    destination_weather_data["current_temperature"],
                    destination_weather_data["wind_speed"],
                    destination_weather_data["precipitation_probability"],
                )

                output = {
                    "origin_weather_data": origin_weather_data,
                    "destination_weather_data": destination_weather_data,
                    "is_origin_bad_weather": is_origin_bad_weather,
                    "is_destination_bad_weather": is_destination_bad_weather,
                }

            except requests.exceptions.RequestException:
                output = "Ошибка подключения к сервису погоды."
            except Exception as e:
                output = f"Произошла ошибка: {str(e)}"

    return render_template(
        "index.html", result=output, start_city=origin_city, end_city=destination_city
    )


if __name__ == "__main__":
    app.run(debug=True)