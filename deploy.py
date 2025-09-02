#!/usr/bin/env python3
"""
Deployment Script for Jubair Boot House
This script handles the complete deployment process including database initialization.
"""

import os
import sys
import subprocess
import time

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"{description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{description} failed!")
        print(f"   Error: {e.stderr.strip()}")
        return False

def check_requirements():
    """Check if all requirements are installed"""
    print("Checking requirements...")
    
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import jinja2
        import passlib
        print("All required packages are installed")
        return True
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def initialize_database():
    """Initialize the database"""
    print("Initializing database...")
    
    try:
        # Run the database initialization script
        result = subprocess.run([sys.executable, "init_database.py"], 
                              capture_output=True, text=True, check=True)
        print("Database initialization completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Database initialization failed!")
        print(f"   Error: {e.stderr.strip()}")
        return False

def verify_deployment():
    """Verify that the application can start"""
    print("Verifying deployment...")
    
    try:
        # Test if the app can be imported
        result = subprocess.run([sys.executable, "-c", "from app.main import app; print('App imported successfully')"], 
                              capture_output=True, text=True, check=True)
        print("Application verification passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Application verification failed!")
        print(f"   Error: {e.stderr.strip()}")
        return False

def main():
    """Main deployment function"""
    print("Starting Jubair Boot House Deployment...")
    print("=" * 50)
    
    # Step 1: Check requirements
    if not check_requirements():
        print("Requirements check failed. Please install missing packages.")
        sys.exit(1)
    
    # Step 2: Initialize database
    if not initialize_database():
        print("Database initialization failed. Please check the error messages above.")
        sys.exit(1)
    
    # Step 3: Verify deployment
    if not verify_deployment():
        print("Deployment verification failed. Please check the error messages above.")
        sys.exit(1)
    
    print("=" * 50)
    print("Deployment completed successfully!")
    print("Your application is ready to run:")
    print("   - Database: Initialized with all tables and sample data")
    print("   - Admin User: Created (JuberSiddique / Juber@708492)")
    print("   - Application: Verified and ready")
    print("")
    print("To start the application, run:")
    print("   python run.py")
    print("")
    print("Then visit: http://localhost:8000")

if __name__ == "__main__":
    main()