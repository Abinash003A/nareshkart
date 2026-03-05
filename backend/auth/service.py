"""
auth/service.py
Business logic for auth feature.
Handles OTP, email, and token logic.
"""
import random, boto3
from core.redis import client as redis_client
from core.security import generate_jwt, check_password
from core.config import AWS_REGION, SES_SENDER_EMAIL
from auth.models import email_exists, create_user, get_user_by_email

ses = boto3.client("ses", region_name=AWS_REGION)

def send_otp(email: str) -> tuple[bool, str]:
    if email_exists(email):
        return False, "Email already registered"
    otp = str(random.randint(100000, 999999))
    redis_client.setex(f"otp:{email}", 300, otp)
    ses.send_email(
        Source=SES_SENDER_EMAIL,
        Destination={"ToAddresses": [email]},
        Message={
            "Subject": {"Data": "NareshKart — Your OTP Code"},
            "Body": {"Text": {"Data": f"Your OTP is: {otp}\nValid for 5 minutes."}}
        },
    )
    return True, "OTP sent to email"

def verify_otp_and_register(name, email, password, otp) -> tuple[bool, str, dict]:
    stored = redis_client.get(f"otp:{email}")
    if not stored or stored != otp:
        return False, "Invalid or expired OTP", {}
    redis_client.delete(f"otp:{email}")
    user_id = create_user(name, email, password)
    token = generate_jwt(user_id)
    return True, "Registered", {"token": token, "user": {"id": user_id, "name": name, "email": email}}

def login_user(email, password) -> tuple[bool, str, dict]:
    user = get_user_by_email(email)
    if not user or not check_password(password, user["password"]):
        return False, "Invalid email or password", {}
    token = generate_jwt(user["id"])
    return True, "OK", {"token": token, "user": {"id": user["id"], "name": user["name"], "email": user["email"]}}
