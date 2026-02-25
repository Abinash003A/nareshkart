from flask import Blueprint, request, jsonify
from db.mysql import get_db_connection

orders_bp = Blueprint("orders", __name__, url_prefix="/api/orders")

@orders_bp.route("", methods=["POST"])
def create_order():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO orders(user_id,total_amount,latitude,longitude) VALUES(%s,%s,%s,%s)",
        (data["user_id"], data["total"], data["lat"], data["lon"])
    )
    return {"message": "Order placed"}, 200

@orders_bp.route("/history/<int:user_id>")
def order_history(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE user_id=%s", (user_id,))
    return jsonify(cur.fetchall())
