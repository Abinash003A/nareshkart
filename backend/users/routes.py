"""
users/routes.py
Thin routes for users feature.
"""
from flask import Blueprint, request, jsonify
from core.security import token_required
from users.models import get_user, update_user, delete_user

users_bp = Blueprint("users", __name__, url_prefix="/api/users")

@users_bp.route("/me", methods=["GET"])
@token_required
def profile(user_id):
    user = get_user(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user)

@users_bp.route("/me", methods=["PUT"])
@token_required
def update_profile(user_id):
    d = request.json or {}
    name  = d.get("name", "").strip()
    email = d.get("email", "").strip()
    if not name or not email:
        return jsonify({"message": "Name and email required"}), 400
    update_user(user_id, name, email)
    return jsonify({"message": "Profile updated"})

@users_bp.route("/me", methods=["DELETE"])
@token_required
def delete_account(user_id):
    delete_user(user_id)
    return jsonify({"message": "Account deleted successfully"})
