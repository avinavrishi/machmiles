from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Optional
from database.session import get_db
from database.models import User, Token
from decorator.jwt_decorator import jwt_authorization
from fastapi.responses import JSONResponse
from service.agoda.language_currency import get_language, get_currency
from service.agoda.flight import auto_complete, search_one_way, search_round_trip, flight_details
from datetime import date

class SearchOneWayPayload(BaseModel):
    origin: str
    destination: str
    departureDate: date
    sort: Optional[str] = None # Best, Price, Duration, OnwardDepartureTime, OnwardArrivalTime, ReturnDepartureTime, ReturnArrivalTime, Stops
    page: Optional[int] = 1
    limit: Optional[int] = 20 # Total number of record per api call
    adults: Optional[int] = 1
    children: Optional[int] = 0
    infants: Optional[int] = 0
    cabinType: Optional[str] = 'Economy' # PremiumEconomy, Business, First
    # stops: Optional[int] = None
    language: Optional[str] = 'en-us'
    currency: Optional[str] = 'USD'


router = APIRouter()

@router.get("/get-language/")
def get_language_data():

    language_data = get_language()
    return JSONResponse(content=language_data)

@router.get("/get-currency/")
def get_currency_data():

    currency_data = get_currency()
    return JSONResponse(content=currency_data)


@router.get("/auto-complete-search/")
def auto_complete_search(query: str):

    find_query = auto_complete(query)
    return JSONResponse(content=find_query)


@router.post("/search-one-way-flight")
def search_one_way_flight(request_data: SearchOneWayPayload):

    flight_details = search_one_way(
        request_data.origin,
        request_data.destination,
        request_data.departureDate,
        request_data.sort,
        request_data.page,
        request_data.limit,
        request_data.adults,
        request_data.children,
        request_data.infants,
        request_data.cabinType,
        request_data.language,
        request_data.currency
    )
    return JSONResponse(content=flight_details)







