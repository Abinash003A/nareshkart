"""
Cart APIs
- Add item
- Remove item
- View cart
"""

from flask import Blueprint, request, jsonify
from db.mysql import get_db_connection

cart_bp = Blueprint("cart", __name__, url_prefix="/api/cart")


@cart_bp.route("", methods=["POST"])
def add_to_cart():
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO cart (user_id, product_id, qty)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE qty = qty + %s
    """, (data["user_id"], data["product_id"], data["qty"], data["qty"]))

    return {"message": "Added to cart"}, 200


@cart_bp.route("/<int:user_id>", methods=["GET"])
def view_cart(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.*, c.qty
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id=%s
    """, (user_id,))

    return jsonify(cur.fetchall())


@cart_bp.route("/remove", methods=["POST"])
def remove_from_cart():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM cart WHERE user_id=%s AND product_id=%s",
        (data["user_id"], data["product_id"])
    )

    return {"message": "Removed from cart"}, 200
