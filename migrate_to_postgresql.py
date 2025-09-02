#!/usr/bin/env python3
"""
Migration script to handle transition from SQLite to PostgreSQL
This script will help migrate data and ensure compatibility
"""

import os
import sys
import json
from datetime import datetime

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from database import engine, Base, SessionLocal, test_connection, init_db
from models import Admin, User, Product, UserFavourite, Session, Feedback

def migrate_data_from_sqlite():
    """Migrate data from SQLite to PostgreSQL if needed"""
    print("🔄 Checking if migration is needed...")
    
    # Check if we're using PostgreSQL
    if not os.getenv("DATABASE_URL"):
        print("ℹ️  Using SQLite locally - no migration needed")
        return True
    
    try:
        # Test PostgreSQL connection
        if not test_connection():
            print("❌ Cannot connect to PostgreSQL database")
            return False
        
        # Initialize tables
        if not init_db():
            print("❌ Failed to initialize PostgreSQL tables")
            return False
        
        print("✅ PostgreSQL database initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False

def create_sample_data():
    """Create sample data for testing"""
    print("📝 Creating sample data...")
    
    try:
        db = SessionLocal()
        
        # Check if admin exists
        existing_admin = db.query(Admin).first()
        if not existing_admin:
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            
            admin = Admin(
                username="JuberSiddique",
                password=pwd_context.hash("Juber@708492")
            )
            db.add(admin)
            print("✅ Created admin user")
        
        # Check if products exist
        existing_products = db.query(Product).first()
        if not existing_products:
            sample_products = [
                {
                    "name": "Nike Air Max 270",
                    "description": "Comfortable running shoes with excellent cushioning.",
                    "price": 129.99,
                    "category": "Sports",
                    "status": "Available",
                    "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
                },
                {
                    "name": "Adidas Ultraboost 22",
                    "description": "Premium running shoes with responsive Boost midsole.",
                    "price": 179.99,
                    "category": "Sports",
                    "status": "Available",
                    "image_url": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
                }
            ]
            
            for product_data in sample_products:
                product = Product(**product_data)
                db.add(product)
            
            print("✅ Created sample products")
        
        db.commit()
        print("✅ Sample data created successfully")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
        return False
    finally:
        db.close()
    
    return True

def main():
    """Main migration function"""
    print("🚀 PostgreSQL Migration Script for Jubair Boot House")
    print("=" * 60)
    
    # Step 1: Migrate database structure
    if not migrate_data_from_sqlite():
        print("❌ Database migration failed")
        sys.exit(1)
    
    # Step 2: Create sample data
    if not create_sample_data():
        print("❌ Sample data creation failed")
        sys.exit(1)
    
    print("=" * 60)
    print("🎉 Migration completed successfully!")
    print("📝 Your app is now ready to use with PostgreSQL")
    
    # Show database info
    if os.getenv("DATABASE_URL"):
        print("🌐 Database: PostgreSQL (Production)")
    else:
        print("💻 Database: SQLite (Local Development)")

if __name__ == "__main__":
    main()
