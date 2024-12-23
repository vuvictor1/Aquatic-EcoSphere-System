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
        cursor.execute("SET time_zone = '-08:00';") # set timezone to PST
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

def get_all_data(): # Function to extract all sensor data
    with connection.cursor() as cursor: # cursor object to interact with db
        cursor.execute("SET time_zone = '-08:00';") # set timezone to PST
        # Query to get all data for each sensor type
        cursor.execute(""" 
            SELECT sensor_type, value, timestamp
            FROM sensor_data
            ORDER BY timestamp
        """)
        results = cursor.fetchall() # store all results
        sensor_data = {}
        for row in results:
            sensor_type = row[0]
            if sensor_type not in sensor_data:
                sensor_data[sensor_type] = []
            sensor_data[sensor_type].append({'value': row[1], 'timestamp': row[2]})
        return sensor_data 

def generate_graphs(): # Function to generate graphs for each sensor type
    data = get_all_data() # get all data
    if data: # If data is not empty
        for sensor_type, values in data.items(): # Iterate through each sensor to generate graph
            timestamps = [entry['timestamp'] for entry in values]
            sensor_values = [entry['value'] for entry in values]
            ui.echart({
                'title': {
                    'text': sensor_type
                },
                'tooltip': {
                    'trigger': 'axis'
                },
                'xAxis': {
                    'type': 'category',
                    'data': timestamps
                },
                'yAxis': {
                    'type': 'value'
                },
                'series': [{
                    'data': sensor_values,
                    'type': 'line',
                    'name': sensor_type,
                    'smooth': True,
                    'areaStyle': {}
                }],
                'toolbox': {
                    'feature': {
                        'saveAsImage': {}
                    }
                }
            }).style('width: 400px; height: 300px;')

# Inject CSS to change the background color of the entire page
ui.add_head_html("""
<style>
    body {
        background-color: #3B3B3B; /* Change to black */
    }
</style>
""")

# Header
with ui.header().style('background-color: #3AAFA9;'):
    ui.label('Homepage').style('color: white; font-size: 24px;')
    ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')

# Right Drawer
with ui.right_drawer(fixed=False).style('background-color: #6C757D; display: flex; align-items: center;').props('bordered') as right_drawer:
    ui.label('[Recommendations]').style('color: white; font-size: 18px;')

# Main Content
with ui.row().style('display: flex; justify-content: center; align-items: center; width: 100%;'):
    ui.label('Welcome to Aquatic EcoSphere System').style('color: white; font-size: 32px; text-align: center;')

# Sensor Cards
labels = {} # dictionary to store sensor labels
with ui.row().style('display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 20px; padding: 20px; width: 100%;'):
    for sensor_type in ['total dissolved solids', 'turbidity', 'temperature']: 
        with ui.column().style('background-color: #2C2C2C; padding: 20px; border-radius: 10px; text-align: center; color: white; width: 200px; margin: 10px;'):
            sensor_label = ui.label(f'{sensor_type}').style('color: white; font-weight: bold; ')
            value_label = ui.label(f'{sensor_type} Value: Loading...').style('color: white;')
            timestamp_label = ui.label(f'{sensor_type} Timestamp: Loading...').style('color: white;')
            labels[sensor_type] = (sensor_label, value_label, timestamp_label)

# Generate Graphs below the sensor cards
with ui.row().style('display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 20px; padding: 20px; width: 100%;'):
    generate_graphs()

# Footer
with ui.footer().style('background-color: #3AAFA9; display: flex; justify-content: center; align-items: center;'):
    ui.label('Copyright 2024 of Victor Vu and Jordan Morris').style('color: white; font-size: 16px;')

ui.timer(600, update_data) # update data every 600ms
ui.run() # run the UI