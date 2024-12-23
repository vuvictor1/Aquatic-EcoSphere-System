# database.py
import pandas as pd
from sqlalchemy import create_engine


def get_database_connection():
    # Database configuration
    db_config = {
        'user': 'root',
        'password': 'ZAJDlxblTEhBCDhOsvxwwQDXjWWCfPoR',
        'host': 'autorack.proxy.rlwy.net',
        'port': 22542,
        'database': 'railway'
    }
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
