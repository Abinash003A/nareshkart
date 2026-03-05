"""
cart/models.py
All DB operations for the cart feature.
"""
from core.db import get_db

def get_cart(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.product_id, c.qty, p.name, p.price, p.emoji
        FROM cart c JOIN products p ON c.product_id = p.id
        WHERE c.user_id=%s
    """, (user_id,))
    return cur.fetchall()

def upsert_cart(user_id, product_id, qty):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM products WHERE id=%s", (product_id,))
    if not cur.fetchone():
        return False
    if qty > 0:
        cur.execute("""
            INSERT INTO cart (user_id, product_id, qty) VALUES (%s,%s,%s)
            ON DUPLICATE KEY UPDATE qty = qty + %s
        """, (user_id, product_id, qty, qty))
    else:
        cur.execute(
            "UPDATE cart SET qty = GREATEST(qty + %s, 0) WHERE user_id=%s AND product_id=%s",
            (qty, user_id, product_id)
        )
        cur.execute(
            "DELETE FROM cart WHERE user_id=%s AND product_id=%s AND qty=0",
            (user_id, product_id)
        )
    conn.commit()
    return True

def remove_from_cart(user_id, product_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM cart WHERE user_id=%s AND product_id=%s", (user_id, product_id))
    conn.commit()
