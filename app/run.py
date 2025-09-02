#!/usr/bin/env python3
"""
Jubair Boot House - Startup Script
Run this script to start the FastAPI application
"""

import uvicorn
import os
import sys
import sqlite3

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def check_database():
    """Check if database exists and is accessible"""
    try:
        # Check if database file exists
        if not os.path.exists("jubair_boot_house.db"):
            print("Database file not found. Creating database...")
            # Import and run database initialization
            from database import engine, Base
            Base.metadata.create_all(bind=engine)
            print("Database created successfully")
        
        # Test database connection
        conn = sqlite3.connect("jubair_boot_house.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()
        
        if len(tables) == 0:
            print("Database tables not found. Initializing...")
            from database import engine, Base
            Base.metadata.create_all(bind=engine)
            print("Database tables created successfully")
        
        print("Database is ready")
        return True
        
    except Exception as e:
        print(f"Database check failed: {e}")
        return False

if __name__ == "__main__":
    print("Starting Jubair Boot House...")
    print("Application will be available at: http://localhost:8000")
    print("Admin login: http://localhost:8000/auth/login")
    print("API docs: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Check database before starting
    if not check_database():
        print("Database initialization failed. Please run: python init_database.py")
        sys.exit(1)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nShutting down Jubair Boot House...")
    except Exception as e:
        print(f"Error starting application: {e}")
        print("Make sure you have:")
        print("   1. Installed requirements: pip install -r requirements.txt")
        print("   2. Database is properly initialized")
        print("   3. Run: python init_database.py if needed")
        sys.exit(1)
