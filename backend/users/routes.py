"""
User profile APIs
"""

from flask import Blueprint, request, jsonify
from db.mysql import get_db_connection

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id,name,email,created_at FROM users WHERE id=%s", (user_id,))
    return jsonify(cur.fetchone())


@users_bp.route("/update", methods=["POST"])
def update_profile():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET name=%s, email=%s WHERE id=%s",
        (data["name"], data["email"], data["user_id"])
    )

    return {"message": "Profile updated"}, 200


@users_bp.route("/delete", methods=["POST"])
def delete_account():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM users WHERE id=%s", (data["user_id"],))
    return {"message": "Account deleted"}, 200
