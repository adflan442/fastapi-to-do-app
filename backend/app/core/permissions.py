from fastapi import HTTPException, status
from app.models.user import User, UserRole

class Permissions:
    @staticmethod
    def is_admin(current_user: User) -> bool:
        if not isinstance(current_user, User):
            raise TypeError(f"Expected User Instance, got {type(current_user).__name__}")
        return current_user.role == UserRole.ADMIN
    
    @staticmethod
    def is_owner(resource_owner_id: int, current_user: User) -> bool:
        return resource_owner_id == current_user.id
    
    @staticmethod
    def require_admin(current_user: User) -> None:
        if not Permissions.is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin privileges required"
            )
    
    @staticmethod
    def require_owner(resource_owner_id: int, current_user: User) -> None:
        if not Permissions.is_owner(resource_owner_id, current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )
    
    @staticmethod
    def require_admin_or_owner(resource_owner_id: int, current_user: User) -> None:
        if not (Permissions.is_admin(current_user) or Permissions.is_owner(resource_owner_id, current_user)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )