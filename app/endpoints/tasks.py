from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from ..db import session
from ..models.task import Task
from ..schemas.task import TaskModel, TaskCreate, TaskResponse, TaskUpdate
#typing import List
from fastapi import status

router = APIRouter()

@router.get("/", response_model=list[TaskModel])
def read_tasks(db: Session = Depends(session.get_db)):
    tasks = db.query(Task).all()
    return [{"id": task.id, "task": task.task} for task in tasks]

@router.get("/{task_id}", response_model=TaskModel)
def read_task(task_id: int = Path(..., title="The ID of the task to retrieve"), db: Session = Depends(session.get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskModel(id=task.id, task=task.task)

@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(session.get_db)):
    db_task = Task(task=task.task)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return TaskResponse(id=db_task.id, task=db_task.task)

@router.delete("/{task_id}", status_code=status.HTTP_200_OK) # new way to add status
def delete_task(task_id: int, db: Session = Depends(session.get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated_task: TaskUpdate, db: Session = Depends(session.get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.task = updated_task.task
    db.commit()
    db.refresh(task)
    return TaskResponse(id=task.id, task=task.task)
