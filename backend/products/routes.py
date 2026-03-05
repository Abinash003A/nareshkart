"""
products/routes.py
Thin routes for products feature.
"""
from flask import Blueprint, request, jsonify
from products.models import get_all_products, get_product_by_id

products_bp = Blueprint("products", __name__, url_prefix="/api/products")

@products_bp.route("", methods=["GET"])
def list_products():
    products = get_all_products(
        category=request.args.get("category"),
        hot=request.args.get("hot")
    )
    return jsonify(products)

@products_bp.route("/<int:product_id>", methods=["GET"])
def single_product(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    return jsonify(product)
