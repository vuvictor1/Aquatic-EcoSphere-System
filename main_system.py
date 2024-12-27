# Authors: Victor Vu and Jordan Morris
# File: main_system.py
# Description: Main system file that connects to the MySQL database for sensor data
# Copyright (C) 2024 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui
from db_connection import create_connection 

connection = create_connection() # Connection to MySQL database

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
                GROUP BY sensor_type)
        """)
        results = cursor.fetchall() # store all results 
        sensor_data = {row[0]: {'value': row[1], 'timestamp': row[2]} for row in results} # store results in dictionary 
        return sensor_data

# Define units for each sensor type
sensor_units = {
    'total dissolved solids': 'ppm',
    'turbidity': 'NTU',
    'temperature': '°F'
}
def update_data(): # Function to update sensor labels
    data = get_latest_data() # update to the latest data
    if data: # If data is not empty
        for sensor_type, value in data.items(): # Iterate through each sensor to update
            unit = sensor_units.get(sensor_type, '') # get the unit for the sensor type
            labels[sensor_type][1].set_text(f"{value['value']:.2f} {unit}") # cut off at 2 decimal (not rounded)
            labels[sensor_type][2].set_text(f"{value['timestamp']}")

def get_all_data(): # Function to extract all sensor data
    with connection.cursor() as cursor: 
        cursor.execute("SET time_zone = '-08:00';") 
        cursor.execute("""
            SELECT sensor_type, value, timestamp
            FROM sensor_data
            ORDER BY timestamp
        """)
        results = cursor.fetchall() # store all results
        sensor_data = {} 

        for row in results: # Add data to sensor_data dictionary
            sensor_type = row[0] 
            if sensor_type not in sensor_data: 
                sensor_data[sensor_type] = [] 
            sensor_data[sensor_type].append({'value': row[1], 'timestamp': row[2]}) 
        return sensor_data

def generate_graphs(): # Function to generate graphs for each sensor type
    data = get_all_data() # get all data
    if data: # If data is not empty

        # Define the desired order of sensor types
        desired_order = ['total dissolved solids', 'turbidity', 'temperature']
        for sensor_type in desired_order: 
            if sensor_type in data: 
                values = data[sensor_type] 
                # Process timestamps to remove the year
                timestamps = [entry['timestamp'].strftime('%m-%d %H:%M') for entry in values] # Extract month, day, and time
                sensor_values = [entry['value'] for entry in values]
                padding = 0.2 # 20% padding for the graph range 

                if sensor_values: 
                    min_sensor_value = min(sensor_values) # get the minimum sensor value
                    max_sensor_value = max(sensor_values) # get the maximum sensor value
                    range_value = max_sensor_value - min_sensor_value # range of sensor values
                    # Calculate the minimum value with padding, ensuring it does not go below 0
                    min_value = round(max(min_sensor_value - (range_value * padding), 0), 1) 
                else: # If no data available set default value
                    min_value = 0

                ui.echart({ # Create the graphs
                    'title': {
                        'text': sensor_type,
                        'textStyle': { 
                            'color': '#FFFFFF' # set text color to white
                        }
                    },
                    'tooltip': {
                        'trigger': 'axis',
                        'textStyle': { 
                            'color': '#rgb(16, 15, 109)' # set tooltip text color to white
                        }
                    },
                    'xAxis': {
                        'type': 'category',
                        'data': timestamps, # Use the processed timestamps without year
                        'axisLabel': { # Add axis label style
                            'color': '#FFFFFF' # set x-axis label color to white
                        }
                    },
                    'yAxis': {
                        'type': 'value',
                        'min': min_value, # set min value for y-axis
                        'axisLabel': { 
                            'color': '#FFFFFF' 
                        }
                    },
                    'series': [{ # Add series to the graph
                        'data': sensor_values,
                        'type': 'line',
                        'name': sensor_type,
                        'smooth': True,
                        'areaStyle': {}
                    }],
                    'toolbox': { # Add toolbox to the graph
                        'feature': {
                            'saveAsImage': {} # add save as image feature
                        }
                    }
                }).style('width: 400px; height: 300px;') # set graph size

# Header menu
with ui.header().style('background-color: #3AAFA9;'): 
    ui.label('🌊 Homepage').style('color: #FFFFFF; font-size: 24px;')
    ui.button(icon='account_circle') # add account button
    ui.button(icon='menu') # add menu button

# Right Drawer
with ui.right_drawer().style('background-color: #6C757D; align-items: center;'): # center the drawer label
    ui.label('[Recommendations]').style('color: #FFFFFF; font-size: 18px;') # add recommendations label

# Inject html with css inside for background of main page
ui.add_head_html("""
<style>
    body {
        background-color: #3B3B3B; /* change to gray */
    }
</style>
""")

# Main title
with ui.row().style('justify-content: center; width: 100%'):
    ui.label('Aquatic EcoSphere System').style('color: #FFFFFF; font-size: 32px;') # add welcome label

# Sensor Cards
labels = {} # dictionary to store sensor labels
with ui.row().style('justify-content: center; width: 100%;'): # center the sensor cards
    for sensor_type in ['total dissolved solids', 'turbidity', 'temperature']: # iterate through each sensor type
        with ui.column().style('background-color: #2C2C2C; padding: 20px; border-radius: 10px; width: 200px; margin: 10px; align-items: center;'):
            sensor_label = ui.label(f'{sensor_type}').style('color: #FFFFFF; font-weight: bold; ') # add sensor label
            value_label = ui.label(f'{sensor_type} Value: Loading...').style('color: #FFFFFF;') # add value label
            timestamp_label = ui.label(f'{sensor_type} Timestamp: Loading...').style('color: #FFFFFF;') # add timestamp label
            labels[sensor_type] = (sensor_label, value_label, timestamp_label) # store labels in dictionary

# Generate graphs
with ui.row().style('justify-content: center; width: 100%;'):
    generate_graphs()

# Footer and copyright
with ui.footer().style('background-color: #3AAFA9; justify-content: center;'):
    ui.label('Copyright (C) 2024 | Victor Vu & Jordan Morris').style('color: #FFFFFF; font-size: 18px;')

ui.timer(10, update_data) # update data every 10s just for testing
ui.run(title="Aquatic EcoSphere", favicon="🌊") # run the UI with tab name and logo