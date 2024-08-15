from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict
from database.session import get_db
from database.models import User, Token
from utils.auth_utils import create_access_token, create_refresh_token, verify_token
from datetime import datetime, timedelta
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/signup/")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = user.password  # You should hash the password before storing it
    new_user = User(username=user.username, password=hashed_password, email=user.email)
    db.add(new_user)
    db.commit()

    return {"msg": "User created successfully"}

@router.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or db_user.password != user.password:  # You should hash passwords for comparison
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    # Insert username and user_id into the token data
    token_data = {
        "sub": user.username,
        "user_id": db_user.user_id
    }

    access_token = create_access_token(data=token_data, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data=token_data, expires_delta=refresh_token_expires)

    # Save tokens in the database
    db_token_access = Token(
        user_id=db_user.user_id,
        token_type="access",
        token=access_token,
        expires_at=datetime.utcnow() + access_token_expires
    )
    db_token_refresh = Token(
        user_id=db_user.user_id,
        token_type="refresh",
        token=refresh_token,
        expires_at=datetime.utcnow() + refresh_token_expires
    )
    db.add(db_token_access)
    db.add(db_token_refresh)
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }

