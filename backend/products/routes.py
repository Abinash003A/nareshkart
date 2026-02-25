"""
Product APIs
- List all products
- Filter by category
- Hot products
"""

from flask import Blueprint, request, jsonify
from db.mysql import get_db_connection

products_bp = Blueprint("products", __name__, url_prefix="/api/products")


@products_bp.route("", methods=["GET"])
def get_products():
    category = request.args.get("cat")

    conn = get_db_connection()
    cur = conn.cursor()

    if category:
        cur.execute("SELECT * FROM products WHERE category=%s", (category,))
    else:
        cur.execute("SELECT * FROM products")

    products = cur.fetchall()
    return jsonify(products)


@products_bp.route("/hot", methods=["GET"])
def hot_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE is_hot=1")
    return jsonify(cur.fetchall())
