from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from auth import create_access_token, hash_password, verify_password
from database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

import models
import schemas
from auth import create_access_token, hash_password, verify_password
from database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: schemas.UserRegister, db: Session = Depends(get_db)):
    try:
        email = payload.email.strip().lower()
        logging.info(f"Attempting to register user: {email}")

        existing_user = db.query(models.User).filter(models.User.email == email).first()
        if existing_user:
            logging.warning(f"Registration failed: Email {email} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered",
            )

        hashed_password = hash_password(payload.password)
        logging.info(f"Password hashed successfully for {email}")

        new_user = models.User(
            email=email,
            password_hash=hashed_password,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logging.info(f"User {email} registered successfully with ID {new_user.id}")
        return new_user
    except Exception as e:
        logging.error(f"Registration failed for {payload.email}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again.",
        )


@router.post("/login", response_model=schemas.TokenResponse)
def login_user(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    email = payload.email.strip().lower()
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(subject=user.email)
    return schemas.TokenResponse(access_token=token)
