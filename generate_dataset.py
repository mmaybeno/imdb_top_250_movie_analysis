"""
Python script that creates a dataset of imdb top 250 movies and wikipedia page revisions

Matt Maybeno 2019
"""
import re
import csv
import logging
import requests
from imdb import IMDb

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_data():
    """
    Fetches Top 250 movies using IMDB data with wikipedia revisions
    and dumps it into a file.

    :return:
    """
    ia = IMDb()
    top250 = ia.get_top250_movies()

    with open(
        "files/top250_imdb_movies_with_wikipedia_revisions.csv", mode="w"
    ) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["rank", "title", "year", "votes", "kind", "rating", "revisions"]
        )

        for movie in top250:
            rank = movie.data["top 250 rank"]
            movie_title = movie.data["title"]
            year = movie.data["year"]
            votes = movie.data["votes"]
            kind = movie.data["kind"]
            rating = movie.data["rating"]

            pageid = find_wikipedia_film_page_id(movie_title, year)
            if pageid is None:
                movie_title = re.sub("[^A-Za-z0-9 ]+", "", movie_title)
                pageid = find_wikipedia_film_page_id(movie_title, year)
            if pageid is not None:
                revisions_number = get_wikipedia_revisions(pageid)
                logger.info(f"fetched {revisions_number} revisions for {movie_title}")
            else:
                logger.error(f"Unable to fetch movie page for {movie_title}")
                return
            writer.writerow(
                [rank, movie_title, year, votes, kind, rating, revisions_number]
            )


def find_wikipedia_film_page_id(movie_title, year):
    """
    Attempts to find the wikipedia page id of a film given its
    title and year.

    :param movie_title:
    :param year:
    :return:
    """
    api_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "description",
        "format": "json",
        "titles": f"{movie_title}",
        "redirects": True,
    }

    response = requests.get(api_url, params=params)
    pageid = get_pageid(response)

    if pageid is None:
        params["titles"] = f"{movie_title} (film)"
    response = requests.get(api_url, params=params)
    pageid = get_pageid(response)

    if pageid is None:
        params["titles"] = f"{movie_title} ({year} film)"
    response = requests.get(api_url, params=params)
    pageid = get_pageid(response)

    return pageid


def get_pageid(response):
    """
    Parses a request to get the page id.

    :param response:
    :return:
    """
    if response.status_code == requests.codes.ok:
        response_data = response.json()
        first_page = list(response_data.get("query", {}).get("pages", {}).values())[0]
        description = first_page.get("description", "")
        title = first_page.get("title", "")
        movie_words = [
            "film",
            "movie",
            "drama",
            "motion picture",
            "feature",
            "picture",
            "cinema",
        ]
        # Make sure the page is the actual movie
        if description:
            if "film" in title:
                return first_page["pageid"]
            if any(word in description for word in movie_words):
                return first_page["pageid"]


def get_wikipedia_revisions(pageids, rvcontinue=None):
    """
    Query wikipedia to fetch number of revisions

    :param pageids:
    :param rvcontinue:
    :return:
    """

    api_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "revisions",
        "format": "json",
        "pageids": pageids,
        "rvprop": "ids|timestamp",
        "rvlimit": 5000,
    }
    if rvcontinue is not None:
        params["rvcontinue"] = rvcontinue
    response = requests.get(api_url, params=params)

    if response.status_code == requests.codes.ok:
        response_data = response.json()
        first_page = list(response_data.get("query", {}).get("pages", {}).values())[0]
        revisions = first_page["revisions"]
        revisions_number = len(revisions)

        rvcontinue = response_data.get("continue", {}).get("rvcontinue", "")
        if rvcontinue:
            revisions_number += get_wikipedia_revisions(pageids, rvcontinue)
        return revisions_number

    else:
        logger.error(f"Problem fetching wikipedia data for {movie_title}")
        return 0


if __name__ == "__main__":
    get_data()
