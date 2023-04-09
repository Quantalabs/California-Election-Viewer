from geopy import Nominatim


def get_coordinates(address):
    geolocator = Nominatim(user_agent="my_app")
    location = geolocator.geocode(address)
    return location.latitude, location.longitude
