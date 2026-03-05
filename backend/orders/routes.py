"""
orders/routes.py
Thin routes for orders feature.
"""
from flask import Blueprint, request, jsonify
from core.security import token_required
from orders.service import place_order
from orders.models import get_order_history

orders_bp = Blueprint("orders", __name__, url_prefix="/api/orders")

@orders_bp.route("", methods=["POST"])
@token_required
def create_order(user_id):
    d = request.json or {}
    location = d.get("location", "").strip()
    if not location:
        return jsonify({"message": "Location required"}), 400
    ok, msg, data = place_order(
        user_id, location,
        source=d.get("source", "cart"),
        product_id=d.get("product_id"),
        qty=d.get("qty", 1)
    )
    return jsonify(data if ok else {"message": msg}), (201 if ok else 400)

@orders_bp.route("", methods=["GET"])
@token_required
def history(user_id):
    return jsonify(get_order_history(user_id))
