from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter,  Depends, HTTPException, Path
from starlette import status

from passlib.context import CryptContext
from pydantic import BaseModel, Field

from .auth import get_current_user
import models
from database import SessionLocal


router = APIRouter(
    prefix = '/user',
    tags = ['user']
)


# Pydantic request model
class UserRequest(BaseModel):
    username: str
    email: str
    first_name : str
    last_name : str
    password: str
    role: str
    phone_number: str

class UserVerification(BaseModel):
    password : str
    new_password: str = Field(min_length = 6)


def get_db():
    # opening the connection, process the request and close the connection
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

 # dependency injections to check if the user is authenticated
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

###   Endpoints ###

@router.get("/", status_code = status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    
    return  db.query(models.Users).filter(models.Users.id == user.get('id')).first()


@router.put("/change_password", status_code = status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification : UserVerification):
    if user is None:
        raise HTTPException(status_code = 401, detail = "Authentication Failed")
    
    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code = 401, detail = "Error on password change")
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


@router.put("/add_phone_number/{phone_number}", status_code = status.HTTP_204_NO_CONTENT)
async def add_phone_number(user: user_dependency, db : db_dependency, phone_number: int):
    if user is None:
        raise HTTPException(status_code = 401, detail = "Authentication Failed")
    
    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
   
    
    