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

# Inject CSS to change the background color of the entire page
ui.add_head_html("""
<style>
    body {
        background-color: #3B3B3B; /* Change to black */
    }
    .dashboard-header {
        background-color: #3AAFA9;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
    }
    .dashboard-footer {
        background-color: #3AAFA9;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px 20px;
    }
    .dashboard-content {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
        padding: 20px;
    }
    .sensor-card {
        background-color: #2C2C2C;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        width: 200px;
    }
</style>
""")

# Header
with ui.header().classes('dashboard-header'):
    ui.label('Homepage').style('text-align: center; color: white; font-size: 24px;')
    ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')

# Right Drawer
with ui.right_drawer(fixed=False).style('background-color: #6C757D').props('bordered') as right_drawer:
    ui.label('Recommendation:').style('text-align: center; color: white;')

# Main Content
with ui.row().classes('dashboard-content'):
    ui.markdown('<h1 style="color:white; text-align: center;">Welcome to Aquatic EcoSphere System</h1>')

# Sensor Cards
labels = {} # dictionary to store sensor labels
with ui.row().classes('dashboard-content'):
    for sensor_type in ['total dissolved solids', 'turbidity', 'temperature']: 
        with ui.column().classes('sensor-card'):
            sensor_label = ui.label(f'Sensor Type: {sensor_type}').style('color: white; font-weight: bold;')
            value_label = ui.label(f'{sensor_type} Value: Loading...').style('color: white;')
            timestamp_label = ui.label(f'{sensor_type} Timestamp: Loading...').style('color: white;')
            labels[sensor_type] = (sensor_label, value_label, timestamp_label)

# Footer
with ui.footer().classes('dashboard-footer'):
    ui.label('Copyright 2024 of Victor Vu and Jordan Morris').style('text-align: center; font-weight: bold; color: white;')

ui.timer(600, update_data) # update data every 600ms
ui.run() # run the UI
