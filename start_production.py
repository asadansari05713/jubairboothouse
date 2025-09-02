#!/usr/bin/env python3
"""
Production startup script for Jubair Boot House
This script is optimized for production deployment
"""

import os
import sys
import logging
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Configure logging for production
def setup_logging():
    """Setup production logging"""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level),
        format=log_format,
        handlers=[
            logging.FileHandler(log_dir / "app.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set specific logger levels
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.ERROR)

def main():
    """Main production startup function"""
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        
        logger.info("🚀 Starting Jubair Boot House in production mode...")
        
        # Import and start the application
        import uvicorn
        from app.main import app
        
        # Production settings
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", "8000"))
        workers = int(os.getenv("WORKERS", "1"))
        
        logger.info(f"📍 Server will be available at: http://{host}:{port}")
        logger.info(f"🔧 Workers: {workers}")
        logger.info(f"🌍 Environment: {os.getenv('ENVIRONMENT', 'production')}")
        
        # Start the server
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            workers=workers,
            log_level="info",
            access_log=True,
            use_colors=False
        )
        
    except KeyboardInterrupt:
        logger.info("👋 Shutting down Jubair Boot House...")
    except Exception as e:
        logger.error(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
