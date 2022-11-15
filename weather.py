#!/usr/bin/env python3

import requests
import json
import os
from os.path import join, dirname, realpath
from dotenv import load_dotenv

# load .env file to get api key
dotenv_path = join(dirname(realpath(__file__)), ".env")
load_dotenv(dotenv_path)

GEOCODING_BASE_URL = "http://api.openweathermap.org/geo/1.0/"
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/"
API_KEY = os.environ.get("OPEN_WEATHER_MAP_API_KEY")


class Geolocation:
    def __init__(self, city_name, country_code):
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
        print(request_url)
        response = requests.get(request_url).json()[0]  # Get first response
        del response["local_names"]
        self._city_name = response["name"]
        self._country_code = response["country"]
        self._latitude = response["lat"]
        self._longitude = response["lon"]
        # print(json.dumps(response, indent=4))


class Weather:
    def __init__(self, longitude, latitude):
        self._longitude = longitude
        self._latitude = latitude

    def current_weather(self):
        units = "metric"
        request_url = f"{WEATHER_BASE_URL}weather?lat={self._latitude}&lon={self._longitude}&units={units}&appid={API_KEY}"

        response = requests.get(request_url).json()
        print(json.dumps(response, indent=4))


def main():
    print("city name (required), country code (optional)")
    # list comprehension
    # TODO: make it maybe into a Tuple?
    city_name = [
        x.strip()
        for x in input('usage: "<city name>, <country code>"\n').lower().split(",")
    ]
    print(city_name)
    geolocation = Geolocation(city_name[0], city_name[1])
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
