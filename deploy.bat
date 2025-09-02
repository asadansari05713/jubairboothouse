@echo off
REM Deployment script for Jubair Boot House (Windows)
REM Usage: deploy.bat [production|staging]

setlocal enabledelayedexpansion

REM Set default environment
if "%1"=="" set ENVIRONMENT=production
if "%1"=="production" set ENVIRONMENT=production
if "%1"=="staging" set ENVIRONMENT=staging

echo 🚀 Deploying Jubair Boot House to %ENVIRONMENT% environment...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Create necessary directories
echo 📁 Creating necessary directories...
if not exist "logs" mkdir logs
if not exist "ssl" mkdir ssl
if not exist "static\uploads" mkdir "static\uploads"

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found. Creating from template...
    if exist "env.production.template" (
        copy "env.production.template" ".env" >nul
        echo ⚠️  Please update the .env file with your production values!
        echo ⚠️  Especially change the SECRET_KEY!
        pause
    ) else (
        echo ❌ env.production.template not found!
        pause
        exit /b 1
    )
)

REM Generate SSL certificates if they don't exist (self-signed for testing)
if not exist "ssl\cert.pem" (
    echo 🔐 Generating self-signed SSL certificates...
    if not exist "ssl" mkdir ssl
    
    REM Check if OpenSSL is available
    openssl version >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  OpenSSL not found. Please install OpenSSL or manually create SSL certificates.
        echo ⚠️  For testing, you can use the application without HTTPS.
    ) else (
        openssl req -x509 -newkey rsa:4096 -keyout ssl\key.pem -out ssl\cert.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
        echo ✅ SSL certificates generated
    )
)

REM Stop existing containers
echo 🛑 Stopping existing containers...
docker-compose down --remove-orphans

REM Build and start containers
echo 🔨 Building and starting containers...
docker-compose up --build -d

REM Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Check if services are running
echo 🔍 Checking service status...
docker-compose ps | findstr "Up" >nul
if errorlevel 1 (
    echo ❌ Services failed to start. Check logs with: docker-compose logs
    pause
    exit /b 1
) else (
    echo ✅ Services are running successfully!
)

REM Show service information
echo 📊 Deployment Summary:
echo    🌐 Application: http://localhost:8000
echo    🔒 HTTPS: https://localhost (if using Nginx)
echo    📝 Logs: .\logs\app.log
echo    🐳 Docker: docker-compose ps

echo 🎉 Deployment completed successfully!

REM Show logs
echo 📋 Recent logs (press Ctrl+C to exit):
docker-compose logs -f --tail=50

pause
