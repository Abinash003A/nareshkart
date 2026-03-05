"""
cart/routes.py
Thin routes for cart feature.
"""
from flask import Blueprint, request, jsonify
from core.security import token_required
from cart.models import get_cart, upsert_cart, remove_from_cart

cart_bp = Blueprint("cart", __name__, url_prefix="/api/cart")

@cart_bp.route("", methods=["GET"])
@token_required
def view_cart(user_id):
    return jsonify(get_cart(user_id))

@cart_bp.route("", methods=["POST"])
@token_required
def update_cart(user_id):
    d = request.json or {}
    product_id = d.get("product_id")
    qty = int(d.get("qty", 1))
    if not product_id:
        return jsonify({"message": "product_id required"}), 400
    ok = upsert_cart(user_id, product_id, qty)
    return jsonify({"message": "Cart updated"}) if ok else (jsonify({"message": "Product not found"}), 404)

@cart_bp.route("/<int:product_id>", methods=["DELETE"])
@token_required
def delete_from_cart(user_id, product_id):
    remove_from_cart(user_id, product_id)
    return jsonify({"message": "Item removed"})
