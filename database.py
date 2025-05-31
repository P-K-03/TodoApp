from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# URL to create a location of database
SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db" 

# Create an engine for our database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base = declarative_base()           #an object of database