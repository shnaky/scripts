#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Prints movie information using the Omdb API.

Usage:
    ./movies.py

Author:
    Orestis Papandreou - 30.10.2022
"""

import requests
import textwrap

# for .env to get api key
import os
from dotenv import load_dotenv

# import json

load_dotenv()

API_KEY = os.getenv("OMDB_API_KEY")
BASE_URL = "http://www.omdbapi.com/?apikey=" + API_KEY + "&"


def search(movie_name: str) -> None:
    search_url = BASE_URL + "s=" + movie_name
    response = requests.get(search_url).json()
    # print(json.dumps(response, indent=4))

    if response["Response"] == "True":
        num_of_movies = len(response["Search"])

        # print and choose movie if there is more than one result
        choise = 1
        if num_of_movies != 1:
            print_search_result(response, num_of_movies)
            # choose a movie out of the search result to get more details
            choise = int(
                input("Chose a movie by number from 1 to " + str(num_of_movies) + ": ")
            )

        imdbID = list(response["Search"])[choise - 1]["imdbID"]
        movie_info_by_ID(imdbID)

    else:
        print("""\nNo Response!\nreason: {}""".format(response["Error"]))


def print_search_result(movies: dict, num_of_movies: int) -> None:
    skip_list = ["imdbID", "Poster"]

    # print movies in reverse so most popular movie is at the bottom
    for i, movie in enumerate(reversed(movies["Search"])):
        print("\n{}: ".format(num_of_movies - i))
        print("-----------------------------------------------------")
        for key in movie:
            if key not in skip_list:
                print("{:<5}: {}".format(key, movie[key]))
        print("-----------------------------------------------------\n")


def movie_info_by_ID(imdb_ID: str) -> None:
    movie_info_url = BASE_URL + "i=" + imdb_ID + "&plot=short"
    response = requests.get(movie_info_url).json()
    print_movie(response)


def print_movie(movie_info: dict) -> None:
    skip_list = [
        "Title",
        "Year",
        "Plot",
        "Poster",
        "imdbRating",
        "imdbVotes",
        "imdbID",
        "Metascore",
        "Response",
        "Website",
    ]
    # print(json.dumps(movie_info, indent=4))
    rating_exist = True if movie_info["Ratings"] else False

    # print Title (Year) and the short version plot of the movie
    print("\n{} ({})\n".format(movie_info["Title"], movie_info["Year"]))
    print(textwrap.fill(movie_info["Plot"]) + "\n")

    # print all the other movie info
    for key in movie_info:
        if key not in skip_list and key != "Ratings":
            print("{:<30}: {:<5}".format(key, movie_info[key]))
    print()

    # if the movie has Ratings print the scores in a table format
    if rating_exist:
        print("{:<30} {:<5}".format("Source", "Value"))
        print("--------------------------------------")
        for rating in movie_info["Ratings"]:
            print("{:<30} {:<5}".format(rating["Source"], rating["Value"]))
        print("--------------------------------------\n")


def main() -> None:
    movie_name = input("Search for movie title: ")
    search(movie_name)


# if script is not executed as a module but as "main"
if __name__ == "__main__":
    main()
