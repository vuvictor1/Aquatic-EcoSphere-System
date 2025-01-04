# Authors: Victor Vu and Jordan Morris
# File: data_functions.py
# Description: Contains functions for fetching and updating sensor data, and generating graphs
# Copyright (C) 2024 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from db_connection import create_connection
from nicegui import ui

connection = create_connection() # Connection to MySQL database

sensor_units = { # Define units for each sensor type
    'total dissolved solids': 'ppm',
    'turbidity': 'NTU',
    'temperature': '°F'
}

def get_latest_data(): # Function to extract the latest sensor data
    with connection.cursor() as cursor: # Use cursor to execute SQL queries
        cursor.execute("SET time_zone = '-08:00';") # set timezone to PST
        cursor.execute("""
            SELECT sensor_type, value, timestamp
            FROM sensor_data
            WHERE (sensor_type, timestamp) IN (
                SELECT sensor_type, MAX(timestamp)
                FROM sensor_data
                GROUP BY sensor_type)
        """) # query to extract the latest sensor data
        results = cursor.fetchall() # fetch all results
        sensor_data = {row[0]: {'value': row[1], 'timestamp': row[2]} for row in results} # store results in dictionary
        return sensor_data 


def get_all_data(start_date=None, end_date=None): # Function to extract all sensor data
    with connection.cursor() as cursor: # Use cursor to execute SQL queries
        cursor.execute("SET time_zone = '-08:00';")
        if start_date is None or end_date is None: # If no date provided get min and max timestamps
            cursor.execute("""
                SELECT MIN(timestamp), MAX(timestamp)
                FROM sensor_data
            """)
            min_timestamp, max_timestamp = cursor.fetchone() # fetch min and max timestamps
            start_date = start_date or min_timestamp # set start date to min timestamp if not provided
            end_date = end_date or max_timestamp # set end date to max timestamp if not provided
        cursor.execute("""
            SELECT sensor_type, value, timestamp
            FROM sensor_data
            WHERE timestamp BETWEEN %s AND %s
            ORDER BY timestamp
        """, (start_date, end_date)) # query to extract all data within specified range

        results = cursor.fetchall()
        sensor_data = {} # store results in dictionary
        for row in results: # Iterate through results
            sensor_type = row[0] # extract sensor type
            if sensor_type not in sensor_data: # if sensor type not in dictionary add it
                sensor_data[sensor_type] = [] 
            sensor_data[sensor_type].append({'value': row[1], 'timestamp': row[2]}) # append value and timestamp
        return sensor_data 

def update_data(labels): # Function to update sensor labels with the latest data
    data = get_latest_data() 
    if data: # If data is not empty
        for sensor_type, value in data.items(): # Iterate through data
            unit = sensor_units.get(sensor_type, '')
            labels[sensor_type][1].set_text(f"{value['value']:.2f} {unit}")
            labels[sensor_type][2].set_text(f"{value['timestamp']}")

def generate_graphs(graph_container, data=None): # Function to generate graphs
    graph_container.clear() # reset the graph container
    if data is None: # If data is not provided get all data
        data = get_all_data() 
    if data: # If data is not empty
        desired_order = ['total dissolved solids', 'turbidity', 'temperature'] 
        for sensor_type in desired_order:
            if sensor_type in data: 
                values = data[sensor_type] # extract values for sensor type
                timestamps = [entry['timestamp'].strftime('%m-%d %H:%M') for entry in values] 
                sensor_values = [entry['value'] for entry in values] 

                sorted_values = sorted(sensor_values) # calculate sorted values quartiles
                q1 = sorted_values[int(0.25 * len(sorted_values))] # 25th percentile
                q3 = sorted_values[int(0.75 * len(sorted_values))] # 75th percentile
                iqr = q3 - q1 # interquartile range
                lower_bound = q1 - 1.5 * iqr # lower bound for outliers
                upper_bound = q3 + 1.5 * iqr # upper bound for outliers

                filtered_values = [ # Filter out outliers
                    value for value in sensor_values if lower_bound <= value <= upper_bound]

                # Calculate the range for the y-axis using filtered values
                max_value = max(sensor_values) 
                min_value = min(filtered_values) if filtered_values else min(sensor_values) 
                range_value = max_value - min_value 
                distance_padding = 0.10 # multiplied against the range for scaling
                y_min = max(0, min_value - distance_padding * range_value) # y-axis min value
                y_max = max_value + distance_padding * range_value # y-axis max value

                # Debugging: Print max and min values for each sensor type
                """ print(f"Sensor Type: {sensor_type}")
                print(f"Original Max Value: {max(sensor_values)}")
                print(f"Original Min Value: {min(sensor_values)}")
                # print(f"Filtered Max Value: {max_value}")
                print(f"Filtered Min Value: {min_value}")
                print(f"Range Value: {range_value}")
                print(f"Y-Min: {y_min}")
                print(f"Y-Max: {y_max}")
                print("-" * 40) """

                with graph_container: # Create a graph for each sensor type
                    ui.echart({ # Create an echart graph
                        'title': {'text': sensor_type, 'textStyle': {'color': '#FFFFFF'}}, 
                        'tooltip': {'trigger': 'axis', 'textStyle': {'color': '#rgb(16, 15, 109)'}},
                        'xAxis': {'type': 'category', 'data': timestamps, 'axisLabel': {'color': '#FFFFFF'}},
                        'yAxis': {
                            'type': 'value',
                            'axisLabel': {'color': '#FFFFFF'}, 
                            'min': round(y_min, 0),
                            'max': round(y_max, 0)
                        },
                        'series': [{'data': sensor_values, 'type': 'line', 'name': sensor_type, 'smooth': True, 'areaStyle': {}}], # line graph
                        'toolbox': {'feature': {'saveAsImage': {}}} # save as image feature
                    }).style('width: 400px; height: 300px;') # set graph dimensions