# 🚀 Jubair Boot House - Deployment Guide

This guide will help you deploy your Jubair Boot House website to production.

## 📋 Prerequisites

- **Python 3.11+** installed
- **Docker** and **Docker Compose** installed
- **Git** for version control
- **Domain name** (optional, for production)

## 🏗️ Deployment Options

### Option 1: Docker Deployment (Recommended)

#### Step 1: Install Dependencies
```bash
# Install production dependencies
pip install -r requirements-prod.txt
```

#### Step 2: Configure Environment
```bash
# Copy environment template
cp env.production.template .env

# Edit .env file with your production values
# IMPORTANT: Change SECRET_KEY to a secure random string
```

#### Step 3: Deploy with Docker
```bash
# On Linux/Mac
./deploy.sh

# On Windows
deploy.bat
```

### Option 2: Manual Deployment

#### Step 1: Install Production Dependencies
```bash
pip install -r requirements-prod.txt
```

#### Step 2: Create Production Environment
```bash
# Set environment variables
export ENVIRONMENT=production
export DEBUG=false
export SECRET_KEY="your-secure-secret-key"
export HOST=0.0.0.0
export PORT=8000
```

#### Step 3: Start Production Server
```bash
# Using Gunicorn (recommended)
gunicorn -c gunicorn.conf.py main:app

# Or using the production script
python start_production.py
```

### Option 3: Cloud Platform Deployment

#### Heroku
```bash
# Create Procfile
echo "web: gunicorn -c gunicorn.conf.py main:app" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

#### Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

#### Render
```bash
# Connect your GitHub repository
# Set build command: pip install -r requirements-prod.txt
# Set start command: gunicorn -c gunicorn.conf.py main:app
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `ENVIRONMENT` | Environment name | `production` | Yes |
| `DEBUG` | Debug mode | `false` | Yes |
| `SECRET_KEY` | Secret key for security | - | **Yes** |
| `HOST` | Server host | `0.0.0.0` | No |
| `PORT` | Server port | `8000` | No |
| `DATABASE_URL` | Database connection string | SQLite | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |

### Security Configuration

1. **Change SECRET_KEY**: Generate a secure random string
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Enable HTTPS**: Use Nginx with SSL certificates
3. **Set up Firewall**: Restrict access to necessary ports
4. **Database Security**: Use strong passwords and restrict access

## 🌐 Domain and SSL Setup

### Using Let's Encrypt (Free SSL)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Using Cloudflare (Recommended)

1. Add your domain to Cloudflare
2. Update nameservers
3. Enable SSL/TLS encryption mode: "Full (strict)"
4. Enable "Always Use HTTPS"

## 📊 Monitoring and Logging

### Health Checks
- **Endpoint**: `/health`
- **Docker**: Built-in health checks
- **External**: Uptime monitoring services

### Logs
- **Application**: `logs/app.log`
- **Docker**: `docker-compose logs`
- **Nginx**: `/var/log/nginx/`

### Performance Monitoring
- **Response Time**: Monitor API endpoints
- **Error Rate**: Track 4xx/5xx responses
- **Resource Usage**: CPU, memory, disk usage

## 🔄 Updates and Maintenance

### Updating the Application
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up --build -d
```

### Database Backups
```bash
# SQLite backup
cp jubair_boot_house.db backup_$(date +%Y%m%d_%H%M%S).db

# MySQL backup
mysqldump -u username -p database_name > backup.sql
```

### Log Rotation
```bash
# Add to crontab
0 0 * * 0 find /path/to/logs -name "*.log" -mtime +7 -delete
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   netstat -tulpn | grep :8000
   
   # Kill the process
   kill -9 <PID>
   ```

2. **Permission Denied**
   ```bash
   # Fix file permissions
   chmod +x deploy.sh
   chmod 755 static/uploads
   ```

3. **Database Connection Issues**
   ```bash
   # Check database file
   ls -la jubair_boot_house.db
   
   # Test connection
   python -c "from app.database import engine; print('Connected')"
   ```

### Debug Mode
```bash
# Enable debug mode temporarily
export DEBUG=true
export LOG_LEVEL=DEBUG

# Start with debug
python start_production.py
```

## 📞 Support

If you encounter issues:

1. Check the logs: `docker-compose logs` or `logs/app.log`
2. Verify environment variables
3. Check Docker container status: `docker-compose ps`
4. Ensure all dependencies are installed

## 🔗 Useful Commands

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop all services
docker-compose down

# View resource usage
docker stats

# Access container shell
docker-compose exec jubair-boot-house bash
```

## 🎯 Production Checklist

- [ ] SECRET_KEY changed to secure value
- [ ] DEBUG mode disabled
- [ ] HTTPS enabled
- [ ] Database backups configured
- [ ] Log rotation set up
- [ ] Monitoring configured
- [ ] Firewall rules set
- [ ] SSL certificates valid
- [ ] Environment variables configured
- [ ] Health checks working
- [ ] Error logging enabled
- [ ] Rate limiting configured

---

**Happy Deploying! 🚀**
