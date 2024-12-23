# db_connection.py
import pymysql
from dotenv import load_dotenv
import os
from urllib.parse import urlparse

load_dotenv()  # Load environment variables from .env

# Parse database URL from .env file
db_url = os.getenv('DATABASE_URL')
parsed_url = urlparse(db_url)

# Establish MySQL connection


def create_connection():
    return pymysql.connect(
        host=parsed_url.hostname,
        user=parsed_url.username,
        password=parsed_url.password,
        database=parsed_url.path[1:],
        port=parsed_url.port,
        autocommit=True  # enable autocommit to refresh data
    )
