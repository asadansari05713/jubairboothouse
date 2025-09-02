#!/usr/bin/env python3
"""
Simple database initialization script for Render
Run this after deployment to set up initial data
"""

import os
import sys

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def init_database():
    """Initialize database with basic data"""
    print("🚀 Initializing Jubair Boot House database...")
    
    try:
        from database import test_connection, SessionLocal
        from models import Admin, Product
        from passlib.context import CryptContext
        
        # Test connection
        if not test_connection():
            print("❌ Cannot connect to database")
            return False
        
        print("✅ Database connection successful")
        
        # Create password context
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Get database session
        db = SessionLocal()
        
        try:
            # Check if admin exists
            existing_admin = db.query(Admin).first()
            if not existing_admin:
                admin = Admin(
                    username="JuberSiddique",
                    password=pwd_context.hash("Juber@708492")
                )
                db.add(admin)
                db.commit()
                print("✅ Admin user created")
            else:
                print("ℹ️  Admin user already exists")
            
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
                
                db.commit()
                print("✅ Sample products created")
            else:
                print("ℹ️  Products already exist")
                
        finally:
            db.close()
        
        print("🎉 Database initialization completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if init_database():
        print("✅ Your Jubair Boot House is ready!")
        print("🔗 You can now login with:")
        print("   Username: JuberSiddique")
        print("   Password: Juber@708492")
    else:
        print("❌ Database initialization failed")
        sys.exit(1)
