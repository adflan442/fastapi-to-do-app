from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 

from schemas.user import UserCreate, UserRead
from models import User
from core.db import get_db
from core.security import hash_password, get_current_user

router = APIRouter()

# GET - Current User Credentials

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# GET - All Users

@router.get("/users", response_model=list[UserRead])
def show_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        return []
    return users

# POST - Create a User

@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email Already Registered"
        )
    new_user = User(
        email=user.email, 
        username = user.username,
        firstname = user.firstname,
        lastname = user.lastname,
        hashed_password=hash_password(user.hashed_password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user