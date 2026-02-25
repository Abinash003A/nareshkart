"""
Wishlist APIs
"""

from flask import Blueprint, request, jsonify
from db.mysql import get_db_connection

wishlist_bp = Blueprint("wishlist", __name__, url_prefix="/api/wishlist")


@wishlist_bp.route("", methods=["POST"])
def add_wishlist():
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT IGNORE INTO wishlist (user_id, product_id) VALUES (%s,%s)",
        (data["user_id"], data["product_id"])
    )

    return {"message": "Added to wishlist"}, 200


@wishlist_bp.route("/<int:user_id>", methods=["GET"])
def view_wishlist(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.*
        FROM wishlist w
        JOIN products p ON w.product_id = p.id
        WHERE w.user_id=%s
    """, (user_id,))

    return jsonify(cur.fetchall())


@wishlist_bp.route("/remove", methods=["POST"])
def remove_wishlist():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM wishlist WHERE user_id=%s AND product_id=%s",
        (data["user_id"], data["product_id"])
    )

    return {"message": "Removed from wishlist"}, 200
