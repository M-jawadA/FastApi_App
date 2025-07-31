from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from db.database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

    todos = relationship("Todo", back_populates="user")  # Ensure it matches the relationship in Todo

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return pwd_context.hash(password)
