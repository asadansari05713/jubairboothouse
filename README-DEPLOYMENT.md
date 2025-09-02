# 🚀 Quick Deployment Guide

## ⚡ Fast Deployment (Docker)

### 1. Install Dependencies
```bash
pip install -r requirements-prod.txt
```

### 2. Deploy
```bash
# Windows
deploy.bat

# Linux/Mac
./deploy.sh
```

### 3. Access Your Website
- **Application**: http://localhost:8000
- **HTTPS**: https://localhost (if using Nginx)

## 🔧 Manual Deployment

### 1. Set Environment Variables
```bash
# Copy template
cp env.production.template .env

# Edit .env file (IMPORTANT: Change SECRET_KEY!)
```

### 2. Start Server
```bash
# Using Gunicorn
gunicorn -c gunicorn.conf.py main:app

# Or using script
python start_production.py
```

## 🌐 Production Deployment

### 1. Update Environment
- Change `SECRET_KEY` to secure value
- Set `ALLOWED_ORIGINS` to your domain
- Configure `DATABASE_URL` for production database

### 2. Deploy to Cloud
- **Heroku**: Use Procfile
- **Railway**: Connect GitHub repo
- **Render**: Set build/start commands

### 3. SSL Setup
- **Let's Encrypt**: Free SSL certificates
- **Cloudflare**: Easy SSL management

## 📁 Files Created

- `config.py` - Configuration management
- `requirements-prod.txt` - Production dependencies
- `start_production.py` - Production startup script
- `gunicorn.conf.py` - Gunicorn configuration
- `Dockerfile` - Docker container setup
- `docker-compose.yml` - Multi-service deployment
- `nginx.conf` - Reverse proxy configuration
- `deploy.sh` / `deploy.bat` - Deployment scripts
- `DEPLOYMENT.md` - Comprehensive guide

## 🚨 Important Notes

1. **Change SECRET_KEY** in `.env` file
2. **Enable HTTPS** for production
3. **Set up monitoring** and logging
4. **Configure backups** for database
5. **Test thoroughly** before going live

## 🔗 Useful Commands

```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Check status
docker-compose ps

# Update application
git pull && docker-compose up --build -d
```

---

**For detailed instructions, see `DEPLOYMENT.md`**
