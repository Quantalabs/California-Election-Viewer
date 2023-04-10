import requests

from .. import utils


def getrepresentatives(lat, long):
    url = f"https://v3.openstates.org/people.geo?lat={lat}&lng={long}"
    headers = {"X-API-Key": utils.apikeys.apikeys["openstates"]}
    r = requests.get(url, headers=headers)
    data = r.json()["results"]

    return data
