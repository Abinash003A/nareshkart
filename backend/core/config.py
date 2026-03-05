"""
core/config.py
All environment-based config. Import from here across all features.
"""
import os

JWT_SECRET       = os.getenv("JWT_SECRET", "changeme-secret")
JWT_EXPIRY_HOURS = 24

AWS_REGION       = os.getenv("AWS_REGION", "ap-south-1")
DB_SECRET_NAME   = os.getenv("DB_SECRET_NAME", "nareshkart/db")

REDIS_HOST       = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT       = int(os.getenv("REDIS_PORT", 6379))

SES_SENDER_EMAIL = os.getenv("SES_SENDER_EMAIL", "no-reply@nareshkart.in")
