from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from app.core.permissions import *
from fastapi import HTTPException, status

class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def get_task_by_id(self, task_id: int, current_user: User) -> Task:
        db_task = self.db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Can't find any task with id - {task_id}"
            )
        Permissions.require_admin_or_owner(db_task.user_id, current_user)
        return db_task
    
    def get_all_tasks(self, current_user: User, skip: int = 0, limit: int = 100) -> list[Task] | None:
        Permissions.require_admin(current_user)
        return self.db.query(Task).offset(skip).limit(limit).all()
    
    def get_tasks_by_user(
        self, 
        user_id: int, 
        current_user: User,
        skip: int = 0, 
        limit: int = 100
    ) -> list[Task] | None:
        
        Permissions.require_admin_or_owner(user_id, current_user)
        return (
            self.db.query(Task)
            .filter(Task.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_task(self, task: TaskCreate, user_id: int):
        db_task = Task(**task.model_dump(), user_id=user_id)
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task
    
    def update_task(self, task_id: int, task_update: TaskUpdate, current_user: User) -> Task | None:
        db_task = self.get_task_by_id(task_id, current_user)

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="We can't found this task in our system"
            )
        
        Permissions.require_owner(db_task.user_id, current_user)
        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete_task(self, task_id: int, current_user: User) -> Task | None:
        db_task = self.get_task_by_id(task_id, current_user)

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="We can't found this task in our system"
            )
        Permissions.require_admin_or_owner(db_task.user_id, current_user)
        self.db.delete(db_task)
        self.db.commit()
        return db_task
    

