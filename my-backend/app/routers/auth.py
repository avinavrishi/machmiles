from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Dict
from database.session import get_db
from database.models import User, Token
from utils.auth_utils import create_access_token, create_refresh_token, verify_password, hash_password
from datetime import datetime, timedelta
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

router = APIRouter()

# Pydantic Models for Request Validation
class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr  # Ensuring valid email format

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/signup/")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    # Hash password before storing
    hashed_password = hash_password(user.password)

    # Create new user
    new_user = User(username=user.username, password=hashed_password, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "User created successfully", "user_id": new_user.user_id}

@router.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    
    # Verify user exists and password is correct
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    token_data = {"sub": db_user.username, "user_id": db_user.user_id}

    access_token = create_access_token(data=token_data, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data=token_data, expires_delta=refresh_token_expires)

    # Remove existing tokens to prevent multiple refresh tokens for one user
    db.query(Token).filter(Token.user_id == db_user.user_id).delete()
    
    # Save new tokens in database
    db.add_all([
        Token(user_id=db_user.user_id, token_type="access", token=access_token, expires_at=datetime.utcnow() + access_token_expires),
        Token(user_id=db_user.user_id, token_type="refresh", token=refresh_token, expires_at=datetime.utcnow() + refresh_token_expires)
    ])
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }
