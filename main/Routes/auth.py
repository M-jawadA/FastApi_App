from fastapi import APIRouter, Depends, HTTPException
from utils.utils import get_db
from sqlalchemy.orm import Session
from models.user import User
from schemas.response import ResponseModel
from Services.auth import *
from datetime import datetime, timedelta

router = APIRouter()


@router.post("/register/")
async def register(user_data: dict, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user_data.get("username")).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    try:
        user = User(
            username=user_data.get("username"),
            password_hash=User.hash_password(user_data.get("password")),  # Fix this
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return ResponseModel(
            success=True, message="User successfully Created", status=200
        ).model_dump(exclude_none=True, exclude_unset=True)
    except Exception as e:
        return ResponseModel(success=False, error=str(e)).model_dump(
            exclude_none=True, exclude_unset=True
        )


@router.post("/login/")
def login( user_data: dict, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.get("username"), user_data.get("password"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}
