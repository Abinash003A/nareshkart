"""
orders/routes.py
----------------
Handles:
- Buy now
- Checkout cart
- Save order with location
- View order history
"""

from flask import Blueprint, request, jsonify
from db.mysql import get_db_connection
from auth.utils import token_required

orders_bp = Blueprint("orders", __name__, url_prefix="/api/orders")


@orders_bp.route("", methods=["POST"])
@token_required
def place_order(user_id):
    """
    POST /api/orders
    body:
    - location (string, e.g. "Hyderabad, India")
    - source: "cart" | "direct"
    - product_id (required if direct)
    - qty (optional)
    """
    data = request.json
    location = data.get("location")
    source = data.get("source")

    if not location:
        return jsonify({"message": "Location required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    items = []

    # ── DIRECT BUY ──
    if source == "direct":
        product_id = data.get("product_id")
        qty = int(data.get("qty", 1))

        cur.execute(
            "SELECT id, price FROM products WHERE id=%s",
            (product_id,)
        )
        product = cur.fetchone()
        if not product:
            return jsonify({"message": "Product not found"}), 404

        total = product["price"] * qty
        items.append((product_id, qty, product["price"]))

    # ── CART CHECKOUT ──
    else:
        cur.execute("""
            SELECT c.product_id, c.qty, p.price
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id=%s
        """, (user_id,))
        rows = cur.fetchall()

        if not rows:
            return jsonify({"message": "Cart is empty"}), 400

        total = sum(r["qty"] * r["price"] for r in rows)
        items = [(r["product_id"], r["qty"], r["price"]) for r in rows]

    # ── CREATE ORDER ──
    cur.execute("""
        INSERT INTO orders (user_id, total_amount, location)
        VALUES (%s, %s, %s)
    """, (user_id, total, location))

    order_id = cur.lastrowid

    # ── ORDER ITEMS ──
    for product_id, qty, price in items:
        cur.execute("""
            INSERT INTO order_items (order_id, product_id, qty, price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, product_id, qty, price))

    # Clear cart after checkout
    if source != "direct":
        cur.execute("DELETE FROM cart WHERE user_id=%s", (user_id,))

    conn.commit()

    return jsonify({
        "message": "Order placed successfully",
        "order_id": order_id,
        "total": total
    })


@orders_bp.route("", methods=["GET"])
@token_required
def order_history(user_id):
    """
    GET /api/orders
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, total_amount, location, created_at
        FROM orders
        WHERE user_id=%s
        ORDER BY created_at DESC
    """, (user_id,))

    return jsonify(cur.fetchall())
