"""
cart/routes.py
--------------
Handles:
- Add item to cart
- Update quantity
- View cart
- Remove item
"""

from flask import Blueprint, request, jsonify
from db.mysql import get_db_connection
from auth.utils import token_required

cart_bp = Blueprint("cart", __name__, url_prefix="/api/cart")


@cart_bp.route("", methods=["GET"])
@token_required
def get_cart(user_id):
    """
    GET /api/cart
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.product_id, c.qty, p.name, p.price, p.emoji
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id=%s
    """, (user_id,))

    return jsonify(cur.fetchall())


@cart_bp.route("", methods=["POST"])
@token_required
def add_to_cart(user_id):
    """
    POST /api/cart
    body: product_id, qty
    """
    data = request.json
    product_id = data["product_id"]
    qty = data.get("qty", 1)

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO cart (user_id, product_id, qty)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE qty = qty + %s
    """, (user_id, product_id, qty, qty))

    conn.commit()
    return jsonify({"message": "Item added to cart"})


@cart_bp.route("/<int:product_id>", methods=["DELETE"])
@token_required
def remove_from_cart(user_id, product_id):
    """
    DELETE /api/cart/<product_id>
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM cart WHERE user_id=%s AND product_id=%s",
        (user_id, product_id)
    )
    conn.commit()

    return jsonify({"message": "Item removed"})
