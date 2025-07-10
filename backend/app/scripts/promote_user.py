# scripts/promote_user.py

from app.core.db import SessionLocal
from app.models.user import User, UserRole

def promote_user_to_admin(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        print(f"User with ID {user_id} not found.")
        return

    user.role = UserRole.ADMIN
    db.commit()
    print(f"User {user.username} promoted to admin.")

if __name__ == "__main__":
    promote_user_to_admin(2)
