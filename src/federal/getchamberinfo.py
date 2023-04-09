import json

import requests
from dotenv import dotenv_values


class House:
    def __init__(self):
        self.uscongress = dotenv_values(".env")["USCONGRESS_API_KEY"]
        self.propublica = dotenv_values(".env")["PROPUBLICA_API_KEY"]
        self.openstates = dotenv_values(".env")["OPENSTATES_API_KEY"]

    # Get all house representatives
    def representatives(self):
        url = "https://api.propublica.org/congress/v1/118/house/members.json"
        headers = {"X-API-Key": self.propublica}
        r = requests.get(url, headers=headers)
        data = r.json()["results"][0]

        careps = []

        for member in data["members"]:
            if member["state"] == "CA":
                careps.append(
                    {
                        "first_name": member["first_name"],
                        "last_name": member["last_name"],
                        "district": member["district"],
                        "id": member["id"],
                    }
                )
            else:
                continue

        return careps

    # Get representative of district
    def representative(self, district):
        url = f"https://api.propublica.org/congress/v1/members/house/CA/{district}/current.json"  # noqa: E501
        headers = {"X-API-Key": self.propublica}
        r = requests.get(url, headers=headers)
        data = r.json()["results"][0]

        return data


class Senate:
    def __init__(self):
        self.uscongress = dotenv_values(".env")["USCONGRESS_API_KEY"]
        self.propublica = dotenv_values(".env")["PROPUBLICA_API_KEY"]
        self.openstates = dotenv_values(".env")["OPENSTATES_API_KEY"]

    def senators(self):
        url = "https://api.propublica.org/congress/v1/118/senate/members.json"
        headers = {"X-API-Key": self.propublica}
        r = requests.get(url, headers=headers)
        data = r.json()["results"][0]

        senators = []

        for member in data["members"]:
            if member["state"] == "CA":
                senators.append(
                    {
                        "first_name": member["first_name"],
                        "last_name": member["last_name"],
                        "id": member["id"],
                    }
                )
            else:
                continue

        return senators

    def senator(self, id):
        url = "https://api.propublica.org/congress/v1/members/senate/CA/current.json"  # noqa: E501
        headers = {"X-API-Key": self.propublica}
        r = requests.get(url, headers=headers)
        data = r.json()["results"]

        for senator in data:
            if senator["id"] == id:
                return senator
