from pydantic import BaseModel

class TaskSchema(BaseModel):
    title: str
    description: str
    is_completed: bool = False

class TaskResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    completed: bool   
    user_id: int | None = 0