from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import StaticPool
import os
from datetime import datetime

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Configure database engine based on environment
if DATABASE_URL:
    # Production: Use PostgreSQL
    if DATABASE_URL.startswith("postgres://"):
        # Handle Render's postgres:// format
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # Ensure we're using psycopg2 driver
    if not DATABASE_URL.startswith("postgresql+psycopg2://"):
        if DATABASE_URL.startswith("postgresql://"):
            DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
    
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Enable connection health checks
        pool_recycle=300,    # Recycle connections every 5 minutes
        echo=False           # Set to True for SQL query logging in development
    )
    print(f"🔗 Connected to PostgreSQL database")
else:
    # Development: Use SQLite
    engine = create_engine(
        "sqlite:///./jubair_boot_house.db",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False
    )
    print(f"🔗 Connected to SQLite database (local development)")

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test database connection
def test_connection():
    try:
        with engine.connect() as conn:
            # Use text() for raw SQL to avoid deprecation warnings
            from sqlalchemy import text
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

# Initialize database tables - this will be called on app startup
def init_db():
    try:
        # Import all models to ensure they're registered with Base
        from app.models import Admin, User, Product, UserFavourite, Session, Feedback
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/verified successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create database tables: {e}")
        return False

# Create tables on module import (ensures tables exist when app starts)
try:
    init_db()
except Exception as e:
    print(f"⚠️  Database initialization warning: {e}")
    # Don't fail the app startup if database is not available
    pass
