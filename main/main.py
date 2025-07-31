from fastapi import FastAPI
from Routes.todos import router as todo_router
from db.database import engine, Base
import models.todo  # Import models
import models.user  
from Routes.auth import router as auth_router
# print("Before table creation:", Base.metadata.tables.keys())  # Debug print

# Create tables
Base.metadata.create_all(bind=engine)

# print("After table creation:", Base.metadata.tables.keys())  # Debug print

app = FastAPI()

app.include_router(todo_router)
app.include_router(auth_router)
