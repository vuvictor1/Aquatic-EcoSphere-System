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
    """Function to generate graphs based on sensor data."""
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
