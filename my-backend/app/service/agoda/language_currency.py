import requests
from core.config import RAPIDAPI_KEY, RAPIDAPI_HOST


def language():

    url = "https://agoda-com.p.rapidapi.com/languages"

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers)

    print(response.json())

    return response.json()

def currency():
    url = "https://agoda-com.p.rapidapi.com/currencies"

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers)

    print(response.json())

    return response.json()