"""
MySQL connection using AWS Secrets Manager
Password rotation safe
"""

import boto3
import json
import pymysql
from config import AWS_REGION, DB_SECRET_NAME

def get_db_connection():
    client = boto3.client("secretsmanager", region_name=AWS_REGION)

    secret = json.loads(
        client.get_secret_value(SecretId=DB_SECRET_NAME)["SecretString"]
    )

    return pymysql.connect(
        host=secret["host"],
        user=secret["username"],
        password=secret["password"],
        database=secret["dbname"],
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
