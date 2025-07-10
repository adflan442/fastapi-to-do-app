from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.core.settings import *
from app.core.security import *
from app.core.db import get_db

from app.db_ops.user import UserService

from app.models.user import User
from app.schemas.user import UserRegister, UserRead
from app.schemas.token import Token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# Login route (token URL)
@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(form_data: UserRegister, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Username {user.username} already exists"
        )
    user = db.query(User).filter(User.email == form_data.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Email {user.email} already exists"
        )
    new_user = UserService(db).create_user(form_data)
    return new_user
    