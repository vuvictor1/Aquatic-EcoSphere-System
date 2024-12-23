# Author: Victor Vu
# File: main_system.py
# Description: Main system file that connects to the MySQL database for sensor data
# Copyright (C) 2024 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui
from db_connection import create_connection  # Import the connection function

# Establish MySQL connection
connection = create_connection()

def get_latest_data():  # Function to extract current latest sensor data
    with connection.cursor() as cursor:  # cursor object to interact with db
        cursor.execute("SET time_zone = '-08:00';")  # set timezone to PST
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
        results = cursor.fetchall()  # store all results
        sensor_data = {row[0]: {'value': row[1], 'timestamp': row[2]}
                       for row in results}  # store results in dictionary
        return sensor_data


def update_data():  # Function to update sensor labels
    data = get_latest_data()  # update to the latest data
    if data:  # If data is not empty
        for sensor_type, value in data.items():  # Iterate through each sensor to update
            # cut off to 2 decimal places (not rounded)
            labels[sensor_type][1].set_text(f"Value: {value['value']:.2f}")
            labels[sensor_type][2].set_text(f"Timestamp: {value['timestamp']}")


def get_all_data():  # Function to extract all sensor data
    with connection.cursor() as cursor:  # cursor object to interact with db
        cursor.execute("SET time_zone = '-08:00';")  # set timezone to PST
        # Query to get all data for each sensor type
        cursor.execute("""
            SELECT sensor_type, value, timestamp
            FROM sensor_data
            ORDER BY timestamp
        """)
        results = cursor.fetchall()  # store all results
        sensor_data = {}
        for row in results:
            sensor_type = row[0]
            if sensor_type not in sensor_data:
                sensor_data[sensor_type] = []
            sensor_data[sensor_type].append(
                {'value': row[1], 'timestamp': row[2]})
        return sensor_data


def generate_graphs():  # Function to generate graphs for each sensor type
    data = get_all_data()  # get all data
    if data:  # If data is not empty
        # Define the desired order of sensor types
        desired_order = ['total dissolved solids', 'turbidity', 'temperature']
        for sensor_type in desired_order:  # Iterate through each sensor in the desired order
            if sensor_type in data:
                values = data[sensor_type]
                timestamps = [entry['timestamp'] for entry in values]
                sensor_values = [entry['value'] for entry in values]

                # Define padding as a percentage of the range
                padding = 0.1
                if sensor_values:
                    # Calculate the minimum value for the graph
                    # Subtract padding from the minimum sensor value to ensure the graph has some space
                    min_sensor_value = min(sensor_values)
                    max_sensor_value = max(sensor_values)
                    # Calculate the range of sensor values
                    range_value = max_sensor_value - min_sensor_value

                    # Calculate the minimum value with padding, ensuring it does not go below 0
                    min_value = round(
                        max(min_sensor_value - (range_value * padding), 0), 1)

                    # Calculate the maximum value with padding
                    max_value = round(max_sensor_value +
                                      (range_value * padding), 1)
                else:
                    min_value = 0
                    max_value = 100

                ui.echart({
                    'title': {
                        'text': sensor_type,
                        'textStyle': {  # Add text style for title
                            'color': '#FFFFFF'  # Set title text color to white
                        }
                    },
                    'tooltip': {
                        'trigger': 'axis',
                        'textStyle': {  # Add text style for tooltip
                            # Set tooltip text color to white
                            'color': '#rgb(16, 15, 109)'
                        }
                    },
                    'xAxis': {
                        'type': 'category',
                        'data': timestamps,
                        'axisLabel': {  # Add axis label style
                            'color': '#FFFFFF'  # Set x-axis label color to white
                        }
                    },
                    'yAxis': {
                        'type': 'value',
                        'min': min_value,  # Set minimum value for y-axis
                        'max': max_value,  # Set maximum value for y-axis
                        'axisLabel': {  # Add axis label style
                            'color': '#FFFFFF'  # Set y-axis label color to white
                        }
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
    ui.label('Homepage').style('color: #FFFFFF; font-size: 24px;')
    ui.button(on_click=lambda: right_drawer.toggle(),
              icon='menu').props('flat color=white')

# Right Drawer
with ui.right_drawer(fixed=False).style('background-color: #6C757D; display: flex; align-items: center;').props('bordered') as right_drawer:
    ui.label('[Recommendations]').style('color: #FFFFFF; font-size: 18px;')

# Main Content
with ui.row().style('display: flex; justify-content: center; align-items: center; width: 100%;'):
    ui.label('Welcome to Aquatic EcoSphere System').style(
        'color: #FFFFFF; font-size: 32px; text-align: center;')

# Sensor Cards
labels = {}  # dictionary to store sensor labels
with ui.row().style('display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 20px; padding: 20px; width: 100%;'):
    for sensor_type in ['total dissolved solids', 'turbidity', 'temperature']:
        with ui.column().style('background-color: #2C2C2C; padding: 20px; border-radius: 10px; text-align: center; color: #FFFFFF; width: 200px; margin: 10px;'):
            sensor_label = ui.label(f'{sensor_type}').style(
                'color: #FFFFFF; font-weight: bold; ')
            value_label = ui.label(
                f'{sensor_type} Value: Loading...').style('color: #FFFFFF;')
            timestamp_label = ui.label(
                f'{sensor_type} Timestamp: Loading...').style('color: #FFFFFF;')
            labels[sensor_type] = (sensor_label, value_label, timestamp_label)

# Generate Graphs below the sensor cards
with ui.row().style('display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 20px; padding: 20px; width: 100%;'):
    generate_graphs()

# Footer
with ui.footer().style('background-color: #3AAFA9; display: flex; justify-content: center; align-items: center;'):
    ui.label('Copyright 2024 of Victor Vu and Jordan Morris').style(
        'color: #FFFFFF; font-size: 16px;')

ui.timer(10, update_data)  # update data every 10s just for testing
ui.run()  # run the UI
