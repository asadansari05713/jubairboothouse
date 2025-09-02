# 🚀 Render Deployment Guide with PostgreSQL

This guide will help you deploy your Jubair Boot House website on Render with PostgreSQL database.

## 📋 Prerequisites

- **GitHub repository** with your code
- **Render account** (free tier available)
- **Python 3.11+** knowledge

## 🏗️ Step-by-Step Deployment

### **Step 1: Prepare Your Repository**

1. **Push your updated code to GitHub:**
   ```bash
   git add .
   git commit -m "Add PostgreSQL support for Render deployment"
   git push origin main
   ```

2. **Ensure these files are in your repository:**
   - ✅ `requirements-prod.txt` (with psycopg2-binary)
   - ✅ `gunicorn.conf.py`
   - ✅ `render.yaml`
   - ✅ `app/` directory with all your code

### **Step 2: Deploy on Render**

1. **Go to [render.com](https://render.com) and sign up/login**

2. **Click "New +" and select "Web Service"**

3. **Connect your GitHub repository:**
   - Select your `jubair_boot_house` repository
   - Choose the `main` branch

4. **Configure your web service:**
   - **Name**: `jubair-boot-house`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main`

5. **Build & Deploy Settings:**
   - **Build Command**: `pip install -r requirements-prod.txt`
   - **Start Command**: `gunicorn -c gunicorn.conf.py app.main:app`

6. **Click "Create Web Service"**

### **Step 3: Set Up PostgreSQL Database**

1. **In your web service dashboard, click "Environment"**

2. **Add these environment variables:**
   ```
   ENVIRONMENT=production
   DEBUG=false
   SECRET_KEY=your-secure-secret-key-here
   HOST=0.0.0.0
   PORT=8000
   ```

3. **Create PostgreSQL Database:**
   - Go to "New +" → "PostgreSQL"
   - Name: `jubair-boot-house-db`
   - Plan: Free
   - Click "Create Database"

4. **Connect Database to Web Service:**
   - In your web service, go to "Environment"
   - Add environment variable:
     - **Key**: `DATABASE_URL`
     - **Value**: Copy from your PostgreSQL service dashboard

### **Step 4: Initialize Database**

1. **After deployment, your app will be available at:**
   `https://jubair-boot-house.onrender.com`

2. **Visit the health check endpoint:**
   `https://jubair-boot-house.onrender.com/health`

3. **If database is not connected, run the setup script:**
   ```bash
   # In Render's shell or locally with DATABASE_URL set
   python setup_render_db.py
   ```

## 🔧 Configuration Files

### **render.yaml (Auto-deployment)**
```yaml
services:
  - type: web
    name: jubair-boot-house
    env: python
    plan: free
    buildCommand: pip install -r requirements-prod.txt
    startCommand: gunicorn -c gunicorn.conf.py app.main:app
    envVars:
      - key: ENVIRONMENT
        value: production
      - key: DEBUG
        value: false
      - key: SECRET_KEY
        generateValue: true
      - key: HOST
        value: 0.0.0.0
      - key: PORT
        value: 8000
      - key: DATABASE_URL
        fromDatabase:
          name: jubair-boot-house-db
          property: connectionString
    healthCheckPath: /health
    autoDeploy: true

  - type: pserv
    name: jubair-boot-house-db
    env: postgres
    plan: free
    ipAllowList: []
    maxConnections: 5
```

### **Environment Variables**
```
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-secure-secret-key
HOST=0.0.0.0
PORT=8000
DATABASE_URL=postgresql://username:password@host:port/database
```

## 🗄️ Database Migration

### **Automatic Migration**
Your app automatically:
- ✅ Detects PostgreSQL vs SQLite
- ✅ Creates tables with proper schema
- ✅ Handles data type differences
- ✅ Sets up foreign key relationships

### **Manual Migration (if needed)**
```bash
# Run migration script
python migrate_to_postgresql.py

# Or run setup script
python setup_render_db.py
```

## 🔍 Troubleshooting

### **Common Issues:**

1. **Build Fails:**
   - Check `requirements-prod.txt` has `psycopg2-binary`
   - Verify Python version compatibility

2. **App Won't Start:**
   - Check start command: `gunicorn -c gunicorn.conf.py app.main:app`
   - Verify `app.main:app` path is correct

3. **Database Connection Fails:**
   - Check `DATABASE_URL` environment variable
   - Ensure PostgreSQL service is running
   - Verify connection string format

4. **Login/Signup Fails:**
   - Check database tables are created
   - Verify models are compatible with PostgreSQL
   - Check for data type conversion issues

### **Debug Steps:**

1. **Check Render logs:**
   - Go to your web service dashboard
   - Click "Logs" tab
   - Look for error messages

2. **Test database connection:**
   - Visit `/health` endpoint
   - Check database status

3. **Verify environment variables:**
   - Go to "Environment" tab
   - Ensure all variables are set correctly

## 📊 Monitoring

### **Health Check Endpoint:**
- **URL**: `/health`
- **Checks**: Database connection, app status
- **Response**: JSON with health status

### **Render Dashboard:**
- **Logs**: Real-time application logs
- **Metrics**: Response times, error rates
- **Deployments**: Build and deployment history

## 🔄 Updates and Maintenance

### **Automatic Updates:**
- Render automatically redeploys when you push to GitHub
- Database schema updates automatically

### **Manual Updates:**
```bash
# Push changes to GitHub
git add .
git commit -m "Update description"
git push origin main

# Render will automatically redeploy
```

### **Database Backups:**
- Render automatically backs up PostgreSQL data
- Free tier includes daily backups

## 🎯 Production Checklist

- [ ] Code pushed to GitHub
- [ ] Web service created on Render
- [ ] PostgreSQL database created
- [ ] Environment variables configured
- [ ] Database tables initialized
- [ ] Health check endpoint working
- [ ] Login/signup functionality tested
- [ ] Admin user created
- [ ] Sample products added

## 🚨 Important Notes

### **Free Tier Limitations:**
- **Web Service**: Sleeps after 15 minutes of inactivity
- **PostgreSQL**: 90-day retention, 1GB storage
- **Custom Domain**: Not supported on free plan

### **Performance Tips:**
- Keep your app lightweight
- Optimize database queries
- Use efficient image handling
- Monitor resource usage

## 🎉 Success!

Once deployed, your Jubair Boot House will be available at:
`https://jubair-boot-house.onrender.com`

**Login Credentials:**
- **Username**: `JuberSiddique`
- **Password**: `Juber@708492`

---

**Happy deploying on Render with PostgreSQL! 🚀**
