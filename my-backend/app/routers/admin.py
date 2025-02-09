from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Dict
from database.session import get_db
from database.models import User, Token
from datetime import datetime, timedelta
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

router = APIRouter()

@router.post("/get-all-users")
def get_all_user(db: Session = Depends(get_db)):

    all_users = db.query(User).filter(User.is_admin != 1).all()

    if not all_users:
        raise HTTPException(status_code=404, detail="Users not found")

    return {"user": all_users}


@router.delete("/delete-user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}


@router.get("/get-all-bookings")
def get_all_bookings(db: Session = Depends(get_db)):
    all_bookings = db.query(Booking).all()
    
    if not all_bookings:
        raise HTTPException(status_code=404, detail="No bookings found")
    
    return {"bookings": all_bookings}

@router.post("/set-status/{booking_id}")
def set_status(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking.status = 1
    db.commit()
    db.refresh(booking)
    
    return {"message": "Booking status updated to 1", "booking": booking}


@router.delete("/delete-booking/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    db.delete(booking)
    db.commit()
    
    return {"message": "Booking deleted successfully"}


@router.get("/get-all-payments")
def get_all_payments(db: Session = Depends(get_db)):
    all_payments = db.query(Payment).all()
    
    if not all_payments:
        raise HTTPException(status_code=404, detail="No payments found")
    
    return {"payments": all_payments}


@router.delete("/delete-payment/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    db.delete(payment)
    db.commit()
    
    return {"message": "Payment deleted successfully"}

