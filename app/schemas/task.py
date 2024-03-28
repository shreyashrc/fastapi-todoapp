from pydantic import BaseModel

class TaskModel(BaseModel):
    id: int
    task: str

class TaskCreate(BaseModel):
    task: str

class TaskResponse(BaseModel):
    id: int
    task: str

class TaskUpdate(BaseModel):
    task: str
