# Authors: Victor Vu and Jordan Morris
# File: contacts.py
# Description: Graphing page for the web interface
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
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
                sorted_values = sorted(sensor_values)
                q1 = sorted_values[int(0.25 * len(sorted_values))] # 25th percentile
                q3 = sorted_values[int(0.75 * len(sorted_values))] # 75th percentile
                iqr = q3 - q1 # interquartile range
                lower_bound = q1 - 1.5 * iqr # lower bound for outliers
                filtered_values = [value for value in sensor_values if lower_bound <= value]

                # Calculate y-axis range using filtered values
                min_value = min(filtered_values) if filtered_values else 0 
                max_value = max(filtered_values) if filtered_values else 1
                distance_padding = 0.10 # padding for y-axis
                y_min = max(0, min_value - distance_padding * (max_value - min_value)) 
                y_max = max_value + distance_padding * (max_value - min_value)

                with graph_container: # Create a graph container
                    ui.echart({ # Create an ECharts graph
                        'title': {'text': sensor_type, 'textStyle': {'color': '#FFFFFF'}},
                        'tooltip': {'trigger': 'axis', 'textStyle': {'color': '#rgb(16, 15, 109)'}},
                        'xAxis': {'type': 'category', 'data': timestamps, 'axisLabel': {'color': '#FFFFFF'}},
                        'yAxis': {
                            'type': 'value',
                            'axisLabel': {'color': '#FFFFFF'},
                            'min': round(y_min, 0),
                            'max': round(y_max, 0)
                        },
                        'series': [{
                            'data': sensor_values,
                            'type': 'line',
                            'name': sensor_type,
                            'smooth': True,
                            'areaStyle': {}
                        }],
                        'toolbox': {'feature': {'saveAsImage': {}}},
                    }).style('width: 400px; height: 300px;')

def graphs_page(graph_container, labels): # Graphs page for the web interface
    eco_header() # display the header
    inject_style() # inject custom CSS styles

    with ui.row().style('justify-content: center; width: 100%; margin-top: 20px;'): # Title for the page
        ui.label('Graphing').style('font-size: 32px; color: white;') 

    with ui.dialog() as date_dialog: # Create a dialog for selecting date range
        with ui.column().style('background-color: #2C2C2C; padding: 2em; border-radius: 10px;'): 
            ui.label('Select Date Range:').style('color: #FFFFFF; font-size: 1.25em; background-color: #333333; padding: 1em;') 
            date_input = ui.input('Date range').classes('w-100').style('display: none;') # hidden input for date range 

            # Create a date picker with a range of dates
            current_date = datetime.now().strftime('%Y/%m') 
            current_date_limit = datetime.now().strftime('%Y/%m/%d') 
            start_date_limit = '2025/01/12' 
            date_picker = ui.date().props(f'range default-year-month={current_date} :options="date => date >= \'{start_date_limit}\' && date <= \'{current_date_limit}\'"') 

            def update_date_input(): # Update the date input with the selected range
                selected_range = date_picker.value 
                date_input.value = f"{selected_range['from']} - {selected_range['to']}" if selected_range and 'from' in selected_range and 'to' in selected_range else None
            date_picker.on('update:model-value', update_date_input) # on value change, update the date input

            with ui.row().style('margin-top: 1em;'): # Create a row for the filter button
                ui.button('Filter Data', on_click=lambda: (
                    generate_graphs(graph_container, get_all_data(
                        *date_input.value.split(' - ')) if date_input.value else get_all_data()),
                    date_dialog.close() # close the dialog
                )).style('background-color: #3AAFA9; color: #FFFFFF; margin-top: 1em;')

    with ui.row().style('justify-content: center; width: 100%;'): # Create a row for the refresh/date button
        ui.button('Generate/Refresh', on_click=lambda: generate_graphs(
            graph_container)).style('background-color: #3AAFA9; color: #FFFFFF; margin-top: 1em; margin-bottom: 3em;')
        ui.button('Select Date Range', on_click=lambda: date_dialog.open()).style(
            'background-color: #3AAFA9; color: #FFFFFF; margin-top: 1em; margin-bottom: 3em;')

    # Generate graph with style 
    graph_container = ui.row().classes('graph-container').style('justify-content: center; background-color: #2C2C2C; padding: 1em; margin: 1em auto;')
    with graph_container:
        ui.label('Please press generate to see data.').style('color: #FFFFFF; font-size: 2em; text-align: center;')
    eco_footer() # display the footer

@ui.page('/graphs') # Route to graphs page
def graphs(): 
    from main_system import graph_container, labels 
    graphs_page(graph_container, labels)

# Add CSS for responsiveness
ui.add_css('''
    .graph-container {
        width: 80%;
        max-width: 1200px;
        height: 300px;
    }

    @media (max-width: 600px) {
        .graph-container {
            width: 100%;
            height: 200px;
        }
        .ui-label {
            font-size: 1.5em;
        }
    }
''')