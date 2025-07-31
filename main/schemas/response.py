from typing import Optional, Any
from pydantic import BaseModel


class ResponseModel(BaseModel):
    status: int
    success: bool
    data: Any = None
    message: Optional[str] = None  # Optional field
    error: Optional[str] = None

    class Config:
        from_attributes = True  # Enables compatibility with SQLAlchemy
