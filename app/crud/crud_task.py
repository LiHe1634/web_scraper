from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.crud.base import CRUDBase
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate

class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def get_by_status(
        self, db: Session, *, status: TaskStatus, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        return (
            db.query(self.model)
            .filter(Task.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_pending_tasks(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        return (
            db.query(self.model)
            .filter(Task.status == TaskStatus.PENDING)
            .filter(Task.next_run <= datetime.utcnow())
            .order_by(Task.priority.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_user_tasks(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        return (
            db.query(self.model)
            .filter(Task.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_task_status(
        self, 
        db: Session,
        *,
        task_id: int,
        status: TaskStatus,
        error_message: Optional[str] = None
    ) -> Task:
        task = self.get(db, id=task_id)
        if not task:
            return None
            
        update_data = {"status": status}
        if status == TaskStatus.FAILED and error_message:
            update_data["error_message"] = error_message
            update_data["retry_count"] = task.retry_count + 1
            
        if status == TaskStatus.COMPLETED:
            update_data["last_run"] = datetime.utcnow()
            
        return self.update(db, db_obj=task, obj_in=update_data)

task = CRUDTask(Task)
