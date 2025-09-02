# Jubair Boot House - Deployment Guide

## 🚀 Quick Deployment

### For New Deployments:
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run complete deployment (recommended)
python deploy.py

# 3. Start the application
python run.py
```

### For Existing Deployments:
```bash
# Just start the application (database will be auto-created if missing)
python run.py
```

## 📋 What the Deployment Script Does

The `deploy.py` script automatically:

1. **Checks Requirements**: Verifies all Python packages are installed
2. **Initializes Database**: Creates all required tables
3. **Creates Admin User**: Sets up default admin account
4. **Adds Sample Data**: Populates database with sample products
5. **Verifies Setup**: Tests that everything works correctly

## 🗄️ Database Setup

### Automatic Database Creation
- Database file: `jubair_boot_house.db` (SQLite)
- Tables are created automatically when the app starts
- No manual database setup required

### Database Tables Created:
- `admins` - Admin users
- `users` - Regular users  
- `products` - Product catalog
- `user_favourites` - User favorite products
- `sessions` - User sessions
- `feedback` - Contact form submissions

### Default Admin Credentials:
- **Username**: JuberSiddique
- **Password**: Juber@708492

## 🔧 Manual Database Initialization

If you need to manually initialize the database:

```bash
python init_database.py
```

This script will:
- Create all database tables
- Verify table structure
- Create default admin user
- Add sample products
- Test database connection

## 🚀 Production Deployment

### Using Gunicorn (Recommended for Production):

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run with Gunicorn:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker:

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python init_database.py

EXPOSE 8000
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### Using Nginx Reverse Proxy:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/your/app/static;
    }
}
```

## 🔍 Troubleshooting

### Database Issues:
- If database creation fails, run: `python init_database.py`
- Check file permissions for database file
- Ensure SQLite is available

### Import Errors:
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python path and virtual environment

### Port Issues:
- Default port is 8000
- Change port in `run.py` if needed
- Ensure port is not already in use

### Permission Issues:
- Ensure write permissions for database file
- Check uploads directory permissions
- Verify static file serving permissions

## 📁 File Structure After Deployment

```
jubair_boot_house/
├── app/                    # Application code
├── templates/             # HTML templates
├── static/               # Static files
├── jubair_boot_house.db  # SQLite database (created automatically)
├── init_database.py      # Database initialization script
├── deploy.py             # Complete deployment script
├── run.py                # Application startup script
└── requirements.txt      # Dependencies
```

## ✅ Verification Checklist

After deployment, verify:

- [ ] Application starts without errors
- [ ] Database file exists (`jubair_boot_house.db`)
- [ ] All tables are created (6 tables total)
- [ ] Admin user can login (JuberSiddique / Juber@708492)
- [ ] Sample products are visible
- [ ] Static files are served correctly
- [ ] Contact form works
- [ ] User registration works
- [ ] Product management works (admin)

## 🌐 Access Points

After successful deployment:

- **Main Site**: http://localhost:8000
- **Admin Login**: http://localhost:8000/auth/login
- **User Login**: http://localhost:8000/auth/user/login
- **API Documentation**: http://localhost:8000/docs
- **Admin Dashboard**: http://localhost:8000/products/admin/dashboard

## 📞 Support

If you encounter issues:

1. Check the console output for error messages
2. Verify all requirements are installed
3. Run `python init_database.py` to reset database
4. Check file permissions
5. Ensure port 8000 is available

---

**Jubair Boot House** - Ready for Production! 🚀
