"""
db/mysql.py
-----------
MySQL connection using AWS Secrets Manager credentials.
Uses a simple per-request connection (PyMySQL does not support pooling natively).
For high-traffic use, consider switching to SQLAlchemy + connection pool.
"""

import boto3
import json
import pymysql
from config import AWS_REGION, DB_SECRET_NAME

_secret_cache = None  # cache credentials in memory to avoid repeated SM calls


def _get_secret():
    global _secret_cache
    if _secret_cache:
        return _secret_cache
    client = boto3.client("secretsmanager", region_name=AWS_REGION)
    _secret_cache = json.loads(
        client.get_secret_value(SecretId=DB_SECRET_NAME)["SecretString"]
    )
    return _secret_cache


def get_db_connection():
    secret = _get_secret()
    return pymysql.connect(
        host=secret["host"],
        user=secret["username"],
        password=secret["password"],
        database=secret["dbname"],
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
        connect_timeout=5,
    )
