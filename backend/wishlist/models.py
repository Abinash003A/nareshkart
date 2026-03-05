"""
wishlist/models.py
All DB operations for the wishlist feature.
"""
from core.db import get_db

def get_wishlist(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT w.product_id, p.name, p.price, p.category, p.emoji
        FROM wishlist w JOIN products p ON w.product_id = p.id
        WHERE w.user_id=%s
    """, (user_id,))
    return cur.fetchall()

def add_to_wishlist(user_id, product_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT IGNORE INTO wishlist (user_id, product_id) VALUES (%s,%s)",
        (user_id, product_id)
    )
    conn.commit()

def remove_from_wishlist(user_id, product_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM wishlist WHERE user_id=%s AND product_id=%s",
        (user_id, product_id)
    )
    conn.commit()
