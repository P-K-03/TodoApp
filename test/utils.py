from fastapi.testclient import TestClient

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest

from models import Todos, Users
from database import Base
from main import app
from routers.auth import bcrypt_context

#Test database uses sqlite3
SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass = StaticPool
)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base.metadata.create_all(bind = engine)

# get mock db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# get mock user
def override_get_current_user():
    return {'username': 'admin', 'id' : 1, 'user_role' : 'admin'}


client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title = 'learn to code',
        description = "Need to learn everyday",
        priority = 5,
        complete = False,
        owner_id = 1 
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    # After the test has ran , the db  is emptied
    with engine.connect() as connection:
        connection.execute(text("Delete FROM todos;"))
        connection.commit()

@pytest.fixture
def test_user():
    user = Users(
        username = 'user',
        email = "user@user.com",
        first_name = "user",
        last_name = "user",
        hashed_password =  bcrypt_context.hash("user"),
        role = "admin",
        phone_number = 111111111
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()