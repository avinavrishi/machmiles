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

class SearchTwoWayPayload(BaseModel):
    origin: str
    destination: str
    departureDate: date
    returnDate: date
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

class GetFlightDetails(BaseModel):
    itenary_id: str
    token: str
    language: Optional[str] = 'en-us'
    currency: Optional[str] = 'USD'

class GetConfirmFlightBooking(BaseModel):
    itinerary_id: str
    itinerary_token: str
    flight_number: str
    seat_class: str
    departure_date: date
    arrival_date: date
    departure_airport: str
    arrival_airport: str
    price: float
    gender: str
    first_name: str
    middle_name: Optional[str]
    last_name: str
    date_of_birth: str
    redress_number: Optional[str]
    known_traveller_id: Optional[str]
    email: str
    mobile: str

    card_number: str
    card_holder_name: str
    expiration_date: str
    cvv: str
    billing_address: str
    city: str
    state: str
    postal_code: str
    country: str
    billing_phone: str



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

    bundles = flight_details['data']['bundles']

    data=[]

    for bundle in bundles:
        itenary = bundle['itineraries'][0]['itineraryInfo']
        itenary_data = {
            "id" : itenary['id'],
            "token": itenary['token'],
            "flight_number": bundle['outboundSlice']['segments'][0]['flightNumber'],
            "carrier_name": itenary['ticketingCarrierContent']['carrierName'],
            "carrier_image": itenary['ticketingCarrierContent']['carrierIcon'],
            "carrier_code": itenary['ticketingCarrierContent']['carrierCode'],
            "arrival_date_time": bundle['outboundSlice']['segments'][0]['arrivalDateTime'],
            "departure_date_time": bundle['outboundSlice']['segments'][0]['departDateTime'],
            "departure_arrival_airport": bundle['outboundSlice']['segments'][0]['airportContent'],
            "total_trip_duration": itenary['totalTripDuration'],
            "cabin_class": bundle['outboundSlice']['segments'][0]['cabinClassContent'],
            "passport_required": itenary['passportRequired'],
            "cart_info": itenary['cartInfo']

        }

        for price in itenary['price'][(request_data.currency).lower()]['charges']:
            if price['type'] == 'Fare':
                itenary_data['price_inclusive'] = price['total']['inc']
                itenary_data['price_exclusive'] = price['total']['exc']
                break

        # print(itenary_data)
        # print("=======================")
        

        data.append(itenary_data)

    return JSONResponse(content=data)


@router.post("/search-two-way-flight")
def search_two_way_flight(request_data: SearchTwoWayPayload):

    flight_details = search_round_trip(
        request_data.origin,
        request_data.destination,
        request_data.departureDate,
        request_data.returnDate,
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

    bundles = flight_details['data']['bundles']

    data=[]

    for bundle in bundles:
        itenary = bundle['itineraries'][0]['itineraryInfo']
        itenary_data = {
            "id" : itenary['id'],
            "token": itenary['token'],
            "flight_number": bundle['outboundSlice']['segments'][0]['flightNumber'],
            "carrier_name": bundle['itineraries'][0]['inboundSlice']['segments'][0]['carrierContent']['carrierName'],
            "carrier_image": bundle['itineraries'][0]['inboundSlice']['segments'][0]['carrierContent']['carrierIcon'],
            "carrier_code": bundle['itineraries'][0]['inboundSlice']['segments'][0]['carrierContent']['carrierCode'],
            "arrival_date_time": bundle['outboundSlice']['segments'][0]['arrivalDateTime'],
            "departure_date_time": bundle['outboundSlice']['segments'][0]['departDateTime'],
            "departure_arrival_airport": bundle['outboundSlice']['segments'][0]['airportContent'],
            "total_trip_duration": itenary['totalTripDuration'],
            "cabin_class": bundle['outboundSlice']['segments'][0]['cabinClassContent'],
            "passport_required": itenary['passportRequired'],
            "cart_info": itenary['cartInfo']

        }

        for price in itenary['price'][(request_data.currency).lower()]['charges']:
            if price['type'] == 'Fare':
                itenary_data['price_inclusive'] = price['total']['inc']
                itenary_data['price_exclusive'] = price['total']['exc']
                break

        data.append(itenary_data)

    return JSONResponse(content=data)


@router.post("/get-flight-details")
def search_one_way_flight(request_data: GetFlightDetails):

    flight_data = flight_details(request_data.itenary_id, request_data.token)

    itinerary = flight_data['data']['itinerary']

    itenary_data = {
        "itinerary_id": itinerary['id'],
        "token": itinerary['token'],
        "lap_infant_allowed": itinerary['lapInfantsAllowed'],
        "password_required": itinerary['passportRequired'],
        "carrier_image": itinerary['ticketingAirline']['logo']['normal'],
        "carrier_name": itinerary['ticketingAirline']['name'],
        "flight_number": itinerary['slices'][0]['segments'][0]['flightNumber'],
        "departure_time": itinerary['slices'][0]['segments'][0]['departureTime'],
        "origin_data": itinerary['slices'][0]['segments'][0]['origin'],
        "arrival_time": itinerary['slices'][0]['segments'][0]['arrivalTime'],
        "destination": itinerary['slices'][0]['segments'][0]['destination'],
        "trip_duration": itinerary['slices'][0]['segments'][0]['duration'],
        "cabin_class": itinerary['slices'][0]['segments'][0]['cabinClass'],
        "cabin_name": itinerary['slices'][0]['segments'][0]['cabinName'],
        "baggage_fee": itinerary['slices'][0]['segments'][0]['baggageFee']['value'],
        "aircraft_data": itinerary['slices'][0]['segments'][0]['aircraft'],
        "base_fare": itinerary['pricing']['baseFare']['value'],
        "total_tax": itinerary['pricing']['totalTaxes']['value'],
        "total_fare": itinerary['pricing']['totalFare']['value'],
        "total_fare_per_passenger": itinerary['pricing']['totalFarePerPassenger']['value'],
        "total_tax_per_passenger": itinerary['pricing']['totalTaxPerPassenger']['value'],
        "total_discount": itinerary['pricing']['totalDiscount']['amount']['value'],
        "total_inclusive_per_passenger": itinerary['pricing']['totalInclusivePerPassenger']['value']
    }

    return JSONResponse(content=itenary_data)


@router.post("/confirm-flight-booking")
def confirm_flight_booking(request_data: GetConfirmFlightBooking, db: Session = Depends(get_db)):
    try:
        # Step 1: Save Booking Details
        new_booking = Booking(
            itinerary_id=request_data.itinerary_id,
            itinerary_token=request_data.itinerary_token,
            flight_number=request_data.flight_number,
            departure_date=request_data.departure_date,
            arrival_date=request_data.arrival_date,
            departure_airport=request_data.departure_airport,
            arrival_airport=request_data.arrival_airport,
            seat_class=request_data.seat_class,  # Assuming a default seat class
            price=request_data.price,
            gender=request_data.gender,
            first_name=request_data.first_name,
            middle_name=request_data.middle_name,
            last_name=request_data.last_name,
            date_of_birth=request_data.date_of_birth,
            redress_number=request_data.redress_number,
            known_traveller_id=request_data.known_traveller_id,
            email=request_data.email,
            mobile=request_data.mobile,
            pnr_number=None  # Can be generated later
        )

        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)  # Retrieve the newly created booking_id

        # Step 2: Save Payment Details
        new_payment = Payment(
            booking_id=new_booking.booking_id,
            card_number=request_data.card_number,
            card_holder_name=request_data.card_holder_name,
            expiration_date=request_data.expiration_date,
            cvv=request_data.cvv,
            billing_address=request_data.billing_address,
            city=request_data.city,
            state=request_data.state,
            postal_code=request_data.postal_code,
            country=request_data.country,
            billing_phone=request_data.billing_phone
        )

        db.add(new_payment)
        db.commit()

        return {
            "status": "success",
            "message": "Flight booking confirmed successfully!",
            "booking_id": new_booking.booking_id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Booking failed: {str(e)}")

