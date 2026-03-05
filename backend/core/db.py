"""
core/db.py
MySQL connection using AWS Secrets Manager credentials (cached).
"""
import boto3, json, pymysql
from core.config import AWS_REGION, DB_SECRET_NAME

_secret_cache = None

def _get_secret():
    global _secret_cache
    if _secret_cache:
        return _secret_cache
    client = boto3.client("secretsmanager", region_name=AWS_REGION)
    _secret_cache = json.loads(
        client.get_secret_value(SecretId=DB_SECRET_NAME)["SecretString"]
    )
    return _secret_cache

def get_db():
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
