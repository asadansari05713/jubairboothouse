# 🚀 SQLite to PostgreSQL Migration Guide for Jubair Boot House

This guide will help you migrate your FastAPI application from SQLite to PostgreSQL while preserving all your existing data.

## 📋 **Prerequisites**

- **Existing SQLite database**: `jubair_boot_house.db`
- **PostgreSQL database**: Set up and accessible
- **Environment variable**: `DATABASE_URL` configured
- **Python packages**: `psycopg2-binary` installed

## 🔧 **Step-by-Step Migration Process**

### **Step 1: Prepare Your Environment**

1. **Install PostgreSQL dependencies:**
   ```bash
   pip install psycopg2-binary
   ```

2. **Set your PostgreSQL connection string:**
   ```bash
   # Linux/Mac
   export DATABASE_URL="postgresql+psycopg2://username:password@host:port/dbname"
   
   # Windows
   set DATABASE_URL=postgresql+psycopg2://username:password@host:port/dbname
   ```

3. **Verify your SQLite database exists:**
   ```bash
   ls -la jubair_boot_house.db
   ```

### **Step 2: Run the Migration Script**

1. **Execute the migration script:**
   ```bash
   python migrate_sqlite_to_postgresql.py
   ```

2. **Monitor the migration process:**
   - The script will analyze your SQLite database
   - Create PostgreSQL tables with proper schemas
   - Migrate all data while preserving relationships
   - Verify data integrity after migration

3. **Expected output:**
   ```
   🚀 SQLite to PostgreSQL Migration Script for Jubair Boot House
   ======================================================================
   📡 Step 1: Connecting to SQLite database...
   ✅ Connected to SQLite database: ./jubair_boot_house.db
   📡 Step 2: Connecting to PostgreSQL database...
   ✅ Connected to PostgreSQL database
   📋 Step 3: Analyzing SQLite database structure...
   📋 Found SQLite tables: admins, users, products, user_favourites, sessions, feedback
   🏗️  Step 4: Initializing PostgreSQL tables...
   ✅ Database tables created/verified successfully!
   🔄 Step 5: Migrating data...
   
   📊 Processing table: admins
   🔄 Migrating table: admins
      📊 Found 1 rows to migrate
      ✅ Successfully migrated 1/1 rows
      ✅ Verification passed: 1 rows in both databases
   
   📊 Processing table: users
   🔄 Migrating table: users
      📊 Found 5 rows to migrate
      ✅ Successfully migrated 5/5 rows
      ✅ Verification passed: 5 rows in both databases
   
   ... (continues for all tables)
   
   ======================================================================
   🎉 Migration Summary
   ======================================================================
   ✅ Successfully migrated: 6/6 tables
   🎊 All tables migrated successfully!
   🚀 Your Jubair Boot House is now running on PostgreSQL!
   ```

### **Step 3: Verify Migration Success**

1. **Check the health endpoint:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Expected response:**
   ```json
   {
     "status": "healthy",
     "database": {
       "type": "PostgreSQL",
       "status": "connected"
     },
     "environment": "production",
     "app": "Jubair Boot House",
     "version": "1.0.0"
   }
   ```

3. **Test your application:**
   - Login with existing credentials
   - Browse products
   - Check admin dashboard
   - Verify all functionality works

## 🗄️ **What Gets Migrated**

### **Tables and Data:**
- ✅ **admins**: Admin users with credentials
- ✅ **users**: Regular user accounts
- ✅ **products**: Product catalog with images and sizes
- ✅ **user_favourites**: User favorite products
- ✅ **sessions**: Active user sessions
- ✅ **feedback**: Contact form submissions

### **Data Type Conversions:**
- **Timestamps**: SQLite text → PostgreSQL DateTime
- **Booleans**: SQLite integer (0/1) → PostgreSQL Boolean
- **JSON Fields**: Preserved as-is with validation
- **Relationships**: Foreign keys and constraints maintained

### **Schema Preservation:**
- **Primary Keys**: Auto-incrementing IDs preserved
- **Foreign Keys**: Relationships between tables maintained
- **Indexes**: Database performance optimized
- **Constraints**: Data integrity rules applied

## 🔍 **Troubleshooting Migration Issues**

### **Common Problems:**

1. **Connection Failed:**
   ```
   ❌ Failed to connect to PostgreSQL
   ```
   **Solution:** Check your `DATABASE_URL` format and database accessibility

2. **Table Creation Failed:**
   ```
   ❌ Failed to initialize PostgreSQL tables
   ```
   **Solution:** Ensure PostgreSQL user has CREATE TABLE permissions

3. **Data Type Conversion Errors:**
   ```
   ⚠️  Error migrating row X: ...
   ```
   **Solution:** Check the specific row data and adjust conversion logic

4. **Verification Failed:**
   ```
   ❌ Verification failed: SQLite=X, PostgreSQL=Y
   ```
   **Solution:** Some rows may have failed migration, check logs

### **Debug Steps:**

1. **Check PostgreSQL logs:**
   ```bash
   # View PostgreSQL server logs
   tail -f /var/log/postgresql/postgresql-*.log
   ```

2. **Verify database permissions:**
   ```sql
   -- Connect to PostgreSQL and check user permissions
   \du
   \l
   ```

3. **Test connection manually:**
   ```bash
   psql "postgresql://username:password@host:port/dbname"
   ```

## 🚀 **Post-Migration Steps**

### **1. Update Environment Variables:**
   ```bash
   # Production environment
   export DATABASE_URL="postgresql+psycopg2://username:password@host:port/dbname"
   export ENVIRONMENT="production"
   export DEBUG="false"
   ```

### **2. Restart Your Application:**
   ```bash
   # Stop current app
   pkill -f "uvicorn\|gunicorn"
   
   # Start with new database
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

### **3. Verify All Functionality:**
   - ✅ User registration and login
   - ✅ Admin dashboard access
   - ✅ Product management
   - ✅ User favorites
   - ✅ Session management

### **4. Monitor Performance:**
   - Check response times
   - Monitor database connections
   - Verify data consistency

## 🔄 **Rollback Plan (If Needed)**

### **Quick Rollback:**
1. **Remove DATABASE_URL environment variable:**
   ```bash
   unset DATABASE_URL
   ```

2. **Restart application:**
   ```bash
   # App will automatically use SQLite again
   python -m uvicorn app.main:app --reload
   ```

### **Full Rollback:**
1. **Restore from SQLite backup:**
   ```bash
   cp jubair_boot_house.db.backup jubair_boot_house.db
   ```

2. **Remove PostgreSQL tables:**
   ```sql
   DROP SCHEMA public CASCADE;
   CREATE SCHEMA public;
   ```

## 📊 **Migration Validation Checklist**

- [ ] **Pre-Migration:**
  - [ ] SQLite database exists and is accessible
  - [ ] PostgreSQL database is set up
  - [ ] DATABASE_URL environment variable is set
  - [ ] All required packages are installed

- [ ] **During Migration:**
  - [ ] Migration script runs without errors
  - [ ] All tables are created successfully
  - [ ] All data is migrated
  - [ ] Row counts match between databases

- [ ] **Post-Migration:**
  - [ ] Application starts successfully
  - [ ] Health endpoint shows PostgreSQL connected
  - [ ] All functionality works as expected
  - [ ] Performance is acceptable

## 🎯 **Success Criteria**

Your migration is successful when:
- ✅ All SQLite data is present in PostgreSQL
- ✅ Application functions identically to before
- ✅ Database performance is maintained or improved
- ✅ No data loss or corruption occurred
- ✅ All relationships and constraints are preserved

## 🚨 **Important Notes**

### **Backup Your Data:**
```bash
# Always backup before migration
cp jubair_boot_house.db jubair_boot_house.db.backup
```

### **Test in Staging:**
- Test migration on a copy of your data first
- Verify all functionality works before production migration
- Have a rollback plan ready

### **Monitor After Migration:**
- Watch for any performance issues
- Check error logs for database-related problems
- Verify data consistency over time

---

**🎉 Congratulations! You've successfully migrated to PostgreSQL!**

Your Jubair Boot House is now running on a production-ready PostgreSQL database with all your existing data preserved and enhanced functionality.
