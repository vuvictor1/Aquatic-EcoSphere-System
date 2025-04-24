# File: recommend.py
# Description: Recommend algorithm for users based on their preferences.
import json
from nicegui import ui
from web_functions import eco_header, eco_footer, inject_style
from collect_database import get_latest_data 

# Define global dictionaries for thresholds
tds_references = {}
turbidity_references = {}
temperature_references = {}
input_fields = []

def load_thresholds(): # Function to load thresholds from JSON file
    global tds_references, turbidity_references, temperature_references, input_fields
    try:
        with open("thresholds.json", "r") as file:
            thresholds = json.load(file)
            tds_references = thresholds.get("TDS Thresholds", {})
            turbidity_references = thresholds.get("Turbidity Thresholds", {})
            temperature_references = thresholds.get("Temperature Thresholds", {})
            input_fields = [
                ("Min Temperature", temperature_references.get("Min Temperature", "0")),
                ("Low Temperature", temperature_references.get("Low Temperature", "0")),
                ("Mid Temperature", temperature_references.get("Mid Temperature", "0")),
                ("Max Temperature", temperature_references.get("Max Temperature", "0")),
            ]
    except FileNotFoundError:
        print("Error: thresholds.json file not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode thresholds.json.")

def recommend_page():  # Function to display the recommend page
    global tds_references, turbidity_references, input_fields

    load_thresholds() # load the thresholds
    eco_header()  # inject the header
    inject_style()  # inject additional styles

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
            tds_label = ui.label("Hi, I am the TDS advisor.").classes(
                "text-white text-base mt-4"
            )

        with ui.column().classes(
            "text-center p-5 bg-gray-800 rounded-lg shadow-lg max-w-sm"
        ):
            ui.image(avatar2).classes("w-24 h-24 rounded-full mx-auto")
            turbidity_label = ui.label("Hello, I am the turbidity advisor.").classes(
                "text-white text-base mt-4"
            )

        with ui.column().classes(
            "text-center p-5 bg-gray-800 rounded-lg shadow-lg max-w-sm"
        ):
            ui.image(avatar3).classes("w-24 h-24 rounded-full mx-auto")
            temperature_label = ui.label("Hey, I am the temperature advisor.").classes(
                "text-white text-base mt-4"
            )

    def on_button_click(): # Function to handle button click
        tds_label.set_text("Fetching data...")
        turbidity_label.set_text("Fetching data...")
        temperature_label.set_text("Fetching data...")

        # Fetch the latest sensor data
        data = get_latest_data()
        if data:
            # TDS Recommendations
            tds_value = data["total dissolved solids"]["value"]
            if tds_value < float(tds_references["Low TDS"]):
                tds_label.set_text(
                    f"TDS: {tds_value:.2f} ppm - Too Low. Consider adding minerals like calcium or magnesium which are present in tap water."
                )
            elif tds_value < float(tds_references["Mid TDS"]):
                tds_label.set_text(f"TDS: {tds_value:.2f} ppm - Optimal range.")
            elif tds_value <= float(tds_references["Max TDS"]):
                tds_label.set_text(
                    f"TDS: {tds_value:.2f} ppm - High. Consider performing a partial water change."
                )
            else:
                tds_label.set_text(
                    f"TDS: {tds_value:.2f} ppm - Too High! Immediate action needed. Perform a large water change."
                )

            # Turbidity Recommendations
            turbidity_value = data["turbidity"]["value"]
            if turbidity_value < float(turbidity_references["Low Turbidity"]):
                turbidity_label.set_text(
                    f"Turbidity: {turbidity_value:.2f} NTU - Clear water. No action needed."
                )
            elif turbidity_value < float(turbidity_references["Mid Turbidity"]):
                turbidity_label.set_text(
                    f"Turbidity: {turbidity_value:.2f} NTU - Slightly cloudy. Be careful with overfeeding."
                )
            elif turbidity_value <= float(turbidity_references["Max Turbidity"]):
                turbidity_label.set_text(
                    f"Turbidity: {turbidity_value:.2f} NTU - Cloudy. Consider cleaning your filter."
                )
            else:
                turbidity_label.set_text(
                    f"Turbidity: {turbidity_value:.2f} NTU - Very cloudy! Immediate action needed! Perform a large water change."
                )

            # Temperature Recommendations
            temperature_value = data["temperature"]["value"]
            if temperature_value < float(input_fields[1][1]):
                temperature_label.set_text(
                    f"Temperature: {temperature_value:.2f} °F - Too cold, consider heating."
                )
            elif temperature_value < float(input_fields[2][1]):
                temperature_label.set_text(
                    f"Temperature: {temperature_value:.2f} °F - Optimal range."
                )
            elif temperature_value <= float(input_fields[3][1]):
                temperature_label.set_text(
                    f"Temperature: {temperature_value:.2f} °F - Warm. Monitor closely."
                )
            else:
                temperature_label.set_text(
                    f"Temperature: {temperature_value:.2f} °F - Too hot, immediate cooling needed!"
                )
        else:
            tds_label.set_text("No data available")
            turbidity_label.set_text("No data available")
            temperature_label.set_text("No data available")

    # Add the button below the recommendation cards
    with ui.row().classes("justify-center w-full mt-6"):
        ui.button("Request advice", on_click=on_button_click).classes(
            "bg-blue-500 text-white px-4 py-2 rounded"
        )

    eco_footer()  # inject the footer


@ui.page("/recommend")  # Route for recommend page
def recommend():
    recommend_page()