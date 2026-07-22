import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
UPLOADS_DIR = BASE_DIR / "uploads"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"

# Create directories if they don't exist
UPLOADS_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# API Configuration
API_TITLE = "ForgeML"
API_VERSION = "1.0.0"
API_DESCRIPTION = "ML Training Platform with Auto-Generated UI"

# CORS
CORS_ORIGINS = ["*"]  # Change to specific domains in production

# ML Configuration
RANDOM_STATE = 42
TEST_SIZE = 0.2

# Development Configuration
DEV_PORT = 8000
DEV_HOST = "0.0.0.0"
DEV_RELOAD = True

# Logging Configuration
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
