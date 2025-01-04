# Authors: Victor Vu and Jordan Morris
# File: main_system.py
# Description: Main system file that connects to the MySQL database for sensor data. Aimed at mobile app users.
# Copyright (C) 2024 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui
from db_connection import create_connection
from web_functions import inject_style, eco_header, eco_footer, inject_lottie
from data_functions import generate_graphs, get_all_data, update_data
from pages.contacts import contacts_page

# Initialize global variables
connection = create_connection() # create a database connection
graph_container = None # container for graphs
labels = {} # sensor labels
LABEL_STYLE = 'color: #FFFFFF; font-size: 16px;' # constant text

def home_page(): # Home page function
    eco_header() # call eco_header function

    with ui.right_drawer().style('background-color: #6C757D; align-items: center;'): # Right drawer
        ui.label('[Notice and Disclaimer]').style('color: #FFFFFF; font-size: 18px;') # title
        notices = [
            '1. Timers update periodically in intervals of 10mins. (Currently 10secs for testing only)',
            '2. Recommendations are suggestions only and up to user discretion.',
            '3. Set species before proceeding, otherwise default tolerances will be used in alerts/recommendations.',
            '4. Graphs update only at startup but can be refreshed with the button',
            'More instructions TBA...'
        ]
        for notice in notices: 
            ui.label(notice).style(LABEL_STYLE) # apply the label style
    inject_style() # call inject_style function

    inject_lottie() # call inject_lottie function
    lottie_url = 'https://lottie.host/33548596-614d-4e89-a0a8-69126f02a92a/EmTPHrDT7l.json' # lottie url
    with ui.row().style('justify-content: center; width: 100%; margin-top: -50px;'): # Lottie player
        ui.html(f'''<lottie-player src="{lottie_url}" loop autoplay style="height: 300px;"></lottie-player>''') 

    with ui.row().style('justify-content: center; width: 100%'): # Main title
        ui.label('Aquatic EcoSphere System').style('color: #FFFFFF; font-size: 32px; margin-top: -50px;') # welcome label

    # Sensor Cards
    global labels
    labels = {}
    with ui.row().style('justify-content: center; width: 100%;'): 
        for sensor_type in ['total dissolved solids', 'turbidity', 'temperature']: 
            with ui.column().classes('card').style('align-items: center;'): # Use css class
                sensor_label = ui.label(sensor_type).style(LABEL_STYLE)
                value_label = ui.label(f'{sensor_type} Value: Loading...').style(LABEL_STYLE)
                timestamp_label = ui.label(f'{sensor_type} Timestamp: Loading...').style(LABEL_STYLE)
                labels[sensor_type] = (sensor_label, value_label, timestamp_label)

    with ui.row().style('justify-content: center; width: 100%; margin-top: 20px;'): # Additional cards
        for card_type in ['Alerts', 'Reminders', 'Recommendations']: # Cards for alerts, reminders, and recommendations
            with ui.column().classes('card').style('align-items: center;'): # Use css class
                ui.label(card_type).style(LABEL_STYLE)
                ui.label('No action required. WIP...').style(LABEL_STYLE)

    with ui.dialog() as date_dialog: # Date range selection dialog
        date_dialog.classes('card').style('justify-content: center; width: 100%;') # use css class for background
        ui.label('Select Date Range:').style('color: #FFFFFF; font-size: 18px;')
        date_input = ui.input('Date range').classes() 
        date_picker = ui.date().props('range')

        def update_date_input(): # Update date input based on selected range
            selected_range = date_picker.value # get selected range
            date_input.value = f"{selected_range['from']} - {selected_range['to']}" if selected_range and 'from' in selected_range and 'to' in selected_range else None
        date_picker.on('update:model-value', update_date_input) # update date input based on calendar selection

        with ui.row().style('justify-content: center; width: 100%; margin-top: 10px;'): # Filter data button
            ui.button('Filter Data', on_click=lambda: (
                generate_graphs(graph_container, get_all_data(
                    *date_input.value.split(' - ')) if date_input.value else get_all_data()),
                date_dialog.close()
            )).style('background-color: #3AAFA9; color: #FFFFFF; margin-top: 10px;')

    with ui.row().style('justify-content: center; width: 100%; margin-top: 20px;'): # Select date range button
        ui.button('Select Date Range', on_click=lambda: date_dialog.open()).style(
            'background-color: #3AAFA9; color: #FFFFFF; margin-top: 10px;')

    # Container for graphs
    global graph_container
    graph_container = ui.row().style('justify-content: center; width: 100%;')
    generate_graphs(graph_container)

    with ui.row().style('justify-content: center; width: 100%;'): # Refresh graphs button
        ui.button('Refresh Graphs', on_click=lambda: generate_graphs(
            graph_container)).style('background-color: #3AAFA9; color: #FFFFFF;')
    eco_footer() # call eco_footer function
    ui.timer(10, lambda: update_data(labels)) # update data every 10s

@ui.page('/') # Set homepage route
def home():
    home_page()

ui.run(title="Aquatic EcoSphere", favicon="🌊") # run ui with logo