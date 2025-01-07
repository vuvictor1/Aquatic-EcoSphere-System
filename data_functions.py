# Authors: Victor Vu and Jordan Morris
# File: data_functions.py
# Description: Contains functions for fetching and updating sensor data, and generating graphs
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from db_connection import create_connection
from nicegui import ui

connection = create_connection() # connection to MySQL database
sensor_units = { # sensor_type: unit
    'total dissolved solids': 'ppm',
    'turbidity': 'NTU',
    'temperature': '°F'
}
def get_latest_data(): # Fetch latest sensor data for each type
    with connection.cursor() as cursor: # Create a cursor object
        cursor.execute("SET time_zone = '-08:00';") # set timezone to PST
        # Execute a query to fetch data 
        cursor.execute("""
            SELECT sensor_type, value, timestamp
            FROM sensor_data
            WHERE (sensor_type, timestamp) IN (
                SELECT sensor_type, MAX(timestamp)
                FROM sensor_data
                GROUP BY sensor_type
            )
        """)
        results = cursor.fetchall() # fetch all rows
        sensor_data = {row[0]: {'value': row[1],'timestamp': row[2]} for row in results} # store data in a dictionary
        return sensor_data

def get_all_data(start_date=None, end_date=None): # Fetch all  data within a specified range
    with connection.cursor() as cursor: 
        cursor.execute("SET time_zone = '-08:00';")
        if start_date is None or end_date is None: # Fetch min and max timestamps if no range provided
            cursor.execute("""
                SELECT MIN(timestamp), MAX(timestamp)
                FROM sensor_data
            """)
            min_timestamp, max_timestamp = cursor.fetchone() 
            start_date = start_date or min_timestamp # set start date to min timestamp if not provided
            end_date = end_date or max_timestamp # set end date to max timestamp if not provided

        # Fetch data within the specified date range
        cursor.execute("""
            SELECT sensor_type, value, timestamp
            FROM sensor_data
            WHERE timestamp BETWEEN %s AND %s
            ORDER BY timestamp
        """, (start_date, end_date)) # pass in the start and end date
        results = cursor.fetchall() # fetch all rows
        sensor_data = {} # empty dictionary to store data

        for row in results: # Iterate each row and store in dictionary
            sensor_type = row[0] # sensor type
            if sensor_type not in sensor_data: # check if sensor type is in the dictionary
                sensor_data[sensor_type] = [] # create a list for each sensor type
            sensor_data[sensor_type].append({'value': row[1], 'timestamp': row[2]}) # append data to the list
        return sensor_data

def update_data(labels): # Update sensor labels with the latest data
    data = get_latest_data() 
    if data: # Update labels if data is available
        for sensor_type, value in data.items(): # Iterate through each type and value label
            unit = sensor_units.get(sensor_type, '') # get unit for sensor type
            labels[sensor_type][1].set_text(f"{value['value']:.2f} {unit}")
            labels[sensor_type][2].set_text(f"{value['timestamp']}")

