"""
products/models.py
All DB operations for the products feature.
"""
from core.db import get_db

def get_all_products(category=None, hot=None):
    conn = get_db()
    cur = conn.cursor()
    query = "SELECT * FROM products WHERE 1=1"
    params = []
    if category:
        query += " AND category=%s"
        params.append(category)
    if hot == "true":
        query += " AND hot=1"
    cur.execute(query, params)
    return cur.fetchall()

def get_product_by_id(product_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id=%s", (product_id,))
    return cur.fetchone()
