"""
core/security.py
JWT + bcrypt helpers and the token_required decorator.
Shared across all features that need authentication.
"""
import bcrypt, jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
from core.config import JWT_SECRET, JWT_EXPIRY_HOURS


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def check_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def generate_jwt(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRY_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def decode_jwt(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"message": "Token missing"}), 401
        try:
            token = auth_header.split(" ")[1]
            data = decode_jwt(token)
            user_id = data["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except Exception:
            return jsonify({"message": "Invalid token"}), 401
        return f(user_id, *args, **kwargs)
    return decorated
