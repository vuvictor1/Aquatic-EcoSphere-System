# File: thresholds.py
# Description: Settings page for thresholds.
from nicegui import ui
from web_functions import inject_style, eco_header, eco_footer
import json  # Import JSON module


def thresholds_page():  # Renders the thresholds page
    eco_header()  # Add header
    inject_style()  # Inject CSS

    ui.html(""" 
        <style>
            .q-field__native {
                color: white;
            }
            .q-field__label {
                color: white;
            }
            .mt-0 {
                margin-top: 0 !important;
            }
            .my-2 {
                margin-top: 0.5rem !important;
                margin-bottom: 0.5rem !important;
            }
        </style>
    """)

    with ui.row().classes("justify-center w-full mt-0"):  # Title for the page
        ui.label("Settings").classes("text-4xl text-white text-center sm:text-3xl mt-0")

    # Store references to all input fields
    tds_references = {}
    turbidity_references = {}
    temperature_references = {}

    # TDS Thresholds
    with ui.card().classes(
        "outline_label bg-gray-800 p-5 rounded-lg w-full max-w-2xl mx-auto mt-0"
    ):
        with ui.row().classes("justify-center w-full mt-0"):
            ui.label("Total Dissolved Solids Thresholds").classes(
                "text-2xl text-white text-center sm:text-xl mt-0"
            )

        tds_fields = [("Min TDS", "0"), ("Low TDS", "300"), ("Mid TDS", "600"), ("Max TDS", "1000")]
        for label, value in tds_fields:
            with ui.row().classes("justify-center items-center w-full my-2"):
                ui.label(label).classes("text-lg text-white text-center sm:text-base mt-0")
                tds_references[label] = ui.input(label, value=value).classes(
                    "w-24 bg-gray-800 mx-2 sm:w-20 mt-0"
                )
                ui.label("ppm").classes("text-lg text-white sm:text-base mt-0")

    # Turbidity Thresholds
    with ui.card().classes(
        "outline_label bg-gray-800 p-5 rounded-lg w-full max-w-2xl mx-auto my-2"
    ):
        with ui.row().classes("justify-center w-full mt-0"):
            ui.label("Turbidity Thresholds").classes(
                "text-2xl text-white text-center sm:text-xl mt-0"
            )

        turbidity_fields = [
            ("Min Turbidity", "0"),
            ("Low Turbidity", "25"),
            ("Mid Turbidity", "50"),
            ("Max Turbidity", "100"),
        ]
        for label, value in turbidity_fields:
            with ui.row().classes("justify-center items-center w-full my-2"):
                ui.label(label).classes("text-lg text-white text-center sm:text-base mt-0")
                turbidity_references[label] = ui.input(label, value=value).classes(
                    "w-24 bg-gray-800 mx-2 sm:w-20 mt-0"
                )
                ui.label("NTU").classes("text-lg text-white sm:text-base mt-0")

    # Temperature Thresholds
    with ui.card().classes(
        "outline_label bg-gray-800 p-5 rounded-lg w-full max-w-2xl mx-auto my-2"
    ):
        with ui.row().classes("justify-center w-full mt-0"):
            ui.label("Temperature Thresholds").classes(
                "text-2xl text-white text-center sm:text-xl mt-0"
            )

        temperature_fields = [
            ("Min Temperature", "50"),
            ("Low Temperature", "60"),
            ("Mid Temperature", "75"),
            ("Max Temperature", "90"),
        ]
        for label, value in temperature_fields:
            with ui.row().classes("justify-center items-center w-full my-2"):
                ui.label(label).classes("text-lg text-white text-center sm:text-base mt-0")
                temperature_references[label] = ui.input(label, value=value).classes(
                    "w-24 bg-gray-800 mx-2 sm:w-20 mt-0"
                )
                ui.label("°F").classes("text-lg text-white sm:text-base mt-0")

    # Global Save Button
    with ui.row().classes("justify-center w-full my-4"):
        ui.button(
            "Save All",
            on_click=lambda: save_all_thresholds(
                {
                    "Min TDS": tds_references["Min TDS"].value,
                    "Low TDS": tds_references["Low TDS"].value,
                    "Mid TDS": tds_references["Mid TDS"].value,
                    "Max TDS": tds_references["Max TDS"].value,
                },
                {
                    "Min Turbidity": turbidity_references["Min Turbidity"].value,
                    "Low Turbidity": turbidity_references["Low Turbidity"].value,
                    "Mid Turbidity": turbidity_references["Mid Turbidity"].value,
                    "Max Turbidity": turbidity_references["Max Turbidity"].value,
                },
                {
                    "Min Temperature": temperature_references["Min Temperature"].value,
                    "Low Temperature": temperature_references["Low Temperature"].value,
                    "Mid Temperature": temperature_references["Mid Temperature"].value,
                    "Max Temperature": temperature_references["Max Temperature"].value,
                },
            ),
        ).classes("bg-teal-500 text-white w-full sm:w-auto mt-0")

    eco_footer()  # Add footer


# Save all thresholds to a single JSON file
def save_all_thresholds(tds, turbidity, temperature):
    data = {
        "TDS Thresholds": tds,
        "Turbidity Thresholds": turbidity,
        "Temperature Thresholds": temperature,
    }
    with open("thresholds.json", "w") as file:
        json.dump(data, file, indent=4)
    print(f"All thresholds saved to thresholds.json")

# Save TDS settings
def save_tds_settings(min_tds, low_tds, mid_tds, max_tds):
    tds = {
        "Min TDS": min_tds,
        "Low TDS": low_tds,
        "Mid TDS": mid_tds,
        "Max TDS": max_tds,
    }
    # Load existing thresholds or create a new structure
    try:
        with open("thresholds.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data["TDS Thresholds"] = tds
    save_all_thresholds(
        data.get("TDS Thresholds", {}),
        data.get("Turbidity Thresholds", {}),
        data.get("Temperature Thresholds", {}),
    )

# Save turbidity settings
def save_turbidity_settings(min_turbidity, low_turbidity, mid_turbidity, max_turbidity):
    turbidity = {
        "Min Turbidity": min_turbidity,
        "Low Turbidity": low_turbidity,
        "Mid Turbidity": mid_turbidity,
        "Max Turbidity": max_turbidity,
    }
    # Load existing thresholds or create a new structure
    try:
        with open("thresholds.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data["Turbidity Thresholds"] = turbidity
    save_all_thresholds(
        data.get("TDS Thresholds", {}),
        data.get("Turbidity Thresholds", {}),
        data.get("Temperature Thresholds", {}),
    )

# Save temperature settings
def save_settings(min_temp, low_temp, mid_temp, max_temp):
    temperature = {
        "Min Temperature": min_temp,
        "Low Temperature": low_temp,
        "Mid Temperature": mid_temp,
        "Max Temperature": max_temp,
    }
    # Load existing thresholds or create a new structure
    try:
        with open("thresholds.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data["Temperature Thresholds"] = temperature
    save_all_thresholds(
        data.get("TDS Thresholds", {}),
        data.get("Turbidity Thresholds", {}),
        data.get("Temperature Thresholds", {}),
    )


@ui.page("/thresholds")  # Route for thresholds page
def thresholds():
    thresholds_page()