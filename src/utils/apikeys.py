from dotenv import dotenv_values

apikeys = {
    "openstates": dotenv_values(".env")["OPENSTATES_API_KEY"],
    "propublica": dotenv_values(".env")["PROPUBLICA_API_KEY"],
    "congress": dotenv_values(".env")["USCONGRESS_API_KEY"],
    "gcivicinfo": dotenv_values(".env")["GCIVICINFO_API_KEY"],
}
