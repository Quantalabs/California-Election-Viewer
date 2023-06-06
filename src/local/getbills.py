import requests

from .. import utils


def byrepresentative(reprid):
    url = f"https://v3.openstates.org/bills?jurisdiction=California&sort=updated_desc&sponsor={reprid}&page=1&per_page=10"  # noqa: E501
    headers = {"X-API-Key": utils.apikeys.apikeys["openstates"]}

    r = requests.get(url, headers=headers)
    data = r.json()

    return data


def byid(billid):
    url = f"https://v3.openstates.org/bills/ocd-bill/{billid}"
    headers = {"X-API-Key": utils.apikeys.apikeys["openstates"]}

    r = requests.get(url, headers=headers)
    data = r.json()

    return data
