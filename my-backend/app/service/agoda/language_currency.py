import requests
from core.config import RAPIDAPI_KEY, RAPIDAPI_HOST


def get_language():

    url = "https://agoda-com.p.rapidapi.com/languages"

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers)

    return response.json()

def get_currency():
    url = "https://agoda-com.p.rapidapi.com/currencies"

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers)

    return response.json()