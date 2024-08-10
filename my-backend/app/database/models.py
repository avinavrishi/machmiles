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
    bookings = relationship('Booking', back_populates='user')
    payments = relationship('Payment', back_populates='user')
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
    user_id = Column(Integer, ForeignKey('users.user_id'))
    flight_number = Column(String, nullable=False)
    departure_date = Column(DateTime, nullable=False)
    arrival_date = Column(DateTime, nullable=False)
    departure_airport = Column(String, nullable=False)
    arrival_airport = Column(String, nullable=False)
    seat_class = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    # Relationships
    user = relationship('User', back_populates='bookings')

class Payment(BaseTable):
    __tablename__ = 'payments'

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    card_number = Column(String, nullable=False)
    card_holder_name = Column(String, nullable=False)
    expiration_date = Column(String, nullable=False)
    cvv = Column(String, nullable=False)

    # Relationships
    user = relationship('User', back_populates='payments')

class Category(BaseTable):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    posts = relationship('Post', back_populates='category')

class Post(BaseTable):
    __tablename__ = 'posts'

    post_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String, nullable=False)
    date_created = Column(DateTime, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'))

    # Relationships
    category = relationship('Category', back_populates='posts')
    comments = relationship('Comment', back_populates='post')

class Comment(BaseTable):
    __tablename__ = 'comments'

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.post_id'))
    author = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    date_created = Column(DateTime, nullable=False)

    # Relationships
    post = relationship('Post', back_populates='comments')