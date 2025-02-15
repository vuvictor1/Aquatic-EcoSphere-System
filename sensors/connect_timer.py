# Author: Victor Vu
# File: connect_timer.py
# Description: MySQL connection for all sensors and provide a central timer
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
import pymysql
import os
import time
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()  # Load environment variables from .env

# Parse database URL from .env file
db_url = os.getenv("DATABASE_URL")
parsed_url = urlparse(db_url)
connection = None  # initialize connection


def create_connection():  # Establish MySQL connection
    global connection
    try:  # If not open make new connection
        if connection is None or not connection.open:
            connection = pymysql.connect(
                host=parsed_url.hostname,
                user=parsed_url.username,
                password=parsed_url.password,
                database=parsed_url.path[1:],
                port=parsed_url.port,
                autocommit=True,  # enable autocommit to refresh data
            )
    except pymysql.MySQLError as e:  # Error handling
        print(f"Error connecting to MySQL: {e}")
        connection = None
    return connection


def reconnect():  # Reconnect if connection is lost
    global connection
    while connection is None or not connection.open:
        print("Attempting to reconnect to MySQL...")
        create_connection()
        if connection is None or not connection.open:
            time.sleep(5)  # wait 5 seconds before retrying


def control_timer():  # Set timer to control the frequency
    while True:
        reconnect()  # Ensure connection is active
        time.sleep(300)  # wait 300sec before reading again
