from pydantic import BaseModel

class productDto(BaseModel):
    id: int
    name: str
    price: float
    description: str