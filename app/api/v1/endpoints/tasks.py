from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.models.task import TaskStatus

router = APIRouter()

@router.get("/", response_model=List[schemas.Task])
def read_tasks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve tasks.
    """
    if crud.user.is_superuser(current_user):
        tasks = crud.task.get_multi(db, skip=skip, limit=limit)
    else:
        tasks = crud.task.get_user_tasks(
            db, user_id=current_user.id, skip=skip, limit=limit
        )
    return tasks

@router.post("/", response_model=schemas.Task)
def create_task(
    *,
    db: Session = Depends(deps.get_db),
    task_in: schemas.TaskCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new task.
    """
    task = crud.task.create(db, obj_in=task_in)
    return task

@router.put("/{task_id}", response_model=schemas.Task)
def update_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: int,
    task_in: schemas.TaskUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update task.
    """
    task = crud.task.get(db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not crud.user.is_superuser(current_user) and task.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    task = crud.task.update(db, db_obj=task, obj_in=task_in)
    return task

@router.get("/{task_id}", response_model=schemas.Task)
def read_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get task by ID.
    """
    task = crud.task.get(db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not crud.user.is_superuser(current_user) and task.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return task

@router.delete("/{task_id}", response_model=schemas.Task)
def delete_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete task.
    """
    task = crud.task.get(db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not crud.user.is_superuser(current_user) and task.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    task = crud.task.remove(db, id=task_id)
    return task

@router.post("/{task_id}/start", response_model=schemas.Task)
def start_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Start a task.
    """
    task = crud.task.get(db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not crud.user.is_superuser(current_user) and task.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    if task.status != TaskStatus.PENDING:
        raise HTTPException(status_code=400, detail="Task is not in pending status")
    
    # TODO: Add task to Celery queue
    task = crud.task.update_task_status(db, task_id=task_id, status=TaskStatus.RUNNING)
    return task
