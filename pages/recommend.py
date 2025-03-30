# File: recommend.py
# Description: Recommend algorithm for users based on their preferences.

from nicegui import ui
from web_functions import eco_header, eco_footer, inject_style
from collect_database import get_latest_data  # Import the function to fetch sensor data

# Define global dictionaries for thresholds
tds_references = {}
turbidity_references = {}
input_fields = []

def recommend_page():  # Function to display the recommend page
    global tds_references, turbidity_references, input_fields

    eco_header()  # inject the header
    inject_style()  # inject additional styles

    # Define TDS thresholds (hidden from UI)
    tds_fields = [
        ("Min TDS", "0"),
        ("Low TDS", "300"),
        ("Mid TDS", "600"),
        ("Max TDS", "1000"),
    ]
    for label, value in tds_fields:
        tds_references[label] = value  # Store thresholds in the dictionary

    # Define Turbidity thresholds (hidden from UI)
    turbidity_fields = [
        ("Min Turbidity", "0"),
        ("Low Turbidity", "25"),
        ("Mid Turbidity", "50"),
        ("Max Turbidity", "100"),
    ]
    for label, value in turbidity_fields:
        turbidity_references[label] = value  # Store thresholds in the dictionary

    # Define Temperature thresholds (hidden from UI)
    temperature_fields = [
        ("Min Temperature", "50"),
        ("Low Temperature", "60"),
        ("Mid Temperature", "75"),
        ("Max Temperature", "90"),
    ]
    for label, value in temperature_fields:
        input_fields.append((label, value))  # Store thresholds in the list

    # Use fixed robot IDs
    avatar = "https://robohash.org/user1?bgset=bg2"
    avatar2 = "https://robohash.org/user2?bgset=bg2"
    avatar3 = "https://robohash.org/user3?bgset=bg2"

    # Title
    with ui.row().classes("justify-center w-full mt-4"):
        ui.label("Recommendations").classes("text-white text-4xl font-bold text-center")

    # Recommendation Cards
    with ui.row().classes("justify-center w-full mt-6"):
        with ui.column().classes(
            "text-center p-5 bg-gray-800 rounded-lg shadow-lg max-w-sm"
        ):
            ui.image(avatar).classes("w-24 h-24 rounded-full mx-auto")
            tds_label = ui.label("Hi, I am the TDS advisor.").classes("text-white text-base mt-4")
            tds_loading = ui.skeleton().classes("w-full h-4 mt-2 hidden")  # Hidden by default

        with ui.column().classes(
            "text-center p-5 bg-gray-800 rounded-lg shadow-lg max-w-sm"
        ):
            ui.image(avatar2).classes("w-24 h-24 rounded-full mx-auto")
            turbidity_label = ui.label("Hello, I am the turbidity advisor.").classes(
                "text-white text-base mt-4"
            )
            turbidity_loading = ui.skeleton().classes("w-full h-4 mt-2 hidden")  # Hidden by default

        with ui.column().classes(
            "text-center p-5 bg-gray-800 rounded-lg shadow-lg max-w-sm"
        ):
            ui.image(avatar3).classes("w-24 h-24 rounded-full mx-auto")
            temperature_label = ui.label("Hey, I am the temperature advisor.").classes(
                "text-white text-base mt-4"
            )
            temperature_loading = ui.skeleton().classes("w-full h-4 mt-2 hidden")  # Hidden by default

    # Button to fetch sensor data and update labels
    def on_button_click():
        tds_label.set_text("Fetching data...")
        turbidity_label.set_text("Fetching data...")
        temperature_label.set_text("Fetching data...")
        tds_loading.classes(remove="hidden")  # Show loading bar
        turbidity_loading.classes(remove="hidden")  # Show loading bar
        temperature_loading.classes(remove="hidden")  # Show loading bar

        # Fetch the latest sensor data
        data = get_latest_data()
        if data:
            # TDS Recommendations
            tds_value = data['total dissolved solids']['value']
            if tds_value < float(tds_references["Low TDS"]):
                tds_label.set_text(f"TDS: {tds_value:.2f} ppm - Too Low, consider adding minerals.")
            elif tds_value < float(tds_references["Mid TDS"]):
                tds_label.set_text(f"TDS: {tds_value:.2f} ppm - Optimal range.")
            elif tds_value <= float(tds_references["Max TDS"]):
                tds_label.set_text(f"TDS: {tds_value:.2f} ppm - High, consider diluting.")
            else:
                tds_label.set_text(f"TDS: {tds_value:.2f} ppm - Too High, immediate action needed!")

            # Turbidity Recommendations
            turbidity_value = data['turbidity']['value']
            if turbidity_value < float(turbidity_references["Low Turbidity"]):
                turbidity_label.set_text(f"Turbidity: {turbidity_value:.2f} NTU - Clear water.")
            elif turbidity_value < float(turbidity_references["Mid Turbidity"]):
                turbidity_label.set_text(f"Turbidity: {turbidity_value:.2f} NTU - Slightly cloudy.")
            elif turbidity_value <= float(turbidity_references["Max Turbidity"]):
                turbidity_label.set_text(f"Turbidity: {turbidity_value:.2f} NTU - Cloudy, consider filtration.")
            else:
                turbidity_label.set_text(f"Turbidity: {turbidity_value:.2f} NTU - Very cloudy, immediate action needed!")

            # Temperature Recommendations
            temperature_value = data['temperature']['value']
            if temperature_value < float(input_fields[1][1]):
                temperature_label.set_text(f"Temperature: {temperature_value:.2f} °F - Too cold, consider heating.")
            elif temperature_value < float(input_fields[2][1]):
                temperature_label.set_text(f"Temperature: {temperature_value:.2f} °F - Optimal range.")
            elif temperature_value <= float(input_fields[3][1]):
                temperature_label.set_text(f"Temperature: {temperature_value:.2f} °F - Warm, monitor closely.")
            else:
                temperature_label.set_text(f"Temperature: {temperature_value:.2f} °F - Too hot, immediate cooling needed!")
        else:
            tds_label.set_text("No data available")
            turbidity_label.set_text("No data available")
            temperature_label.set_text("No data available")

        tds_loading.classes(add="hidden")  # Hide loading bar
        turbidity_loading.classes(add="hidden")  # Hide loading bar
        temperature_loading.classes(add="hidden")  # Hide loading bar

    # Add the button below the recommendation cards
    with ui.row().classes("justify-center w-full mt-6"):
        ui.button("Request advice", on_click=on_button_click).classes("bg-blue-500 text-white px-4 py-2 rounded")

    eco_footer()  # inject the footer


@ui.page("/recommend")  # Route for recommend page
def recommend():
    recommend_page()
