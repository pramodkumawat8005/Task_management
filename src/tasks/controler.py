
from sqlalchemy.orm import Session
from src.tasks.dtos import TaskSchema
from src.tasks.model import TaskModel
from src.user.model import UserModel
from fastapi import HTTPException

def create_task(body: TaskSchema, db: Session, user: UserModel):
    data = body.model_dump()
    new_task = TaskModel(title=data['title'],
                          description=data['description'],
                          completed=data['is_completed'],
                          user_id = user.id
                            )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_task(db: Session, user: UserModel):
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user.id).all()
    return tasks

def get_one_task(task_id: int, db: Session, user: UserModel):
    one_task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == user.id).first()
    if not one_task:
        raise HTTPException(status_code=404, detail="Task_id not found")
    return one_task

def update_task(task_id: int, body: TaskSchema, db: Session, user: UserModel):
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(status_code=404, detail="Task_id not found")
    if one_task.user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this task") 
    data = body.model_dump()
    for key, value in data.items():
        setattr(one_task, key, value)
    db.commit()
    db.refresh(one_task)
    return one_task

def delete_task(task_id: int, db: Session, user: UserModel):
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(status_code=404, detail="Task_id not found")
    if one_task.user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this task")
    db.delete(one_task)
    db.commit()
    return None