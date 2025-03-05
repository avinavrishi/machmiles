import requests
from core.config import RAPIDAPI_KEY, RAPIDAPI_HOST

def make_api_request(url, querystring):
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return {"status": "success", "data": response.json()}
    except requests.exceptions.HTTPError as http_err:
        return {"status": "error", "code": response.status_code, "message": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.ConnectionError as conn_err:
        return {"status": "error", "code": None, "message": f"Connection error occurred: {conn_err}"}
    except requests.exceptions.Timeout as timeout_err:
        return {"status": "error", "code": None, "message": f"Timeout error occurred: {timeout_err}"}
    except requests.exceptions.RequestException as req_err:
        return {"status": "error", "code": None, "message": f"An error occurred: {req_err}"}
    except ValueError as json_err:
        return {"status": "error", "code": None, "message": f"JSON decode error: {json_err}"}

def auto_complete(query):
    url = "https://agoda-com.p.rapidapi.com/flights/auto-complete"
    querystring = {"query": query}
    return make_api_request(url, querystring)

def search_one_way(origin, destination, departure_date, sort, page, page_limit, adults, children, infant, cabin_type, language, currency):
    url = "https://agoda-com.p.rapidapi.com/flights/search-one-way"
    querystring = {
        "origin": origin,
        "destination": destination,
        "departureDate": departure_date,
        "sort": sort,
        "page": page,
        "limit": page_limit,
        "adults": adults,
        "children": children,
        "infants": infant,
        "cabinType": cabin_type,
        "language": language,
        "currency": currency
    }
    return make_api_request(url, querystring)

def search_round_trip(origin, destination, departure_date, return_date, sort, page, page_limit, adults, children, infant, cabin_type, language, currency):
    url = "https://agoda-com.p.rapidapi.com/flights/search-roundtrip"
    querystring = {
        "origin": origin,
        "destination": destination,
        "departureDate": departure_date,
        "returnDate": return_date,
        "sort": sort,
        "page": page,
        "limit": page_limit,
        "adults": adults,
        "children": children,
        "infants": infant,
        "cabinType": cabin_type,
        "language": language,
        "currency": currency
    }
    return make_api_request(url, querystring)

def flight_details(itinerary_id, token, language, currency):
    url = "https://agoda-com.p.rapidapi.com/flights/details"
    querystring = {"itineraryId": itinerary_id, "token": token, "language": language, "currency": currency}
    return make_api_request(url, querystring)