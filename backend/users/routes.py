"""
users/routes.py
---------------
Handles:
- Get profile
- Update profile
- Delete account
"""

from flask import Blueprint, request, jsonify
from db.mysql import get_db_connection
from auth.utils import token_required

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("/me", methods=["GET"])
@token_required
def get_profile(user_id):
    """
    GET /api/users/me
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, name, email, created_at FROM users WHERE id=%s",
        (user_id,)
    )

    user = cur.fetchone()

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(user)


@users_bp.route("/me", methods=["PUT"])
@token_required
def update_profile(user_id):
    """
    PUT /api/users/me
    body:
    - name
    - email
    """
    data = request.json
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"message": "Name and email required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET name=%s, email=%s WHERE id=%s",
        (name, email, user_id)
    )

    conn.commit()

    return jsonify({"message": "Profile updated"})


@users_bp.route("/me", methods=["DELETE"])
@token_required
def delete_account(user_id):
    """
    DELETE /api/users/me
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # Delete related data first (safe cleanup)
    cur.execute("DELETE FROM cart WHERE user_id=%s", (user_id,))
    cur.execute("DELETE FROM wishlist WHERE user_id=%s", (user_id,))
    cur.execute("DELETE FROM orders WHERE user_id=%s", (user_id,))
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))

    conn.commit()

    return jsonify({"message": "Account deleted successfully"})
