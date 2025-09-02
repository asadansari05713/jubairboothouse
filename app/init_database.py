#!/usr/bin/env python3
"""
Database Initialization Script for Jubair Boot House
This script ensures the database is properly created and initialized during deployment.
"""

import sys
import os
import sqlite3
from datetime import datetime

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from database import engine, Base, SessionLocal
from models import Admin, User, Product, UserFavourite, Session, Feedback
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_database_tables():
    """Create all database tables"""
    try:
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("All database tables created successfully!")
        return True
    except Exception as e:
        print(f"Error creating database tables: {e}")
        return False

def verify_database_structure():
    """Verify that all required tables exist"""
    try:
        print("Verifying database structure...")
        
        # Connect to SQLite database directly
        conn = sqlite3.connect("jubair_boot_house.db")
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in cursor.fetchall()]
        
        required_tables = ["admins", "users", "products", "user_favourites", "sessions", "feedback"]
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            print(f"Missing tables: {missing_tables}")
            return False
        
        print("All required tables exist!")
        
        # Check table structures
        for table in required_tables:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            print(f"   {table}: {len(columns)} columns")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error verifying database structure: {e}")
        return False

def create_default_admin():
    """Create default admin user if none exists"""
    try:
        print("Checking for admin user...")
        
        db = SessionLocal()
        
        # Check if admin already exists
        existing_admin = db.query(Admin).first()
        if existing_admin:
            print(f"Admin user already exists: {existing_admin.username}")
            db.close()
            return True
        
        # Create default admin
        admin = Admin(
            username="JuberSiddique",
            password=pwd_context.hash("Juber@708492")
        )
        
        db.add(admin)
        db.commit()
        db.close()
        
        print("Default admin user created successfully!")
        print("Username: JuberSiddique")
        print("Password: Juber@708492")
        return True
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
        db.close()
        return False

def add_sample_products():
    """Add sample products if database is empty"""
    try:
        print("Checking for sample products...")
        
        db = SessionLocal()
        
        # Check if products already exist
        existing_count = db.query(Product).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} products")
            db.close()
            return True
        
        # Sample product data
        sample_products = [
            {
                "name": "Nike Air Max 270",
                "description": "Comfortable running shoes with excellent cushioning and breathable mesh upper.",
                "price": 129.99,
                "category": "Sports",
                "status": "Available",
                "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Adidas Ultraboost 22",
                "description": "Premium running shoes with responsive Boost midsole and Primeknit upper.",
                "price": 179.99,
                "category": "Sports",
                "status": "Available",
                "image_url": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Converse Chuck Taylor",
                "description": "Classic canvas sneakers perfect for casual wear and street style.",
                "price": 59.99,
                "category": "Casual",
                "status": "Available",
                "image_url": "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Dr. Martens 1460",
                "description": "Classic leather boots with air-cushioned sole and durable construction.",
                "price": 169.99,
                "category": "Boots",
                "status": "Available",
                "image_url": "https://images.unsplash.com/photo-1549298916-b41d501d3772?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Allen Edmonds Oxford",
                "description": "Premium leather dress shoes with Goodyear welt construction.",
                "price": 349.99,
                "category": "Formal",
                "status": "Available",
                "image_url": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            }
        ]
        
        # Add sample products
        for product_data in sample_products:
            product = Product(**product_data)
            db.add(product)
        
        db.commit()
        db.close()
        
        print(f"Successfully added {len(sample_products)} sample products!")
        return True
        
    except Exception as e:
        print(f"Error adding sample products: {e}")
        db.rollback()
        db.close()
        return False

def test_database_connection():
    """Test database connection and basic operations"""
    try:
        print("Testing database connection...")
        
        db = SessionLocal()
        
        # Test basic queries
        admin_count = db.query(Admin).count()
        user_count = db.query(User).count()
        product_count = db.query(Product).count()
        
        print("Database connection successful!")
        print(f"   Admins: {admin_count}")
        print(f"   Users: {user_count}")
        print(f"   Products: {product_count}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"Database connection test failed: {e}")
        return False

def main():
    """Main initialization function"""
    print("Initializing Jubair Boot House Database for Deployment...")
    print("=" * 60)
    
    # Step 1: Create database tables
    if not create_database_tables():
        print("Failed to create database tables. Exiting.")
        sys.exit(1)
    
    # Step 2: Verify database structure
    if not verify_database_structure():
        print("Database structure verification failed. Exiting.")
        sys.exit(1)
    
    # Step 3: Create default admin
    if not create_default_admin():
        print("Failed to create default admin. Exiting.")
        sys.exit(1)
    
    # Step 4: Add sample products
    if not add_sample_products():
        print("Failed to add sample products. Exiting.")
        sys.exit(1)
    
    # Step 5: Test database connection
    if not test_database_connection():
        print("Database connection test failed. Exiting.")
        sys.exit(1)
    
    print("=" * 60)
    print("Database initialization completed successfully!")
    print("Deployment ready:")
    print("   - All tables created")
    print("   - Default admin user: JuberSiddique / Juber@708492")
    print("   - Sample products added")
    print("   - Database connection verified")
    print("You can now deploy the application!")

if __name__ == "__main__":
    main()