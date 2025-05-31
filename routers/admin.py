from typing import Annotated
from fastapi import APIRouter,  Depends, HTTPException, Path
from starlette import status

from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from .auth import get_current_user
import models
from database import SessionLocal


router = APIRouter(
    prefix = '/admin',
    tags = ['admin']
)


# Pydantic request model
class TodoRequest(BaseModel):
    title: str = Field(min_length = 3)
    description: str = Field(min_length = 3, max_length = 100)
    priority: int = Field(gt = 0, lt = 6)
    complete: bool



# opening the connection, process the request and close the connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# dependency injections
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


###   Endpoints   ###

@router.get("/todo", status_code = status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin' :
        raise HTTPException(status_code = 401, detail = "Authentication Failed")
    
    return db.query(models.Todos).all()


@router.delete("/delete/{todo_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt = 0)):

    if user is None or user.get('user_role') != 'admin' :
        raise HTTPException(status_code = 401, detail = "Authentication Failed")

    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code = 404, detail = 'Todo not Found')
    
    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()

