"""
products/routes.py
------------------
Handles:
- List all products
- Filter by category
- Hot products
"""

from flask import Blueprint, jsonify, request
from db.mysql import get_db_connection

products_bp = Blueprint("products", __name__, url_prefix="/api/products")


@products_bp.route("", methods=["GET"])
def list_products():
    """
    GET /api/products
    Optional query params:
    - category
    - hot=true
    """
    category = request.args.get("category")
    hot = request.args.get("hot")

    conn = get_db_connection()
    cur = conn.cursor()

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if category:
        query += " AND category=%s"
        params.append(category)

    if hot == "true":
        query += " AND hot=1"

    cur.execute(query, params)
    products = cur.fetchall()

    return jsonify(products)


@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    GET /api/products/<id>
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM products WHERE id=%s", (product_id,))
    product = cur.fetchone()

    if not product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify(product)
