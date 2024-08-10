import requests
from core.config import RAPIDAPI_KEY, RAPIDAPI_HOST

def auto_complete(query):

    url = "https://agoda-com.p.rapidapi.com/flights/auto-complete"

    querystring = {"query":query}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())

    return response.json()

def search_one_way(origin, destination, departure_date):

    url = "https://agoda-com.p.rapidapi.com/flights/search-one-way"

    querystring = {"origin":origin,"destination":destination, "departureDate": departure_date, "returnDate": retun_date}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())

    return response.json()

def search_round_trip(origin, destination, departure_date, return_date):
    url = "https://agoda-com.p.rapidapi.com/flights/search-roundtrip"

    querystring = {"origin":origin,"destination":destination, "departureDate": departure_date, "returnDate": return_date}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())

    return response.json()

def flight_deyails():
    url = "https://agoda-com.p.rapidapi.com/flights/details"

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers)

    print(response.json())

    return response.json()