from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 

from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.models.user import User
from app.db_ops.user import UserService
from app.core.db import get_db
from app.core.security import hash_password, get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# GET - Current User Credentials

# UserRead omits the password field - see schemas/user.py
@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# GET user - this is for admins, but could update for user or admin okay and forget /me route

@router.get("/{user_id}",response_model=UserRead)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return UserService(db).get_user_by_id(user_id, current_user)


# GET - All Users

@router.get("/", response_model=list[UserRead])
def show_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        return []
    return users

# POST - Create a User

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
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
        hashed_password=hash_password(user.password),
        role = user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# PATCH - Update a User

@router.patch("/{user_id}",  response_model=UserRead)
def update_user(
    user_id: int, 
    user: UserUpdate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    updated_user = UserService(db).update_user(user_id, user, current_user)
    if updated_user:
        return updated_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Can't find User with ID {user_id}"
    )



# DELETE - Delete a User

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    UserService(db).delete_user(user_id, current_user)



    

