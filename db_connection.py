# Author: Jordan Morris and Victor Vu
# File: db_connection.py
# Description: Adds a connection to MySQL for all local server files
# Copyright (C) 2024 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
import pymysql
from dotenv import load_dotenv
import os
from urllib.parse import urlparse

load_dotenv() # Load environment variables from .env

# Parse database URL from .env file
db_url = os.getenv('DATABASE_URL')
parsed_url = urlparse(db_url)

def create_connection(): # Establish MySQL connection
    return pymysql.connect(
        host=parsed_url.hostname,
        user=parsed_url.username,
        password=parsed_url.password,
        database=parsed_url.path[1:],
        port=parsed_url.port,
        autocommit=True # autocommit to refresh data
    )
