#!/usr/bin/env python3

import requests
import json
import os
from os.path import join, dirname, realpath
from dotenv import load_dotenv

# load .env file to get api key
dotenv_path = join(dirname(realpath(__file__)), ".env")
load_dotenv(dotenv_path)

API_KEY = os.environ.get("OPEN_WEATHER_MAP_API_KEY")
GEOCODING_BASE_URL = "http://api.openweathermap.org/geo/1.0/"
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/"


class Geolocation:
    def __init__(self, city_name, country_code=None):
        self._city_name = None
        self._country_code = None
        self._latitude = None
        self._longitude = None
        self._direct_geocoding((city_name, country_code))

    @property
    def city_name(self):
        return self._city_name

    @property
    def country_code(self):
        return self._country_code

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    def update_geolocation(self, city_name, country_code):
        self._direct_geocoding((city_name, country_code))

    def _direct_geocoding(self, city_name: tuple, limit: int = 5):
        request_url = (
            f"{GEOCODING_BASE_URL}direct?q={city_name}&limit={limit}&appid={API_KEY}"
        )

        try:
            response = requests.get(request_url).json()[0]  # Get first response
        except IndexError:
            raise ValueError("Bad API request")

        del response["local_names"]
        self._city_name = response["name"]
        self._country_code = response["country"]
        self._latitude = response["lat"]
        self._longitude = response["lon"]
        # print(json.dumps(response, indent=4))


class Weather:
    _units = "metric"

    def __init__(self, longitude, latitude):
        self._longitude = longitude
        self._latitude = latitude
        self._weather_main = None
        self._weather_description = None
        self._temp = None
        self._feels_like = None
        self._temp_min = None
        self._temp_max = None
        self._humidity = None
        self._wind_speed = None

    def current_weather(self):
        request_url = f"{WEATHER_BASE_URL}weather?lat={self._latitude}&lon={self._longitude}&units={Weather._units}&appid={API_KEY}"

        response = requests.get(request_url).json()
        print(json.dumps(response, indent=4))
        self._weather_main = response["weather"][0]["main"]
        self._weather_description = response["weather"][0]["description"]
        self._temp = response["main"]["temp"]
        self._feels_like = response["main"]["feels_like"]
        self._temp_min = response["main"]["temp_min"]
        self._temp_max = response["main"]["temp_max"]
        self._humidity = response["main"]["humidity"]
        self._wind_speed = response["wind"]["speed"]
        # print(self._weather_main)


def main():
    print("city name (required), country code (optional)")
    # list comprehension
    # TODO: make it maybe into a Tuple?
    city_name = [
        x.strip()
        for x in input('usage: "<city name>, <country code>"\n').lower().split(",")
    ]
    print(city_name)
    if len(city_name) > 1:
        geolocation = Geolocation(city_name[0], city_name[1])
    elif len(city_name) == 1:
        geolocation = Geolocation(city_name[0])
    else:
        raise IndexError("there was no input")

    print(
        geolocation.city_name,
        geolocation.country_code,
        geolocation.latitude,
        geolocation.longitude,
    )
    weather = Weather(geolocation.longitude, geolocation.latitude)
    weather.current_weather()


if __name__ == "__main__":
    main()
