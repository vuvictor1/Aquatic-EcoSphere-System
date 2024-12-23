# Author: Victor Vu
# File: main_system.py
# Description: Main system file that connects to the MySQL database for sensor data
# Copyright (C) 2024 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
import pymysql
from dotenv import load_dotenv
import os
from urllib.parse import urlparse
from nicegui import ui

load_dotenv() # Load environment variables from .env

# Parse database URL from .env file
db_url = os.getenv('DATABASE_URL')
parsed_url = urlparse(db_url)

# Establish MySQL connection 
connection = pymysql.connect( 
    host=parsed_url.hostname,
    user=parsed_url.username,
    password=parsed_url.password,
    database=parsed_url.path[1:], 
    port=parsed_url.port,
    autocommit=True # enable autocommit to refresh data
)

def get_latest_data(): # Function to extract current latest sensor data
    with connection.cursor() as cursor: # cursor object to interact with db
        # Query to get latest data for each sensor type
        cursor.execute(""" 
            SELECT sensor_type, value, timestamp
            FROM sensor_data
            WHERE (sensor_type, timestamp) IN (
                SELECT sensor_type, MAX(timestamp) 
                FROM sensor_data
                GROUP BY sensor_type
            )
        """)
        results = cursor.fetchall() # store all results
        sensor_data = {row[0]: {'value': row[1], 'timestamp': row[2]} for row in results} # store results in dictionary
        return sensor_data 

def update_data(): # Function to update sensor labels
    data = get_latest_data() # update to the latest data
    if data: # If data is not empty
        for sensor_type, value in data.items(): # Iterate through each sensor to update
            labels[sensor_type][1].set_text(f"Value: {value['value']:.2f}") # cut off to 2 decimal places (not rounded)
            labels[sensor_type][2].set_text(f"Timestamp: {value['timestamp']}")

labels = {} # dictionary to store sensor labels

# Create UI elements for each sensor type
with ui.row().style('display: flex; justify-content: center; align-items: center; width: 100%;'): # Center the row
    for sensor_type in ['total dissolved solids', 'turbidity', 'temperature']: 
        with ui.column().style('display: flex; align-items: center;'): # Center the column
            sensor_label = ui.label(f'Sensor Type: {sensor_type}') # create sensor label
            value_label = ui.label(f'{sensor_type} Value: Loading...') # create value label
            timestamp_label = ui.label(f'{sensor_type} Timestamp: Loading...') # create timestamp label
            labels[sensor_type] = (sensor_label, value_label, timestamp_label) # store labels in dictionary

ui.timer(600, update_data) # update data every 600ms
ui.run() # run the UI