from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    description: str

class TodoCreate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int

    class Config:
        from_attributes = True  # Ensures SQLAlchemy ORM compatibility
