#!/usr/bin/env python3
"""
Database setup script for Render deployment
Run this after your app is deployed to initialize the database
"""

import os
import sys

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def setup_render_database():
    """Set up database on Render"""
    print("🚀 Setting up Render database...")
    
    # Check if we're on Render
    if not os.getenv("DATABASE_URL"):
        print("❌ DATABASE_URL not found. Make sure you're running this on Render.")
        return False
    
    try:
        from database import test_connection, init_db
        from models import Admin, User, Product, UserFavourite, Session, Feedback
        
        print(f"🔗 Database URL: {os.getenv('DATABASE_URL')[:50]}...")
        
        # Test connection
        if not test_connection():
            print("❌ Cannot connect to database")
            return False
        
        # Initialize tables
        if not init_db():
            print("❌ Failed to initialize database tables")
            return False
        
        print("✅ Database tables created successfully")
        
        # Create admin user
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        from database import SessionLocal
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
            
            # Create sample products
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
        
        print("🎉 Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database setup error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if setup_render_database():
        print("✅ Your Jubair Boot House is ready on Render!")
        print("🔗 You can now login with:")
        print("   Username: JuberSiddique")
        print("   Password: Juber@708492")
    else:
        print("❌ Database setup failed")
        sys.exit(1)
