"""
wishlist/routes.py
------------------
Handles:
- Add to wishlist
- Remove from wishlist
- View wishlist
"""

from flask import Blueprint, request, jsonify
from db.mysql import get_db_connection
from auth.utils import token_required

wishlist_bp = Blueprint("wishlist", __name__, url_prefix="/api/wishlist")


@wishlist_bp.route("", methods=["GET"])
@token_required
def get_wishlist(user_id):
    """
    GET /api/wishlist
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT w.product_id, p.name, p.price, p.category
        FROM wishlist w
        JOIN products p ON w.product_id = p.id
        WHERE w.user_id=%s
    """, (user_id,))

    return jsonify(cur.fetchall())


@wishlist_bp.route("", methods=["POST"])
@token_required
def add_to_wishlist(user_id):
    """
    POST /api/wishlist
    body: product_id
    """
    product_id = request.json["product_id"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT IGNORE INTO wishlist (user_id, product_id)
        VALUES (%s, %s)
    """, (user_id, product_id))

    conn.commit()

    return jsonify({"message": "Added to wishlist"})


@wishlist_bp.route("/<int:product_id>", methods=["DELETE"])
@token_required
def remove_from_wishlist(user_id, product_id):
    """
    DELETE /api/wishlist/<product_id>
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM wishlist WHERE user_id=%s AND product_id=%s",
        (user_id, product_id)
    )

    conn.commit()

    return jsonify({"message": "Removed from wishlist"})
