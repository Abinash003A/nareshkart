from flask import Blueprint, request, jsonify
import random
from db.mysql import get_db_connection
from cache.redis_client import redis_client
from auth.utils import hash_password, verify_password, generate_jwt
from auth.email_service import send_otp_email

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# STEP 1: Register (Send OTP)
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")

    if not email:
        return {"message": "Email required"}, 400

    otp = str(random.randint(100000, 999999))

    # Store OTP in Redis for 5 minutes
    redis_client.setex(f"otp:{email}", 300, otp)

    # Send real email via SES
    send_otp_email(email, otp)

    return {"message": "OTP sent to email"}, 200


# STEP 2: Verify OTP & Create User
@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    otp = data.get("otp")

    stored_otp = redis_client.get(f"otp:{email}")

    if not stored_otp or stored_otp != otp:
        return {"message": "Invalid or expired OTP"}, 400

    conn = get_db_connection()
    cur = conn.cursor()

    # Prevent duplicate user
    cur.execute("SELECT id FROM users WHERE email=%s", (email,))
    if cur.fetchone():
        return {"message": "User already exists"}, 400

    cur.execute(
        "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
        (name, email, hash_password(password))
    )

    user_id = cur.lastrowid

    token = generate_jwt(user_id)

    return {
        "token": token,
        "user": {"id": user_id, "name": name, "email": email}
    }, 200


# STEP 3: Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()

    if not user or not verify_password(password, user["password"]):
        return {"message": "Invalid credentials"}, 401

    token = generate_jwt(user["id"])

    return {
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    }, 200
