"""
Auth utilities: password hashing & JWT
"""

import bcrypt
import jwt
import datetime
from config import JWT_SECRET, JWT_EXPIRY_SECONDS

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def generate_jwt(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXPIRY_SECONDS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")
