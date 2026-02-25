from flask import Blueprint, request, jsonify
import random
from db.mysql import get_db_connection
from cache.redis_client import redis_client
from auth.utils import hash_password, verify_password, generate_jwt

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data["email"]

    otp = str(random.randint(100000, 999999))
    redis_client.setex(f"otp:{email}", 300, otp)

    # REAL EMAIL CAN BE PLUGGED VIA SES LATER
    return {"message": "OTP sent"}, 200

@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.json
    otp_saved = redis_client.get(f"otp:{data['email']}")

    if otp_saved != data["otp"]:
        return {"message": "Invalid OTP"}, 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
        (data["name"], data["email"], hash_password(data["password"]))
    )

    user_id = cur.lastrowid
    token = generate_jwt(user_id)

    return {"token": token, "user": {"id": user_id, "name": data["name"]}}, 200

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email=%s", (data["email"],))
    user = cur.fetchone()

    if not user or not verify_password(data["password"], user["password"]):
        return {"message": "Invalid credentials"}, 401

    token = generate_jwt(user["id"])
    return {"token": token, "user": user}, 200
