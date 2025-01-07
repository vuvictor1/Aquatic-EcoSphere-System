# Authors: Victor Vu 
# File: contacts.py
# Description: Graphing page for the web interface
# Copyright (C) 2024 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui
from datetime import datetime
from web_functions import inject_style, eco_header, eco_footer
from collect_database import get_all_data

def generate_graphs(graph_container, data=None): # Generate graphs for sensor data
    graph_container.clear() # reset the graph container
    if data is None: # Fetch all data if none is provided
        data = get_all_data() 

    if data: # Generate graphs if data is available
        desired_order = ['total dissolved solids', 'turbidity', 'temperature'] 
        for sensor_type in desired_order: 
            if sensor_type in data: # Check if sensor type is in the data
                values = data[sensor_type] # get values for the sensor type
                timestamps = [entry['timestamp'].strftime('%m-%d %H:%M') for entry in values] # extract timestamps
                sensor_values = [entry['value'] for entry in values] # extract sensor values

                # Calculate y-axis range
                sorted_values = sorted(sensor_values) # sort values
                q1 = sorted_values[int(0.25 * len(sorted_values))] # 25th percentile
                q3 = sorted_values[int(0.75 * len(sorted_values))] # 75th percentile
                iqr = q3 - q1 # interquartile range
                lower_bound = q1 - 1.5 * iqr # lower bound for outliers
                filtered_values = [value for value in sensor_values if lower_bound <= value] # filter out outliers

                # Calculate y-axis range using filtered values
                min_value = min(filtered_values) if filtered_values else 0 # minimum value
                max_value = max(filtered_values) if filtered_values else 1 # maximum value
                distance_padding = 0.10 # padding for y-axis
                y_min = max(0, min_value - distance_padding *(max_value - min_value)) # minimum y-axis value
                y_max = max_value + distance_padding * (max_value - min_value) # maximum y-axis value

                with graph_container: # Create a graph for each sensor type
                    ui.echart({ # Create an echart object
                        'title': {'text': sensor_type, 'textStyle': {'color': '#FFFFFF'}},
                        'tooltip': {'trigger': 'axis', 'textStyle': {'color': '#rgb(16, 15, 109)'}},
                        'xAxis': {'type': 'category', 'data': timestamps, 'axisLabel': {'color': '#FFFFFF'}},
                        'yAxis': { # Y-axis configuration
                            'type': 'value',
                            'axisLabel': {'color': '#FFFFFF'},
                            'min': round(y_min, 0),
                            'max': round(y_max, 0)
                        },
                        'series': [{ # Series configuration
                            'data': sensor_values,
                            'type': 'line',
                            'name': sensor_type,
                            'smooth': True,
                            'areaStyle': {} 
                        }], # create a line graph
                        'toolbox': {'feature': {'saveAsImage': {}}}, # save as image feature
                         'dataZoom': [{ # Zoom feature for zooming
                            'type': 'slider',
                            'start': 0,
                            'end': 100
                        }]
                    }).style('width: 400px; height: 300px;') # set width and height of the graph

def graphs_page(graph_container, labels): # Graphs page function
    eco_header() # header menu
    inject_style() # inject CSS for background

    with ui.row().style('justify-content: center; width: 100%; margin-top: 20px;'):
        ui.label('Graphing').style('font-size: 32px; color: white;') # Add title

    with ui.dialog() as date_dialog: # Date range selection dialog
        with ui.column().style('background-color: #2C2C2C; padding: 40px; border-radius: 10px;'): # Box container
            ui.label('Select Date Range:').style('color: #FFFFFF; font-size: 20px; background-color: #333333; padding: 20px;')
            date_input = ui.input('Date range').style('display: none;') # get date input but don't display to user
            current_date = datetime.now().strftime('%Y/%m') # read current date
            current_date_limit = datetime.now().strftime('%Y/%m/%d') # get current date max filter
            start_date_limit = '2025/01/05' # minimum date limit for filter based on data collected
            date_picker = ui.date().props(f'default-year-month={current_date} :options="date => date >= \'{start_date_limit}\' && date <= \'{current_date_limit}\'"') # date menu

            def update_date_input(): # Update date input based on selected range
                selected_range = date_picker.value # get selected range
                date_input.value = f"{selected_range['from']} - {selected_range['to']}" if selected_range and 'from' in selected_range and 'to' in selected_range else None
            date_picker.on('update:model-value', update_date_input) # update date input based on calendar selection

            with ui.row().style('margin-top: 10px;'): # Filter data button
                ui.button('Filter Data', on_click=lambda: (
                    generate_graphs(graph_container, get_all_data(
                        *date_input.value.split(' - ')) if date_input.value else get_all_data()),
                    date_dialog.close()
                )).style('background-color: #3AAFA9; color: #FFFFFF; margin-top: 10px;')

    with ui.row().style('justify-content: center; width: 100%; margin-top: 20px;'): # Select date range button
        ui.button('Select Date Range', on_click=lambda: date_dialog.open()).style(
            'background-color: #3AAFA9; color: #FFFFFF; margin-top: 10px;')

    graph_container = ui.row().style('justify-content: center; width: 100%;') # graph container
    generate_graphs(graph_container) # call generate graphs

    with ui.row().style('justify-content: center; width: 100%;'): # Refresh graphs button
        ui.button('Refresh Graphs', on_click=lambda: generate_graphs(
            graph_container)).style('background-color: #3AAFA9; color: #FFFFFF;')
    eco_footer() # footer menu
        
@ui.page('/graphs') # Route to graphs page
def graphs():
    from main_system import graph_container, labels # import globals
    graphs_page(graph_container, labels) # pass global to graphs page