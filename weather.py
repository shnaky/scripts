#!/usr/bin/env python3

import requests
import os
from os.path import join, dirname, realpath
from dotenv import load_dotenv

# import json

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

    # __repr__ for returning how the class was created
    def __repr__(self):
        # don't forget to put "" to notify that the arguments of the class are strings
        return '{self.__class__.__name__}("{self._city_name}", "{self._country_code}")'.format(
            self=self
        )

    # __str__ for returning human readable class representation as string
    def __str__(self):
        return """{self.__class__.__name__}:
            City Name: {self._city_name}
            Country Code: {self._country_code}
            Latitude: {self._latitude}
            Longitude: {self._longitude}""".format(
            self=self
        )


class Weather:
    # static class variables
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
        self._weather_main = response["weather"][0]["main"]
        self._weather_description = response["weather"][0]["description"]
        self._temp = response["main"]["temp"]
        self._feels_like = response["main"]["feels_like"]
        self._temp_min = response["main"]["temp_min"]
        self._temp_max = response["main"]["temp_max"]
        self._humidity = response["main"]["humidity"]
        self._wind_speed = response["wind"]["speed"]
        # print(self._weather_main)

    def __repr__(self):
        return "{self.__class__.__name__}({self._longitude}, {self._latitude})".format(
            self=self
        )

    def __str__(self):
        return """{self.__class__.__name__}:
            Weather: {self._weather_main}
            Description: {self._weather_description}
            Temperature: {self._temp}
            Feels Like: {self._feels_like}
            Min Temperature: {self._temp_min}
            Max Temperature: {self._temp_max}
            Humidity: {self._humidity}
            Wind Speed: {self._wind_speed}""".format(
            self=self
        )


def main():
    print("city name (required), country code (optional)")
    # list comprehension
    # TODO: make it maybe into a Tuple?
    city_name = [
        x.strip()
        for x in input('usage: "<city name>, <country code>"\n').lower().split(",")
    ]
    if len(city_name) > 1:
        geolocation = Geolocation(city_name[0], city_name[1])
    elif len(city_name) == 1:
        geolocation = Geolocation(city_name[0])
    else:
        raise IndexError("there was no input")

    print()
    print(geolocation)  # call geolocation __str__
    # print(repr(geolocation))
    print()
    weather = Weather(geolocation.longitude, geolocation.latitude)
    weather.current_weather()
    print(weather)


if __name__ == "__main__":
    main()
