#!/bin/bash

# Deployment script for Jubair Boot House
# Usage: ./deploy.sh [production|staging]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default environment
ENVIRONMENT=${1:-production}

echo -e "${BLUE}🚀 Deploying Jubair Boot House to ${ENVIRONMENT} environment...${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Create necessary directories
echo -e "${YELLOW}📁 Creating necessary directories...${NC}"
mkdir -p logs
mkdir -p ssl
mkdir -p static/uploads

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from template...${NC}"
    if [ -f env.production.template ]; then
        cp env.production.template .env
        echo -e "${YELLOW}⚠️  Please update the .env file with your production values!${NC}"
        echo -e "${YELLOW}⚠️  Especially change the SECRET_KEY!${NC}"
        read -p "Press Enter after updating .env file..."
    else
        echo -e "${RED}❌ env.production.template not found!${NC}"
        exit 1
    fi
fi

# Generate SSL certificates if they don't exist (self-signed for testing)
if [ ! -f ssl/cert.pem ] || [ ! -f ssl/key.pem ]; then
    echo -e "${YELLOW}🔐 Generating self-signed SSL certificates...${NC}"
    mkdir -p ssl
    openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    echo -e "${GREEN}✅ SSL certificates generated${NC}"
fi

# Stop existing containers
echo -e "${YELLOW}🛑 Stopping existing containers...${NC}"
docker-compose down --remove-orphans

# Build and start containers
echo -e "${YELLOW}🔨 Building and starting containers...${NC}"
docker-compose up --build -d

# Wait for services to be ready
echo -e "${YELLOW}⏳ Waiting for services to be ready...${NC}"
sleep 10

# Check if services are running
echo -e "${YELLOW}🔍 Checking service status...${NC}"
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✅ Services are running successfully!${NC}"
else
    echo -e "${RED}❌ Services failed to start. Check logs with: docker-compose logs${NC}"
    exit 1
fi

# Show service information
echo -e "${BLUE}📊 Deployment Summary:${NC}"
echo -e "${BLUE}   🌐 Application: http://localhost:8000${NC}"
echo -e "${BLUE}   🔒 HTTPS: https://localhost (if using Nginx)${NC}"
echo -e "${BLUE}   📝 Logs: ./logs/app.log${NC}"
echo -e "${BLUE}   🐳 Docker: docker-compose ps${NC}"

echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"

# Show logs
echo -e "${YELLOW}📋 Recent logs (press Ctrl+C to exit):${NC}"
docker-compose logs -f --tail=50
