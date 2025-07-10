from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User, UserRole
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.permissions import Permissions

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password) -> str:
        return self.pwd_context.hash(password)
        
    def authenticate_user(self, email: str, password: str) -> User | None:
        user = self.get_user_by_email(email)
        if not user or not self.pwd_context.verify(password, user.hashed_password):
            return None
        return user

    def get_user_by_id(self, user_id: int, current_user: User) -> User | None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"We can't find any User with id {user_id} in our system"
            )
        Permissions.require_admin_or_owner(user_id, current_user)
        return user
    
    def get_user_by_email(self, email: str, current_user: User) -> User | None:
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No user found with email: {email} "
            )
        Permissions.require_admin_or_owner(user.id, current_user)
        return user
        
    
    def get_all_users(self, current_user: User) -> list[User]:
        Permissions.require_admin(current_user)
        return self.db.query(User).all()
    
    def get_all_by_role(self, current_user: User, role: UserRole) -> list[User]:
        Permissions.require_admin(current_user)
        return self.db.query(User).filter(User.role == role).all()
    
    def create_user(self, user_data: UserCreate) -> User:
        hashed_pw = self.hash_password(user_data.password)
        user = User(
            email=user_data.email,
            username=user_data.username,
            firstname=user_data.firstname,
            lastname=user_data.lastname,
            hashed_password=hashed_pw,
            role=user_data.role
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update_user(
            self, 
            user_id: int, 
            user_update: UserUpdate, 
            current_user: User
        ) -> User | None:
        user = self.get_user_by_id(user_id)
        if not user: 
            return None
        
        Permissions.require_admin_or_owner(user_id, current_user)
        update_data = user_update.model_dump(exclude_unset=True)

        if 'role' in update_data and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can update user roles"
            )
        
        for key, value in update_data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete_user(
            self, 
            user_id: int,
            current_user: User
        ) -> User | None:
        user = self.get_user_by_id(user_id, current_user) # This already has Permissions Check
        if not user: 
            return None
        self.db.delete(user)
        self.db.commit()
        return user






    