"""
orders/models.py
All DB operations for the orders feature.
"""
from core.db import get_db

def get_cart_items(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.product_id, c.qty, p.price
        FROM cart c JOIN products p ON c.product_id = p.id
        WHERE c.user_id=%s
    """, (user_id,))
    return cur.fetchall()

def get_product_price(product_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, price FROM products WHERE id=%s", (product_id,))
    return cur.fetchone()

def create_order(user_id, total, location, items):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO orders (user_id, total_amount, location) VALUES (%s,%s,%s)",
        (user_id, total, location)
    )
    order_id = cur.lastrowid
    for pid, qty, price in items:
        cur.execute(
            "INSERT INTO order_items (order_id, product_id, qty, price) VALUES (%s,%s,%s,%s)",
            (order_id, pid, qty, price)
        )
    conn.commit()
    return order_id

def clear_cart(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM cart WHERE user_id=%s", (user_id,))
    conn.commit()

def get_order_history(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, total_amount, location, created_at
        FROM orders WHERE user_id=%s ORDER BY created_at DESC
    """, (user_id,))
    return cur.fetchall()
