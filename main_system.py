# Authors: Victor Vu and Jordan Morris
# File: main_system.py
# Description: Main system file that connects to the MySQL database for sensor data.
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui
import os
import json
from collect_database import create_connection, get_latest_data, env_reuse
from web_functions import inject_style, eco_header, eco_footer, inject_lottie
from pages.contacts import contacts_page
from pages.graphs import graphs_page
from pages.encyclopedia import encyclopedia_page
from pages.login import AuthMiddleware
from pages.thresholds import thresholds_page, generate_default_settings
from pages.reminders import reminders_page
from pages.predictions import predictions_page
from pages.recommend import recommend_page
from firebase import notifications_page

# Initialize global variables
connection = create_connection()  # create a database connection
graph_container = None  # container for graphs
labels = {}  # sensor labels
sensor_units = {  # sensor_type: unit
    "total dissolved solids": "ppm",
    "turbidity": "NTU",
    "temperature": "°F",
}

generate_default_settings()  # Ensure default settings file exists

# Function to read reminders from reminders.json
def read_reminders():
    reminders_file = "reminders_data.json"
    if os.path.exists(reminders_file):
        with open(reminders_file, "r") as file:
            return json.load(file)
    return None


def home_page():  # Home page function
    eco_header()  # call eco_header function

    with ui.right_drawer().classes(
        "bg-gray-600 flex items-center"
    ) as right_drawer:  # Right drawer
        ui.label("[Notices]").classes("text-white text-2xl")  # notice title

        notices = [  # List of notices
            "1. Timers update periodically in intervals of 5 minutes.",
            "2. You can configure sensor thresholds in the settings menu.",
            "3. Add tank species before proceeding, otherwise default values apply in alerts.",
            "4. Graph data only updates at startup but can be refreshed with new generation",
            "5. Be sure you to set any reminders for regular maintenance tasks.",
        ]
        for notice in notices:  # Iterate through each notice
            ui.chat_message(
                notice,
                name="Advisor Robot",
                avatar="https://robohash.org/iamexpertfishadvisor",
            ).classes("text-white text-base")

        ui.label("[Disclaimer]").classes(
            "text-white text-2xl")  # disclaimer title
        disclaimers = [
            "1. Recommendations are suggestions only and up to user discretion.",
            "2. This tool must be manually configured for salt-water setups.",
        ]
        for disclaimer in disclaimers:
            ui.chat_message(
                disclaimer,
                name="Warning Robot",
                avatar="https://robohash.org/alarm?set=set2",
            ).classes("text-white text-base")
        ui.button("Close", on_click=lambda: right_drawer.toggle()).classes(
            "text-white text-base"
        )  # button to toggle advisor

    inject_style()  # call inject_style function
    inject_lottie()  # call inject_lottie function
    lottie_url = "https://lottie.host/33548596-614d-4e89-a0a8-69126f02a92a/EmTPHrDT7l.json"  # lottie url
    with ui.row().classes("justify-center w-full mt-0"):  # Lottie player
        ui.html(f'''<lottie-player src="{lottie_url}"
                loop autoplay speed="0.25" style="height: 300px;"></lottie-player>''')

    with ui.row().classes("justify-center w-full mt-0"):  # Main title
        ui.label("Aquatic EcoSphere System").classes(
            "text-white text-4xl mt-0 text-center")

    # Sensor Cards
    global labels
    labels = {}
    with ui.row().classes("justify-center w-full mt-0"):
        for sensor_type in ["total dissolved solids", "turbidity", "temperature"]:
            with ui.column().classes(
                "outline_label items-center text-center p-5 bg-gray-800 rounded-lg shadow-lg max-w-sm my-2"
            ):
                sensor_label = ui.label(sensor_type.title()).classes(
                    "text-white text-base"
                )
                value_label = ui.label("Value: Loading...").classes(
                    "text-white text-base"
                )
                timestamp_label = ui.label("Timestamp: Loading...").classes(
                    "text-white text-base"
                )
                labels[sensor_type] = (
                    sensor_label, value_label, timestamp_label)

    reminders = read_reminders()  # read reminders from reminders.json
    if reminders:  # Sort reminders by priority
        reminders.sort(key=lambda x: x["priority"])
        upcoming_task = reminders[0]
    else:
        upcoming_task = None

    with ui.row().classes("justify-center w-full mt-2"):  # Additional cards
        card_labels = {  # Card for alerts, reminders, & recommendations
            "Alerts": "Coming soon... W.I.P.",
            "Reminders": f"Upcoming Task: {upcoming_task['task']} (Priority Rank: {upcoming_task['priority']})"
            if upcoming_task
            else "No upcoming tasks",
            "Recommendations": "Consult recommend page",
        }

        for card_type, card_label in card_labels.items():  # Use css class
            with ui.column().classes(
                "outline_label items-center text-center p-5 bg-gray-800 rounded-lg shadow-lg max-w-sm my-2"
            ):
                ui.label(card_type).classes("text-white text-base")
                ui.label(card_label).classes("text-white text-base")

    with ui.row().classes("justify-center w-full mt-2"): # TEMP only to test noftifications -------------------------------
        ui.link("Go to Notifications Page", "/notifications").classes(
            "text-white text-2xl no-underline mb-2 md:mb-0"
        )

    eco_footer()  # call eco_footer function
    ui.timer(290, lambda: update_ui(labels))  # update ui every 290s


def update_ui(labels):  # Update sensor labels with the latest data
    data = get_latest_data()
    if data:  # Update labels if data is available
        for (
            sensor_type,
            value,
        ) in data.items():  # Iterate through each type and value label
            # Get unit for sensor type
            unit = sensor_units.get(sensor_type, "")
            labels[sensor_type][1].set_text(f"{value['value']:.2f} {unit}")
            labels[sensor_type][2].set_text(f"{value['timestamp']}")


@ui.page("/")  # Set homepage route
def home():
    home_page()


env_reuse()  # load environment variables from .env file
storage_secret = os.getenv("STORAGE_SECRET")  # storage secret from .env file
ui.run(
    title="Aquatic EcoSphere", favicon="🌊", storage_secret=storage_secret
)  # run ui with logo
