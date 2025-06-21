from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """
    Retrieve a paginated list of tasks for a specific user.

    Parameters:
    - db: Database Session
    - user_id: ID of the user whose tasks to fetch
    - skip: Number of tasks to skip (offset) for pagination
    - limit: Maximum number of tasks to return (default 100)

    Returns:
    - List of Task objects for the user

    Notes:
    - `skip` (offset) is used to skip a number of records, useful for pagination.
    - `limit` caps the number of records returned to avoid overloading responses.
    """
    # Query tasks for the user with pagination support
    return db.query(Task).filter(Task.user_id == user_id).offset(skip).limit(limit).all()


def create_task(db: Session, task: TaskCreate, user_id: int):
    """
    Create a new task in the database for the given user.

    Parameters:
    - db: Database Session
    - task: TaskCreate Pydantic schema with task details
    - user_id: ID of the user who owns the task

    Returns:
    - The created Task object

    Notes:
    - `task.model_dump()` converts the Pydantic model into a dictionary.
    - The `**` operator unpacks this dictionary into keyword arguments for the SQLAlchemy Task constructor.
    - This is equivalent to calling:
      Task(title="...", details="...", status="...", priority="...", user_id=user_id)
    """
    db_task = Task(**task.model_dump(), user_id=user_id)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)  # Ensure the instance is refreshed with any DB defaults or triggers
    return db_task


def update_task(db: Session, task_id: int, task_update: TaskUpdate):
    """
    Update an existing task with new values; only updates fields that are provided by the user.

    Parameters:
    - db: Database Session
    - task_id: ID of the task to update
    - task_update: TaskUpdate Pydantic schema with updated fields (all optional).

    Returns:
    - The updated Task object, or None if the task can't be found.

    Notes:
    - `task_update.model_dump(exclude_unset=True)` returns a dictionary of only the fields explicitly set by the user.
    - Normally, `model_dump()` returns all fields including unset ones with default or None values.
    - Excluding unset fields avoids overwriting existing data with defaults or None.
    - The loop with `setattr(db_task, key, value)` dynamically updates attributes on the SQLAlchemy Task instance.
    """
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return None
    
    update_data = task_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)  # Refresh to get latest DB state
    return db_task

def delete_task(db: Session, task_id: int):
    """
    Delete an existing task from the database.

    Parameters: 
    - db: Database Session
    - task_id: The ID of the Task to delete

    Returns:
    - The deleted Task object, or None if the task can't be found.

    Notes:
    - No need to refresh the deleted task after deletion.
    - Calling `db.refresh()` after deletion would raise an error or be pointless.
    - The function returns the task object as it was before deletion.
    """
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return None
    
    db.delete(db_task)
    db.commit()
    return db_task

