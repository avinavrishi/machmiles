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
    return response.json()

def search_one_way(origin, destination, departure_date, sort, page, page_limit, adults, children, infant, cabin_type, language, currency):

    url = "https://agoda-com.p.rapidapi.com/flights/search-one-way"

    querystring = {
        "origin":origin,
        "destination":destination,
        "departureDate":departure_date,
        "sort":sort,
        "page":page,
        "limit":page_limit,
        "adults":adults,
        "children":children,
        "infants":infant,
        "cabinType":cabin_type,
        "language":language,
        "currency":currency
        }

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()

def search_round_trip(origin, destination, departure_date, return_date, sort, page, page_limit, adults, children, infant, cabin_type, language, currency):
    url = "https://agoda-com.p.rapidapi.com/flights/search-roundtrip"

    querystring = {
        "origin":origin,
        "destination":destination,
        "departureDate":departure_date,
        "returnDate": return_date,
        "sort":sort,
        "page":page,
        "limit":page_limit,
        "adults":adults,
        "children":children,
        "infants":infant,
        "cabinType":cabin_type,
        "language":language,
        "currency":currency
        }


    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()

def flight_details(itenary_id, token):

    url = "https://agoda-com.p.rapidapi.com/flights/details"

    querystring = {"itineraryId":itenary_id,"token":token}

    headers = {
        "x-rapidapi-key": "f419aee40cmsh30d7ffb65a062fbp145396jsn95b5295dfb39",
        "x-rapidapi-host": "agoda-com.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()