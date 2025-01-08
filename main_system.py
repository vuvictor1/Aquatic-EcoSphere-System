# Authors: Victor Vu and Jordan Morris
# File: main_system.py
# Description: Main system file that connects to the MySQL database for sensor data. Aimed at mobile app users.
# Copyright (C) 2024 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from dotenv import load_dotenv
import os
from nicegui import ui
from collect_database import create_connection, get_latest_data
from web_functions import inject_style, eco_header, eco_footer, inject_lottie
from pages.contacts import contacts_page
from pages.graphs import graphs_page
from pages.encyclopedia import encyclopedia_page
from pages.login import AuthMiddleware

# Initialize global variables
connection = create_connection()  # create a database connection
graph_container = None  # container for graphs
labels = {}  # sensor labels
LABEL_STYLE = 'color: #FFFFFF; font-size: 16px;'  # constant text
sensor_units = {  # sensor_type: unit
    'total dissolved solids': 'ppm',
    'turbidity': 'NTU',
    'temperature': '°F'
}


def home_page():  # Home page function
    eco_header()  # call eco_header function

    with ui.right_drawer().style('background-color: #6C757D; align-items: center;'):  # Right drawer
        ui.label('[Notice and Disclaimer]').style(
            'color: #FFFFFF; font-size: 18px;')  # title
        notices = [
            '1. Timers update periodically in intervals of 10mins. (Currently 10secs for testing only)',
            '2. Recommendations are suggestions only and up to user discretion.',
            '3. Set species before proceeding, otherwise default tolerances will be used in alerts/recommendations.',
            '4. Graphs update only at startup but can be refreshed with the button',
            'More instructions TBA...'
        ]
        for notice in notices:
            ui.label(notice).style(LABEL_STYLE)  # apply the label style
    inject_style()  # call inject_style function

    inject_lottie()  # call inject_lottie function
    lottie_url = 'https://lottie.host/33548596-614d-4e89-a0a8-69126f02a92a/EmTPHrDT7l.json'  # lottie url
    with ui.row().style('justify-content: center; width: 100%; margin-top: -50px;'):  # Lottie player
        ui.html(f'''<lottie-player src="{lottie_url}
                " loop autoplay speed="0.25" style="height: 300px;"></lottie-player>''')

    with ui.row().style('justify-content: center; width: 100%'):  # Main title
        ui.label('Aquatic EcoSphere System').style(
            'color: #FFFFFF; font-size: 32px; margin-top: -50px;')  # welcome label

    # Sensor Cards
    global labels
    labels = {}
    with ui.row().style('justify-content: center; width: 100%;'):
        for sensor_type in ['total dissolved solids', 'turbidity', 'temperature']:
            with ui.column().classes('card').style('align-items: center;'):  # Use css class
                sensor_label = ui.label(sensor_type).style(LABEL_STYLE)
                value_label = ui.label('Value: Loading...').style(LABEL_STYLE)
                timestamp_label = ui.label(
                    'Timestamp: Loading...').style(LABEL_STYLE)
                labels[sensor_type] = (
                    sensor_label, value_label, timestamp_label)

    with ui.row().style('justify-content: center; width: 100%; margin-top: 20px;'):  # Additional cards
        # Cards for alerts, reminders, and recommendations
        for card_type in ['Alerts', 'Reminders', 'Recommendations']:
            with ui.column().classes('card').style('align-items: center;'):  # Use css class
                ui.label(card_type).style(LABEL_STYLE)
                ui.label('No action required. WIP...').style(LABEL_STYLE)
    eco_footer()  # call eco_footer function
    ui.timer(10, lambda: update_ui(labels))  # update ui every 10s


def update_ui(labels):  # Update sensor labels with the latest data
    data = get_latest_data()
    if data:  # Update labels if data is available
        for sensor_type, value in data.items():  # Iterate through each type and value label
            # get unit for sensor type
            unit = sensor_units.get(sensor_type, '')
            labels[sensor_type][1].set_text(f"{value['value']:.2f} {unit}")
            labels[sensor_type][2].set_text(f"{value['timestamp']}")


@ui.page('/')  # Set homepage route
def home():
    home_page()


load_dotenv()  # Load environment variables from .env file

storage_secret = os.getenv('STORAGE_SECRET')
ui.run(title="Aquatic EcoSphere", favicon="🌊", storage_secret=storage_secret)
