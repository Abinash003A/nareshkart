import os

AWS_REGION     = os.getenv("AWS_REGION")
DB_SECRET_NAME = os.getenv("DB_SECRET_NAME")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRY_SECONDS = 86400

SES_SENDER_EMAIL = os.getenv("SES_SENDER_EMAIL")
