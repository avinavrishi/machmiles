from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, JSON, ARRAY, Enum, Table, Float
from sqlalchemy.orm import relationship
from .session import Base
from sqlalchemy.sql import func
# from sqlalchemy.dialects.postgresql import ARRAY

class BaseTable(Base):
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_by = Column(Integer, nullable=True)

class User(BaseTable):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_admin = Column(Integer, nullable=True)
    is_staff = Column(Integer, nullable=True)

    # Relationships
    tokens = relationship('Token', back_populates='user')  # Added relationship

class Token(Base):
    __tablename__ = 'tokens'

    token_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    token_type = Column(String, nullable=False)  # e.g., 'access' or 'refresh'
    token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    # Relationships
    user = relationship('User', back_populates='tokens')  # Added back_populates

class Booking(BaseTable):
    __tablename__ = 'bookings'

    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)
    itinerary_id = Column(String, nullable = False)
    itinerary_token = Column(String, nullable = False)
    pnr_number = Column(String, nullable = True)

    flight_number = Column(String, nullable=False)
    departure_date = Column(DateTime, nullable=False)
    arrival_date = Column(DateTime, nullable=False)
    departure_airport = Column(String, nullable=False)
    arrival_airport = Column(String, nullable=False)
    seat_class = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    gender = Column(String, nullable = False)
    first_name = Column(String, nullable = False)
    middle_name = Column(String, nullable= True)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(String, nullable = False)

    redress_number = Column(String, nullable = True)
    known_traveller_id = Column(String, nullable = True)

    email = Column(String, nullable = False)
    mobile = Column(String, nullable = False)


class Payment(BaseTable):
    __tablename__ = 'payments'

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable = True)
    booking_id = Column(Integer, nullable=False)
    
    card_number = Column(String, nullable=False)
    card_holder_name = Column(String, nullable=False)
    expiration_date = Column(String, nullable=False)
    cvv = Column(String, nullable=False)
    billing_address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    country = Column(String, nullable=False)
    billing_phone = Column(String, nullable=False)