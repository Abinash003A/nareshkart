"""
wishlist/routes.py
Thin routes for wishlist feature.
"""
from flask import Blueprint, request, jsonify
from core.security import token_required
from wishlist.models import get_wishlist, add_to_wishlist, remove_from_wishlist

wishlist_bp = Blueprint("wishlist", __name__, url_prefix="/api/wishlist")

@wishlist_bp.route("", methods=["GET"])
@token_required
def view_wishlist(user_id):
    return jsonify(get_wishlist(user_id))

@wishlist_bp.route("", methods=["POST"])
@token_required
def add_wishlist(user_id):
    product_id = (request.json or {}).get("product_id")
    if not product_id:
        return jsonify({"message": "product_id required"}), 400
    add_to_wishlist(user_id, product_id)
    return jsonify({"message": "Added to wishlist"})

@wishlist_bp.route("/<int:product_id>", methods=["DELETE"])
@token_required
def remove_wishlist(user_id, product_id):
    remove_from_wishlist(user_id, product_id)
    return jsonify({"message": "Removed from wishlist"})
