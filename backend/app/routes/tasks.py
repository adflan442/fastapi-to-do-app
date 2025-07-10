from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.task import TaskResponse, TaskCreate, TaskUpdate
from app.db_ops.task import TaskService
from app.core.security import get_current_user
from app.core.db import get_db
from app.models.user import User

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

# ---------------------------------
# --------- GET ALL TASKS ---------
# ---------------------------------

@router.get("/", response_model=List[TaskResponse])
def read_tasks(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)):
    return TaskService(db).get_all_tasks(current_user, skip=skip, limit=limit)  # Replace user_id=1 with auth user id later

# ---------------------------------
# ---------- GET A TASK -----------
# ---------------------------------

@router.get("/{task_id}", response_model=TaskResponse)
def read_task(
    task_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return TaskService(db).get_task_by_id(task_id, current_user)

# ---------------------------------
# ------GET ALL USER TASKS --------
# ---------------------------------

@router.get("/user/{user_id}/", response_model=List[TaskResponse])
def read_user_tasks(
    user_id: int, 
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    return TaskService(db).get_tasks_by_user(user_id=user_id, current_user=current_user, skip=skip, limit=limit)
    
# ---------------------------------
# -------- CREATE A TASK ----------
# ---------------------------------

@router.post("/", response_model=TaskCreate, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return TaskService(db).create_task(task, user_id=current_user.id)

# ---------------------------------
# -------- UPDATE A TASK ----------
# ---------------------------------

@router.put("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK) # Want to return the Updated Task, incase App needs it.
def update_task(
    task_id: int, 
    task_update: TaskUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return TaskService(db).update_task(task_id, task_update, current_user)
   

# ---------------------------------
# -------- DELETE A TASK ----------
# ---------------------------------

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
    ):
    return TaskService(db).delete_task(task_id, current_user)



