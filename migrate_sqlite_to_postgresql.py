#!/usr/bin/env python3
"""
Comprehensive SQLite to PostgreSQL Migration Script for Jubair Boot House
This script will migrate all data from SQLite to PostgreSQL while preserving schemas and relationships.
"""

import os
import sys
import sqlite3
from datetime import datetime
import json

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def connect_sqlite():
    """Connect to existing SQLite database"""
    try:
        sqlite_path = "./jubair_boot_house.db"
        if not os.path.exists(sqlite_path):
            print(f"❌ SQLite database not found at: {sqlite_path}")
            return None
        
        conn = sqlite3.connect(sqlite_path)
        conn.row_factory = sqlite3.Row  # Enable row access by column name
        print(f"✅ Connected to SQLite database: {sqlite_path}")
        return conn
    except Exception as e:
        print(f"❌ Failed to connect to SQLite: {e}")
        return None

def connect_postgresql():
    """Connect to PostgreSQL database"""
    try:
        from app.database import engine, SessionLocal
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Connected to PostgreSQL database")
        
        return SessionLocal()
    except Exception as e:
        print(f"❌ Failed to connect to PostgreSQL: {e}")
        return None

def get_sqlite_tables(sqlite_conn):
    """Get list of tables from SQLite database"""
    try:
        cursor = sqlite_conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [row['name'] for row in cursor.fetchall()]
        print(f"📋 Found SQLite tables: {', '.join(tables)}")
        return tables
    except Exception as e:
        print(f"❌ Error getting SQLite tables: {e}")
        return []

def get_table_schema(sqlite_conn, table_name):
    """Get table schema from SQLite"""
    try:
        cursor = sqlite_conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        schema = {}
        for col in columns:
            schema[col['name']] = {
                'type': col['type'],
                'notnull': col['notnull'],
                'default': col['dflt_value'],
                'pk': col['pk']
            }
        return schema
    except Exception as e:
        print(f"❌ Error getting schema for {table_name}: {e}")
        return {}

def migrate_table_data(sqlite_conn, postgres_db, table_name, table_schema):
    """Migrate data from SQLite table to PostgreSQL"""
    try:
        print(f"🔄 Migrating table: {table_name}")
        
        # Get all data from SQLite table
        cursor = sqlite_conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        if not rows:
            print(f"   ℹ️  Table {table_name} is empty, skipping")
            return True
        
        print(f"   📊 Found {len(rows)} rows to migrate")
        
        # Import models dynamically
        from app.models import Admin, User, Product, UserFavourite, Session, Feedback
        
        model_map = {
            'admins': Admin,
            'users': User,
            'products': Product,
            'user_favourites': UserFavourite,
            'sessions': Session,
            'feedback': Feedback
        }
        
        if table_name not in model_map:
            print(f"   ⚠️  No model found for table {table_name}, skipping")
            return True
        
        Model = model_map[table_name]
        
        # Migrate each row
        migrated_count = 0
        for row in rows:
            try:
                # Convert row to dict
                row_dict = dict(row)
                
                # Handle data type conversions
                row_dict = convert_data_types(row_dict, table_schema)
                
                # Create model instance
                instance = Model(**row_dict)
                postgres_db.add(instance)
                migrated_count += 1
                
            except Exception as e:
                print(f"   ⚠️  Error migrating row {migrated_count + 1}: {e}")
                print(f"      Row data: {dict(row)}")
                continue
        
        # Commit the batch
        postgres_db.commit()
        print(f"   ✅ Successfully migrated {migrated_count}/{len(rows)} rows")
        return True
        
    except Exception as e:
        print(f"   ❌ Error migrating table {table_name}: {e}")
        postgres_db.rollback()
        return False

def convert_data_types(row_dict, table_schema):
    """Convert SQLite data types to PostgreSQL compatible types"""
    converted = {}
    
    for column, value in row_dict.items():
        if value is None:
            converted[column] = None
            continue
            
        if column in table_schema:
            col_type = table_schema[column]['type'].upper()
            
            if 'INTEGER' in col_type and column == 'is_active':
                # Convert SQLite integer (0/1) to PostgreSQL boolean
                converted[column] = bool(value)
            elif 'TEXT' in col_type and column in ['created_at', 'updated_at']:
                # Convert text timestamps to datetime objects
                try:
                    if isinstance(value, str) and value:
                        converted[column] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    else:
                        converted[column] = datetime.now()
                except:
                    converted[column] = datetime.now()
            elif 'TEXT' in col_type and column in ['images', 'sizes']:
                # Ensure JSON fields are valid
                if isinstance(value, str) and value:
                    try:
                        json.loads(value)
                        converted[column] = value
                    except:
                        converted[column] = '[]'
                else:
                    converted[column] = '[]'
            else:
                converted[column] = value
        else:
            converted[column] = value
    
    return converted

def verify_migration(sqlite_conn, postgres_db, table_name):
    """Verify that migration was successful by comparing row counts"""
    try:
        # Count rows in SQLite
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        sqlite_count = sqlite_cursor.fetchone()[0]
        
        # Count rows in PostgreSQL
        from app.models import Admin, User, Product, UserFavourite, Session, Feedback
        
        model_map = {
            'admins': Admin,
            'users': User,
            'products': Product,
            'user_favourites': UserFavourite,
            'sessions': Session,
            'feedback': Feedback
        }
        
        if table_name in model_map:
            postgres_count = postgres_db.query(model_map[table_name]).count()
            
            if sqlite_count == postgres_count:
                print(f"   ✅ Verification passed: {sqlite_count} rows in both databases")
                return True
            else:
                print(f"   ❌ Verification failed: SQLite={sqlite_count}, PostgreSQL={postgres_count}")
                return False
        else:
            print(f"   ⚠️  Cannot verify table {table_name} (no model)")
            return True
            
    except Exception as e:
        print(f"   ❌ Verification error: {e}")
        return False

def main():
    """Main migration function"""
    print("🚀 SQLite to PostgreSQL Migration Script for Jubair Boot House")
    print("=" * 70)
    
    # Check environment
    if not os.getenv("DATABASE_URL"):
        print("❌ DATABASE_URL environment variable not set!")
        print("   Please set DATABASE_URL to your PostgreSQL connection string")
        print("   Example: postgresql+psycopg2://username:password@host:port/dbname")
        sys.exit(1)
    
    # Connect to SQLite
    print("📡 Step 1: Connecting to SQLite database...")
    sqlite_conn = connect_sqlite()
    if not sqlite_conn:
        sys.exit(1)
    
    # Connect to PostgreSQL
    print("📡 Step 2: Connecting to PostgreSQL database...")
    postgres_db = connect_postgresql()
    if not postgres_db:
        sqlite_conn.close()
        sys.exit(1)
    
    try:
        # Get SQLite tables
        print("📋 Step 3: Analyzing SQLite database structure...")
        tables = get_sqlite_tables(sqlite_conn)
        if not tables:
            print("❌ No tables found in SQLite database")
            sys.exit(1)
        
        # Initialize PostgreSQL tables
        print("🏗️  Step 4: Initializing PostgreSQL tables...")
        from app.database import init_db
        if not init_db():
            print("❌ Failed to initialize PostgreSQL tables")
            sys.exit(1)
        
        # Migrate each table
        print("🔄 Step 5: Migrating data...")
        success_count = 0
        total_tables = len(tables)
        
        for table_name in tables:
            print(f"\n📊 Processing table: {table_name}")
            
            # Get table schema
            schema = get_table_schema(sqlite_conn, table_name)
            
            # Migrate table data
            if migrate_table_data(sqlite_conn, postgres_db, table_name, schema):
                # Verify migration
                if verify_migration(sqlite_conn, postgres_db, table_name):
                    success_count += 1
                else:
                    print(f"   ⚠️  Migration completed but verification failed for {table_name}")
            else:
                print(f"   ❌ Migration failed for {table_name}")
        
        # Final summary
        print("\n" + "=" * 70)
        print("🎉 Migration Summary")
        print("=" * 70)
        print(f"✅ Successfully migrated: {success_count}/{total_tables} tables")
        
        if success_count == total_tables:
            print("🎊 All tables migrated successfully!")
            print("🚀 Your Jubair Boot House is now running on PostgreSQL!")
        else:
            print("⚠️  Some tables failed to migrate. Check the logs above.")
        
        print("\n📝 Next steps:")
        print("   1. Restart your FastAPI application")
        print("   2. Test login/signup functionality")
        print("   3. Verify all data is accessible")
        
    except Exception as e:
        print(f"❌ Migration failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        # Clean up connections
        sqlite_conn.close()
        postgres_db.close()
        print("\n🔌 Database connections closed")

if __name__ == "__main__":
    main()
