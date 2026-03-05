"""
auth/routes.py
Thin routes — just HTTP in/out. All logic delegated to service.py.
"""
from flask import Blueprint, request, jsonify
from auth.service import send_otp, verify_otp_and_register, login_user

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    email = (request.json or {}).get("email", "").strip()
    if not email:
        return jsonify({"message": "Email required"}), 400
    ok, msg = send_otp(email)
    return jsonify({"message": msg}), (200 if ok else 409)

@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    d = request.json or {}
    name     = d.get("name", "").strip()
    email    = d.get("email", "").strip()
    password = d.get("password", "")
    otp      = d.get("otp", "").strip()
    if not all([name, email, password, otp]):
        return jsonify({"message": "All fields required"}), 400
    ok, msg, data = verify_otp_and_register(name, email, password, otp)
    return jsonify(data if ok else {"message": msg}), (201 if ok else 400)

@auth_bp.route("/login", methods=["POST"])
def login():
    d = request.json or {}
    email    = d.get("email", "").strip()
    password = d.get("password", "")
    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400
    ok, msg, data = login_user(email, password)
    return jsonify(data if ok else {"message": msg}), (200 if ok else 401)
