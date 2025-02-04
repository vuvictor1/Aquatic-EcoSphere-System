# File: contacts.py
# Description: Graphing page for the web interface
from nicegui import ui
from datetime import datetime
from web_functions import inject_style, eco_header, eco_footer
from collect_database import get_all_data

def generate_graphs(graph_container, data=None):  # Generate graphs for sensor data
    graph_container.clear()  # reset the graph container

    if data is None:  # Fetch all data if none is provided
        data = get_all_data()

    if data:  # Generate graphs if data is available
        desired_order = ['total dissolved solids', 'turbidity', 'temperature']
        for sensor_type in desired_order:

            if sensor_type in data:  # Check if sensor type is in the data
                values = data[sensor_type]  # get values for the sensor type
                timestamps = [entry['timestamp'].strftime(
                    '%m-%d %H:%M') for entry in values]  # extract timestamps
                sensor_values = [entry['value']
                                 for entry in values]  # extract sensor values

                # Calculate y-axis range
                sorted_values = sorted(sensor_values)
                # 25th percentile
                q1 = sorted_values[int(0.25 * len(sorted_values))]
                # 75th percentile
                q3 = sorted_values[int(0.75 * len(sorted_values))]
                iqr = q3 - q1  # interquartile range
                lower_bound = q1 - 1.5 * iqr  # lower bound for outliers
                filtered_values = [
                    value for value in sensor_values if lower_bound <= value]

                # Calculate y-axis range using filtered values
                min_value = min(filtered_values) if filtered_values else 0
                max_value = max(filtered_values) if filtered_values else 1
                distance_padding = 0.10  # padding for y-axis
                y_min = max(0, min_value - distance_padding *
                            (max_value - min_value))
                y_max = max_value + distance_padding * (max_value - min_value)

                with graph_container:  # Create a graph container

                    ui.echart({  # Create an ECharts graph
                        'title': {'text': sensor_type.title(), 'textStyle': {'color': '#FFFFFF'}},
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
                    }).classes('w-full sm:w-96 h-72')

def graphs_page(graph_container):  # Graphs page for the web interface
    eco_header()  # display the header
    inject_style()  # inject custom CSS styles

    with ui.row().classes('justify-center w-full mt-5'):  # Title for the page
        ui.label('Generate Graphs').classes('text-2xl sm:text-4xl text-white')

    with ui.dialog() as date_dialog:  # Create a dialog for selecting date range
        with ui.column().classes('bg-gray-800 p-4 sm:p-8 rounded-lg'):
            ui.label('Select Date Range:').classes(
                'text-white text-lg sm:text-xl bg-gray-700 p-2 sm:p-4')
            date_input = ui.input('Date range').classes(
                'w-full hidden')  # hidden input for date range

            # Create a date picker with a range of dates
            current_date = datetime.now().strftime('%Y/%m')
            current_date_limit = datetime.now().strftime('%Y/%m/%d')
            start_date_limit = '2025/01/12'
            date_picker = ui.date().props(f'range default-year-month={current_date} :options="date => date >= \'{start_date_limit}\' && date <= \'{current_date_limit}\'"')

            def update_date_input():  # Update the date input with the selected range
                selected_range = date_picker.value
                date_input.value = f"{selected_range['from']} - {selected_range['to']}" if selected_range and 'from' in selected_range and 'to' in selected_range else None
            # on value change, update the date input
            date_picker.on('update:model-value', update_date_input)

            with ui.row().classes('mt-4'):  # Create a row for the filter button
                ui.button('Filter Data', on_click=lambda: (
                    generate_graphs(graph_container, get_all_data(
                        *date_input.value.split(' - ')) if date_input.value else get_all_data()),
                    date_dialog.close()  # close the dialog
                )).classes('bg-teal-500 text-white mt-4')

    with ui.row().classes('justify-center w-full'):  # Create a row for the refresh/date button
        ui.button('Generate', on_click=lambda: generate_graphs(
            graph_container)).classes('bg-teal-500 text-white mt-4 mb-12')
        ui.button('Select Date Range', on_click=lambda: date_dialog.open()).classes(
            'bg-teal-500 text-white mt-4 mb-12')

    # Generate graph with style
    graph_container = ui.row().classes(
        'outline_label graph-container justify-center items-center bg-gray-800 p-4 my-4 mx-auto w-full max-w-screen-md')
    with graph_container:
        ui.label('Press generate to see graphing data').classes(
            'text-white text-lg sm:text-2xl text-center')
    eco_footer()  # display the footer


@ui.page('/graphs')  # Route to graphs page
def graphs():
    from main_system import graph_container
    graphs_page(graph_container)