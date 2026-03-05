"""
auth/models.py
All database operations for the auth feature.
"""
from core.db import get_db
from core.security import hash_password, check_password

def email_exists(email: str) -> bool:
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE email=%s", (email,))
    return cur.fetchone() is not None

def create_user(name: str, email: str, password: str) -> int:
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (name, email, hash_password(password))
    )
    conn.commit()
    return cur.lastrowid

def get_user_by_email(email: str) -> dict | None:
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, password FROM users WHERE email=%s", (email,))
    return cur.fetchone()
