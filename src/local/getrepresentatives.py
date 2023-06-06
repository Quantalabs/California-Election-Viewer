import requests

from .. import utils


def byaddress(address):
    url = f"https://www.googleapis.com/civicinfo/v2/representatives?address={address}&levels=administrativeArea1&levels=administrativeArea2&levels=locality&levels=regional&levels=special&levels=subLocality1&levels=subLocality2&key={utils.apikeys.apikeys['gcivicinfo']}"  # noqa: E501
    r = requests.get(url)
    data = r.json()

    return data


def byname(name, district):
    url = f"https://v3.openstates.org/people?jurisdiction=California&name={name}&district={district}&page=1&per_page=10"  # noqa: E501
    headers = {"X-API-Key": utils.apikeys.apikeys["openstates"]}
    r = requests.get(url, headers=headers)
    data = r.json()

    return data["results"][0]
