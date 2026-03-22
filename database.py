from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from typing import Generator
from fastapi import HTTPException
import os

# Create database engine
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise HTTPException(status_code=500, detail="DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base model
Base = declarative_base()

# Dependency to get database session
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Initialize database on startup
init_db()