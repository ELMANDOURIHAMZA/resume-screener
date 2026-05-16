"""Central configuration for the Resume Screener project.

Defines filesystem paths, API metadata and simple env-configurable settings.
"""
from pathlib import Path
import os

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = DATA_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Model artifact paths
VECTORIZER_PATH = MODELS_DIR / "vectorizer.joblib"
CLASSIFIER_PATH = MODELS_DIR / "category_classifier.joblib"
CLASSIFIER_META_PATH = MODELS_DIR / "classifier_meta.json"
RESUME_CSV = DATA_DIR / "Resume.csv"

# API / App settings
API_TITLE = os.getenv("API_TITLE", "Resume Screening API")
API_VERSION = os.getenv("API_VERSION", "1.0.0")
API_DESCRIPTION = os.getenv("API_DESCRIPTION", "AI-powered resume screening service.")

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() in ("1", "true", "yes")
CORS_ALLOW_METHODS = os.getenv("CORS_ALLOW_METHODS", "*")
CORS_ALLOW_HEADERS = os.getenv("CORS_ALLOW_HEADERS", "*")

# ML defaults
DEFAULT_TOP_K = int(os.getenv("DEFAULT_TOP_K", "5"))
MAX_TOP_K = int(os.getenv("MAX_TOP_K", "100"))
MIN_TOP_K = int(os.getenv("MIN_TOP_K", "1"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
