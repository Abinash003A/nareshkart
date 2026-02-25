from flask import Blueprint, request, jsonify
from db.mysql import get_db_connection
from cache.redis_client import redis_client
from auth.utils import *
import random
import boto3
from config import AWS_REGION, SES_SENDER_EMAIL

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

ses = boto3.client("ses", region_name=AWS_REGION)

@auth_bp.route("/register", methods=["POST"])
def register():
    email = request.json.get("email")
    otp = str(random.randint(100000, 999999))

    redis_client.setex(f"otp:{email}", 300, otp)

    ses.send_email(
        Source=SES_SENDER_EMAIL,
        Destination={"ToAddresses": [email]},
        Message={
            "Subject": {"Data": "NareshKart OTP"},
            "Body": {"Text": {"Data": f"Your OTP is {otp}"}}
        }
    )

    return jsonify({"message": "OTP sent"}), 200

@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.json
    stored = redis_client.get(f"otp:{data['email']}")

    if stored != data["otp"]:
        return jsonify({"message": "Invalid OTP"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",
        (data["name"], data["email"], hash_password(data["password"]))
    )

    user_id = cur.lastrowid
    token = generate_jwt(user_id)

    return jsonify({"token": token, "user": {"id": user_id, "name": data["name"]}})
