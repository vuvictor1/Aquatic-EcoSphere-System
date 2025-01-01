# Authors: Victor Vu and Jordan Morris
# File: main_system.py
# Description: Main system file that connects to the MySQL database for sensor data
# Copyright (C) 2024 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui
from db_connection import *
from web_functions import *
from pages.contacts import contacts_page

connection = create_connection()  # Connection to MySQL database
graph_container = None  # Container to store graphs
labels = {}  # Dictionary to store sensor labels


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
                GROUP BY sensor_type)
        """)
        results = cursor.fetchall()  # store all results
        sensor_data = {row[0]: {'value': row[1], 'timestamp': row[2]}
                       for row in results}  # store results in dictionary
        return sensor_data


# Define units for each sensor type
sensor_units = {
    'total dissolved solids': 'ppm',
    'turbidity': 'NTU',
    'temperature': '°F'
}


def update_data():  # Function to update sensor labels
    data = get_latest_data()  # update to the latest data
    if data:  # If data is not empty
        for sensor_type, value in data.items():  # Iterate through each sensor to update
            # get the unit for the sensor type
            unit = sensor_units.get(sensor_type, '')
            # cut off at 2 decimal (not rounded)
            labels[sensor_type][1].set_text(f"{value['value']:.2f} {unit}")
            labels[sensor_type][2].set_text(f"{value['timestamp']}")

# Function to extract all sensor data within a specific date range


def get_all_data(start_date=None, end_date=None):
    with connection.cursor() as cursor:
        cursor.execute("SET time_zone = '-08:00';")
        if start_date is None or end_date is None:
            cursor.execute("""
                SELECT MIN(timestamp), MAX(timestamp)
                FROM sensor_data
            """)
            min_timestamp, max_timestamp = cursor.fetchone()
            start_date = start_date or min_timestamp
            end_date = end_date or max_timestamp

        cursor.execute("""
            SELECT sensor_type, value, timestamp
            FROM sensor_data
            WHERE timestamp BETWEEN %s AND %s
            ORDER BY timestamp
        """, (start_date, end_date))

        results = cursor.fetchall()
        sensor_data = {}
        for row in results:
            sensor_type = row[0]
            if sensor_type not in sensor_data:
                sensor_data[sensor_type] = []
            sensor_data[sensor_type].append(
                {'value': row[1], 'timestamp': row[2]})
        print(sensor_data)  # Debug: Print the fetched data
        return sensor_data


def generate_graphs(data=None):
    global graph_container
    print("Generating graphs...")  # Debug: Confirm function is called
    graph_container.clear()
    if data is None:
        data = get_all_data()
    if data:
        desired_order = ['total dissolved solids', 'turbidity', 'temperature']
        for sensor_type in desired_order:
            if sensor_type in data:
                values = data[sensor_type]
                timestamps = [entry['timestamp'].strftime(
                    '%m-%d %H:%M') for entry in values]
                sensor_values = [entry['value'] for entry in values]
                with graph_container:
                    ui.echart({
                        'title': {'text': sensor_type, 'textStyle': {'color': '#FFFFFF'}},
                        'tooltip': {'trigger': 'axis', 'textStyle': {'color': '#rgb(16, 15, 109)'}},
                        'xAxis': {'type': 'category', 'data': timestamps, 'axisLabel': {'color': '#FFFFFF'}},
                        'yAxis': {'type': 'value', 'axisLabel': {'color': '#FFFFFF'}},
                        'series': [{'data': sensor_values, 'type': 'line', 'name': sensor_type, 'smooth': True, 'areaStyle': {}}],
                        'toolbox': {'feature': {'saveAsImage': {}}}
                    }).style('width: 400px; height: 300px;')


def home_page():  # Define the homepage layout
    eco_header()  # call eco_header function

    # Right Drawer
    with ui.right_drawer().style('background-color: #6C757D; align-items: center;'):  # center the drawer label
        ui.label('[Notice and Disclaimer]').style(
            'color: #FFFFFF; font-size: 18px;')  # add recommendations label
        ui.label('1. Timers update periodically in intervals of 10mins. (Set to 10secs for debugging and testing only)').style(
            'color: #FFFFFF; font-size: 14px;')
        ui.label('2. Recommendations are suggestions, not mandatory.').style(
            'color: #FFFFFF; font-size: 14px;')
        ui.label('3. Specifiy species before proceeding, overwise default values will be used.').style(
            'color: #FFFFFF; font-size: 14px;')
        ui.label('4. Graphs update only a startup but can be refreshed with the button').style(
            'color: #FFFFFF; font-size: 14px;')
        ui.label('TBA...').style('color: #FFFFFF; font-size: 14px;')

    inject_style()  # call inject_style function

    # Main title
    with ui.row().style('justify-content: center; width: 100%'):
        ui.label('Aquatic EcoSphere System').style(
            'color: #FFFFFF; font-size: 32px;')  # add welcome label

    # Sensor Cards
    global labels  # global variable
    labels = {}  # dictionary to store sensor labels
    with ui.row().style('justify-content: center; width: 100%;'):  # center the sensor cards
        # iterate through each sensor type
        for sensor_type in ['total dissolved solids', 'turbidity', 'temperature']:
            with ui.column().style('background-color: #2C2C2C; padding: 20px; border-radius: 10px; width: 200px; margin: 10px; align-items: center;'):
                sensor_label = ui.label(f'{sensor_type}').style(
                    'color: #FFFFFF; font-weight: bold; ')  # add sensor label
                value_label = ui.label(f'{sensor_type} Value: Loading...').style(
                    'color: #FFFFFF;')  # add value label
                timestamp_label = ui.label(f'{sensor_type} Timestamp: Loading...').style(
                    'color: #FFFFFF;')  # add timestamp label
                # store labels in dictionary
                labels[sensor_type] = (
                    sensor_label, value_label, timestamp_label)

    # Additional Cards for Alert, Reminder, Recommendation
    with ui.row().style('justify-content: center; width: 100%; margin-top: 20px;'):
        for card_type in ['Alerts', 'Reminders', 'Recommendations']:
            with ui.column().style('background-color: #2C2C2C; padding: 20px; border-radius: 10px; width: 200px; margin: 10px; align-items: center;'):
                ui.label(card_type).style('color: #FFFFFF; font-weight: bold;')
                ui.label(f'{card_type} Content: WIP...').style(
                    'color: #FFFFFF;')

    global graph_container
    graph_container = ui.row().style(
        'justify-content: center; width: 100%;')  # container for graphs
    generate_graphs()  # generate graphs

    # Refresh graphs button
    with ui.row().style('justify-content: center; width: 100%;'):
        ui.button('Refresh Graphs', on_click=generate_graphs).style(
            'background-color: #3AAFA9; color: #FFFFFF;')

    eco_footer()  # call eco_footer function

    ui.timer(10, update_data)  # update data every 10s just for testing


@ui.page('/')  # Set homepage route
def home():
    home_page()  # call home_page function


# run the UI with tab name and logo
ui.run(title="Aquatic EcoSphere", favicon="🌊")
