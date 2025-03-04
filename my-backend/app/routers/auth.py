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
async def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        # Get user with a single query
        db_user = (
            db.query(User)
            .filter(User.username == user.username)
            .first()
        )
        
        # Early return if user doesn't exist or password is wrong
        if not db_user or not verify_password(user.password, db_user.password):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        # Parse environment variables with error handling
        try:
            access_token_expire_minutes = int(ACCESS_TOKEN_EXPIRE_MINUTES)
            refresh_token_expire_days = int(REFRESH_TOKEN_EXPIRE_DAYS)
        except ValueError:
            raise HTTPException(
                status_code=500,
                detail="Invalid token expiration configuration"
            )

        # Calculate token expiration times
        current_time = datetime.utcnow()
        access_token_expires = timedelta(minutes=access_token_expire_minutes)
        refresh_token_expires = timedelta(days=refresh_token_expire_days)

        
        token_data = {
            "sub": db_user.username,
            "user_id": db_user.user_id,
            "type": "access"  # Add token type for additional security
        }
        refresh_token_data = {
            "sub": db_user.username,
            "user_id": db_user.user_id,
            "type": "refresh"
        }


        # Generate tokens
        access_token = create_access_token(
            data=token_data,
            expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(
            data=refresh_token_data,
            expires_delta=refresh_token_expires
        )

        print("hiiiiiiii")

        # Use a transaction for database operations
        try:
            # Remove old tokens
            db.query(Token).filter(Token.user_id == db_user.user_id).delete()
            
            # Add new tokens
            db.add_all([
                Token(
                    user_id=db_user.user_id,
                    token_type="access",
                    token=access_token,
                    expires_at=current_time + access_token_expires
                ),
                Token(
                    user_id=db_user.user_id,
                    token_type="refresh",
                    token=refresh_token,
                    expires_at=current_time + refresh_token_expires
                )
            ])
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error while processing authentication"
            )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": access_token_expire_minutes * 60  # Return expiration in seconds
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error during authentication"
        )
