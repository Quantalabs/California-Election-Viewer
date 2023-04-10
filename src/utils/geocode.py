import urllib.parse as urlparse

import requests


def get_coordinates(address):
    url = f"https://geocode.maps.co/search?q={urlparse.quote(address)}"

    response = requests.get(url)
    data = response.json()
    lat = data[0]["lat"]
    long = data[0]["lon"]

    return lat, long
