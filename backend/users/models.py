"""
users/models.py
All DB operations for the users feature.
"""
from core.db import get_db

def get_user(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, email, created_at FROM users WHERE id=%s",
        (user_id,)
    )
    return cur.fetchone()

def update_user(user_id, name, email):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET name=%s, email=%s WHERE id=%s",
        (name, email, user_id)
    )
    conn.commit()

def delete_user(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM cart WHERE user_id=%s", (user_id,))
    cur.execute("DELETE FROM wishlist WHERE user_id=%s", (user_id,))
    cur.execute("UPDATE orders SET user_id=NULL WHERE user_id=%s", (user_id,))
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
