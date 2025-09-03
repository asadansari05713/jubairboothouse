import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLite Database configuration - Local file-based, zero connection hassle
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine with SQLite-specific settings
engine = create_engine(DATABASE_URL) # Required for SQLite with FastAPI
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
