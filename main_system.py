# Authors: Victor Vu and Jordan Morris
# File: main_system.py
# Description: Main system file that connects to the MySQL database for sensor data. Aimed at mobile app users.
# Copyright (C) 2024 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui
import os
import json
from dotenv import load_dotenv
from collect_database import create_connection, get_latest_data
from web_functions import inject_style, eco_header, eco_footer, inject_lottie
from pages.contacts import contacts_page
from pages.graphs import graphs_page
from pages.encyclopedia import encyclopedia_page
from pages.login import AuthMiddleware
from threshold_config import get_temperature_thresholds, interpolate_color
from pages.settings import settings_page
from pages.reminders import reminders_page
from pages.species import species_page
from pages.predictions import predictions_page

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

# Function to read reminders from reminders.json


def read_reminders():
    reminders_file = 'reminders_data.json'
    if os.path.exists(reminders_file):
        with open(reminders_file, 'r') as file:
            return json.load(file)
    return None


def home_page():  # Home page function
    eco_header()  # call eco_header function

    with ui.right_drawer().style('background-color: #6C757D; align-items: center;') as right_drawer:  # Right drawer
        ui.label('[Notices]').style(
            'color: #FFFFFF; font-size: 24px;')  # notice title

        notices = [  # list of notices
            '1. Timers update periodically in intervals of 5 minutes.',
            '2. You can configure sensor thresholds in the settings menu.',
            '3. Add tank species before proceeding, otherwise default values apply in alerts.',
            '4. Graph data only updates at startup but can be refreshed with new generation',
            '5. Be sure you to set any reminders for regular maintenance tasks.'
        ]
        for notice in notices:  # Iterate through each notice
            ui.chat_message(notice, name='Advisor Robot',
                            # chat message
                            avatar='https://robohash.org/iamexpertfishadvisor').style(LABEL_STYLE)

        ui.label('[Disclaimer]').style(
            'color: #FFFFFF; font-size: 24px;')  # disclaimer title
        disclaimers = [
            '1. Recommendations are suggestions only and up to user discretion.',
            '2. This tool must be manually configured for salt-water setups.',
        ]
        for disclaimer in disclaimers:
            ui.chat_message(disclaimer, name='Warning Robot',
                            # chat message
                            avatar='https://robohash.org/alarm?set=set2').style(LABEL_STYLE)
        ui.button('Close', on_click=lambda: right_drawer.toggle()
                  ).style(LABEL_STYLE)  # button to toggle advisor

    inject_style()  # call inject_style function
    inject_lottie()  # call inject_lottie function
    lottie_url = 'https://lottie.host/33548596-614d-4e89-a0a8-69126f02a92a/EmTPHrDT7l.json'  # lottie url
    with ui.row().style('justify-content: center; width: 100%; margin-top: -50px;'):  # Lottie player
        ui.html(f'''<lottie-player src="{lottie_url}
                " loop autoplay speed="0.25" style="height: 300px;"></lottie-player>''')

    with ui.row().style('justify-content: center; width: 100%'):  # Main title
        ui.label('Aquatic EcoSphere System').style(
            'color: #FFFFFF; font-size: 32px; margin-top: -50px;')

    # Sensor Cards
    global labels
    labels = {}
    with ui.row().style('justify-content: center; width: 100%;'):
        for sensor_type in ['total dissolved solids', 'turbidity', 'temperature']:

            with ui.column().classes('card').style('align-items: center;'):  # Use css class
                sensor_label = ui.label(sensor_type.title()).style(LABEL_STYLE)
                value_label = ui.label('Value: Loading...').style(LABEL_STYLE)
                timestamp_label = ui.label(
                    'Timestamp: Loading...').style(LABEL_STYLE)
                labels[sensor_type] = (
                    sensor_label, value_label, timestamp_label)

    reminders = read_reminders()
    upcoming_task = reminders[0] if reminders else None

    with ui.row().style('justify-content: center; width: 100%; margin-top: 20px;'):  # Additional cards
        card_labels = {  # Card for alerts, reminders, & recommendations
            'Alerts': 'Coming soon... W.I.P.',
            'Reminders': f"Upcoming Task: {upcoming_task['task']} ({upcoming_task['frequency']} days)" if upcoming_task else "No upcoming tasks",
            'Recommendations': 'Coming soon... W.I.P.'
        }

        for card_type, card_label in card_labels.items():  # Use css class
            with ui.column().classes('card').style('align-items: center;'):
                ui.label(card_type).style(LABEL_STYLE)
                ui.label(card_label).style('color: #FFFFFF; font-size: 16px;')
    eco_footer()  # call eco_footer function
    ui.timer(290, lambda: update_ui(labels))  # update ui every 290s


def update_ui(labels):  # Update sensor labels with the latest data
    data = get_latest_data()
    if data:  # Update labels if data is available
        for sensor_type, value in data.items():  # Iterate through each type and value label

            # Get unit for sensor type
            unit = sensor_units.get(sensor_type, '')
            labels[sensor_type][1].set_text(f"{value['value']:.2f} {unit}")
            labels[sensor_type][2].set_text(f"{value['timestamp']}")

            if sensor_type == 'temperature':  # Update temperature card color
                current_temp = value['value']
                thresholds = get_temperature_thresholds()  # get current thresholds
                color = interpolate_color(current_temp, thresholds)
                labels[sensor_type][0].style(LABEL_STYLE)
                labels[sensor_type][1].style(
                    f'color: {color}; font-size: 16px;')
                labels[sensor_type][2].style(LABEL_STYLE)


@ui.page('/')  # Set homepage route
def home():
    home_page()


load_dotenv()  # load environment variables from .env file
storage_secret = os.getenv('STORAGE_SECRET')  # storage secret from .env file
ui.run(title="Aquatic EcoSphere", favicon="🌊",
       storage_secret=storage_secret)  # run ui with logo
