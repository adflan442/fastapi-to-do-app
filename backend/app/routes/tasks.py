from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from schemas import task as schema_task
from db_ops import task as db_ops_task
from core.security import get_current_user
from core.db import get_db


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.post("/", response_model=schema_task.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schema_task.TaskCreate, db: Session = Depends(get_db)):
    user_id = 1
    return db_ops_task.create_task(db, task, user_id)


@router.get("/", response_model=List[schema_task.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = db_ops_task.get_tasks_by_user(db, user_id=1, skip=skip, limit=limit)  # Replace user_id=1 with auth user id later
    return tasks

@router.get("/{task_id}", response_model=schema_task.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db_ops_task.get_task_by_id(db, task_id)
    return task

@router.put("/{task_id}", response_model=schema_task.Task)
def update_task(task_id: int, task_update: schema_task.TaskUpdate, db: Session = Depends(get_db)):
    user_id = 1
    db_task = db_ops_task.get_task_by_id(db, task_id)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found, Task ID: {task_id}"
        )
    
    updated_task = db_ops_task.update_task(db, task_id, task_update)
    return updated_task

@router.delete("/{task_id}", response_model=schema_task.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db_ops_task.get_task_by_id(db, task_id)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found, has it been already deleted? Task ID: {task_id}"
        )
    
    deleted_task = db_ops_task.delete_task(db, task_id)
    return deleted_task



