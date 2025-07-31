from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.todo import Todo
from schemas.todo import TodoCreate, TodoResponse
from schemas.response import ResponseModel
from utils.utils import get_db
from Services.auth import get_current_user  # Import authentication dependency

router = APIRouter()

@router.post("/todos/")
def create_todo(todo: TodoCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Create a new To-Do item for the authenticated user."""
    db_todo = Todo(title=todo.title, description=todo.description, user_id=user.id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    response = ResponseModel(status=201, success=True, data=TodoResponse.model_validate(db_todo))
    return response.model_dump(exclude_unset=True, exclude_none=True)
@router.get("/todos/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Retrieve a To-Do item by ID for the authenticated user."""
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="To-Do not found")

    response = ResponseModel(status=200, success=True, data=TodoResponse.model_validate(todo))
    return response.model_dump(exclude_unset=True, exclude_none=True)
@router.get("/todos/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Retrieve a To-Do item by ID for the authenticated user."""
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="To-Do not found")

    response = ResponseModel(status=200, success=True, data=TodoResponse.model_validate(todo))
    return response.model_dump(exclude_unset=True, exclude_none=True)

@router.get("/todos/")
def get_all_todos(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Retrieve all To-Do items for the authenticated user."""
    todos = db.query(Todo).filter(Todo.user_id == user.id).all()

    response = ResponseModel(
        status=200,
        success=True,
        data=[TodoResponse.model_validate(todo) for todo in todos],
    )
    return response.model_dump(exclude_unset=True, exclude_none=True)


@router.patch("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: TodoCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Update a To-Do item for the authenticated user."""
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user.id).first()
    
    if not db_todo:
        raise HTTPException(status_code=404, detail="To-Do not found")

    db_todo.title = updated_todo.title
    db_todo.description = updated_todo.description
    db.commit()
    db.refresh(db_todo)

    response = ResponseModel(status=200, success=True, message="To-Do updated successfully", data=TodoResponse.model_validate(db_todo))
    return response.model_dump(exclude_unset=True, exclude_none=True)








