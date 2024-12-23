# database.py
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from urllib.parse import urlparse  # Import urlparse

# Load environment variables from .env file
load_dotenv()


def get_database_connection():
    # Parse database URL from .env file
    db_url = os.getenv('DATABASE_URL')
    parsed_url = urlparse(db_url)

    # Database configuration
    db_config = {
        'user': parsed_url.username,
        'password': parsed_url.password,
        'host': parsed_url.hostname,
        'port': parsed_url.port,
        'database': parsed_url.path[1:]  # Remove leading '/'
    }

    # Check for missing environment variables
    for key, value in db_config.items():
        if value is None:
            raise ValueError(f"Missing environment variable: {key}")

    # Create the connection string
    connection_string = f"mysql+mysqlconnector://{db_config['user']}:{
        db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    engine = create_engine(connection_string)
    return engine


def fetch_sensor_data(engine):
    # Query the table
    query = "SELECT * FROM sensor_data"  # Replace with your table name
    df = pd.read_sql(query, engine)  # Use the SQLAlchemy engine
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df
