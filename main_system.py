# Authors: Victor Vu and Jordan Morris
# File: main_system.py
# Description: Main system file that connects to the MySQL database for sensor data
# Copyright (C) 2024 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui
from db_connection import *
from web_functions import *
from data_functions import *
from pages.contacts import contacts_page 

connection = create_connection()  # Connection to MySQL database
graph_container = None  # Container to store graphs
labels = {}  # Dictionary to store sensor labels

# Header menu
with ui.header().style('background-color: #3AAFA9;'):
    ui.label('🌊 Homepage').style('color: #FFFFFF; font-size: 24px;')
    ui.button(icon='account_circle')  # add account button
    ui.button(icon='menu')  # add menu button

# Right Drawer
with ui.right_drawer().style('background-color: #6C757D; align-items: center;'):
    ui.label('[Notice and Disclaimer]').style(
        'color: #FFFFFF; font-size: 18px;')
    ui.label('1. Timers update periodically in intervals of 10mins. (Set to 10secs for debugging and testing only)').style(
        'color: #FFFFFF; font-size: 14px;')
    ui.label('2. Recommendations are suggestions, not mandatory.').style(
        'color: #FFFFFF; font-size: 14px;')
    ui.label('3. Specify species before proceeding, otherwise default values will be used.').style(
        'color: #FFFFFF; font-size: 14px;')
    ui.label('4. Graphs update only at startup but can be refreshed with the button').style(
        'color: #FFFFFF; font-size: 14px;')
    ui.label('TBA...').style('color: #FFFFFF; font-size: 14px;')


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
                    'color: #FFFFFF; font-weight: bold;')  # add sensor label
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

    # Create a dialog for the date range input
    with ui.dialog() as date_dialog:
        ui.label('Select Date Range:').style(
            'color: #FFFFFF; font-size: 18px;')
        date_input = ui.input('Date range').classes('w-40')
        date_picker = ui.date().props('range')

        def update_date_input():
            selected_range = date_picker.value
            if selected_range and 'from' in selected_range and 'to' in selected_range:date_input.value = f"{selected_range['from']} - {selected_range['to']}"
            else:
                date_input.value = None

        date_picker.on('update:model-value', update_date_input)

    # Button to open the date range selection dialog
    with ui.row().style('justify-content: center; width: 100%; margin-top: 20px;'):
        ui.button('Select Date Range', on_click=lambda: date_dialog.open()).style(
            'background-color: #3AAFA9; color: #FFFFFF; margin-top: 10px;')

    # Button to filter data based on selected date range
    with ui.row().style('justify-content: center; width: 100%; margin-top: 10px;'):
        ui.button('Filter Data', on_click=lambda: (
            generate_graphs(graph_container, get_all_data(
                *date_input.value.split(' - ')) if date_input.value else get_all_data()),
            date_dialog.close()
        )).style('background-color: #3AAFA9; color: #FFFFFF; margin-top: 10px;')

    global graph_container
    graph_container = ui.row().style(
        'justify-content: center; width: 100%;')  # container for graphs
    generate_graphs(graph_container)  # Pass graph_container to generate_graphs

    # Refresh graphs button
    with ui.row().style('justify-content: center; width: 100%;'):
        ui.button('Refresh Graphs', on_click=lambda: generate_graphs(graph_container)).style(
            'background-color: #3AAFA9; color: #FFFFFF;')

    eco_footer()  # call eco_footer function

    # update data every 10s just for testing
    ui.timer(10, lambda: update_data(labels))


@ui.page('/')  # Set homepage route
def home():
    home_page()


# run the UI with tab name and logo
ui.run(title="Aquatic EcoSphere", favicon="🌊")
