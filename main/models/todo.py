from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))  # Add ForeignKey to link with User
    user = relationship("User", back_populates="todos")
