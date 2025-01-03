# Authors: Victor Vu and Jordan Morris
# File: data_functions.py
# Description: Contains functions for fetching and updating sensor data, and generating graphs
# Copyright (C) 2024 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from db_connection import create_connection
from nicegui import ui

connection = create_connection()  # Connection to MySQL database

# Define units for each sensor type
sensor_units = {
    'total dissolved solids': 'ppm',
    'turbidity': 'NTU',
    'temperature': '°F'
}


def get_latest_data():
    """Function to extract the latest sensor data."""
    with connection.cursor() as cursor:
        cursor.execute("SET time_zone = '-08:00';")
        cursor.execute("""
            SELECT sensor_type, value, timestamp
            FROM sensor_data
            WHERE (sensor_type, timestamp) IN (
                SELECT sensor_type, MAX(timestamp)
                FROM sensor_data
                GROUP BY sensor_type)
        """)
        results = cursor.fetchall()
        sensor_data = {row[0]: {'value': row[1],
                                'timestamp': row[2]} for row in results}
        return sensor_data


def get_all_data(start_date=None, end_date=None):
    """Function to extract all sensor data within a specific date range."""
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
        return sensor_data


def update_data(labels):
    """Function to update sensor labels with the latest data."""
    data = get_latest_data()
    if data:
        for sensor_type, value in data.items():
            unit = sensor_units.get(sensor_type, '')
            labels[sensor_type][1].set_text(f"{value['value']:.2f} {unit}")
            labels[sensor_type][2].set_text(f"{value['timestamp']}")


def generate_graphs(graph_container, data=None):
    """Function to generate graphs based on sensor data with dynamic y-axis range, ignoring outliers."""
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

                # Calculate quartiles and IQR to identify outliers
                sorted_values = sorted(sensor_values)
                # First quartile (25th percentile)
                q1 = sorted_values[int(0.25 * len(sorted_values))]
                # Third quartile (75th percentile)
                q3 = sorted_values[int(0.75 * len(sorted_values))]
                iqr = q3 - q1  # Interquartile range
                lower_bound = q1 - 1.5 * iqr  # Lower bound for outliers
                upper_bound = q3 + 1.5 * iqr  # Upper bound for outliers

                # Filter out outliers
                filtered_values = [
                    value for value in sensor_values if lower_bound <= value <= upper_bound]

                # Calculate the range for the y-axis using filtered values
                max_value = max(sensor_values)
                min_value = min(filtered_values) if filtered_values else min(
                    sensor_values)
                range_value = max_value - min_value
                distance_padding = 0.10  # Multiplied against the range for scaling
                y_min = max(0, min_value - distance_padding * range_value)
                y_max = max_value + distance_padding * range_value

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

                with graph_container:
                    ui.echart({
                        'title': {'text': sensor_type, 'textStyle': {'color': '#FFFFFF'}},
                        'tooltip': {'trigger': 'axis', 'textStyle': {'color': '#rgb(16, 15, 109)'}},
                        'xAxis': {'type': 'category', 'data': timestamps, 'axisLabel': {'color': '#FFFFFF'}},
                        'yAxis': {
                            'type': 'value',
                            'axisLabel': {'color': '#FFFFFF'},
                            'min': round(y_min, 0),
                            'max': round(y_max, 0)
                        },
                        'series': [{'data': sensor_values, 'type': 'line', 'name': sensor_type, 'smooth': True, 'areaStyle': {}}],
                        'toolbox': {'feature': {'saveAsImage': {}}}
                    }).style('width: 400px; height: 300px;')
