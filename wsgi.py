#!/usr/bin/env python3
"""
WSGI entry point for Jubair Boot House
This file is used by Gunicorn and other WSGI servers
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the FastAPI app
from app.main import app

# For WSGI servers that need a callable
application = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
