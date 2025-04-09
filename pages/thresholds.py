# File: thresholds.py
# Description: Settings page for thresholds.
from nicegui import ui
from web_functions import inject_style, eco_header, eco_footer
import json  
import os

DEFAULT_THRESHOLDS = {
    "TDS Thresholds": {
        "Min TDS": "50",
        "Low TDS": "100",
        "Mid TDS": "300",
        "Max TDS": "500",
    },
    "Turbidity Thresholds": {
        "Min Turbidity": "0",
        "Low Turbidity": "1",
        "Mid Turbidity": "5",
        "Max Turbidity": "25",
    },
    "Temperature Thresholds": {
        "Min Temperature": "65",
        "Low Temperature": "72",
        "Mid Temperature": "78",
        "Max Temperature": "82",
    },
}

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
    references = {
        "TDS Thresholds": {},
        "Turbidity Thresholds": {},
        "Temperature Thresholds": {},
    }

    for category, fields in DEFAULT_THRESHOLDS.items():
        with ui.card().classes(
            "outline_label bg-gray-800 p-5 rounded-lg w-full max-w-2xl mx-auto my-2"
        ):
            with ui.row().classes("justify-center w-full mt-0"):
                ui.label(category).classes(
                    "text-2xl text-white text-center sm:text-xl mt-0"
                )

            for label, value in fields.items():
                with ui.row().classes("justify-center items-center w-full my-2"):
                    ui.label(label).classes("text-lg text-white text-center sm:text-base mt-0")
                    references[category][label] = ui.input(label, value=value).classes(
                        "w-24 bg-gray-800 mx-2 sm:w-20 mt-0"
                    )
                    unit = "ppm" if "TDS" in label else "NTU" if "Turbidity" in label else "°F"
                    ui.label(unit).classes("text-lg text-white sm:text-base mt-0")

    with ui.row().classes("justify-center w-full my-4"):  # Save button for all thresholds
        ui.button(
            "Save All",
            on_click=lambda: save_all_thresholds(
                {key: ref.value for key, ref in references["TDS Thresholds"].items()},
                {key: ref.value for key, ref in references["Turbidity Thresholds"].items()},
                {key: ref.value for key, ref in references["Temperature Thresholds"].items()},
            ),
        ).classes("bg-teal-500 text-white w-full sm:w-auto mt-0")

    eco_footer()  # Add footer


def save_all_thresholds(tds, turbidity, temperature): # Save all thresholds to a JSON file
    data = {
        "TDS Thresholds": tds,
        "Turbidity Thresholds": turbidity,
        "Temperature Thresholds": temperature,
    }
    with open("thresholds.json", "w") as file:
        json.dump(data, file, indent=4)
    print(f"All thresholds saved to thresholds.json")

def save_tds_settings(min_tds, low_tds, mid_tds, max_tds): # Save TDS settings
    tds = {
        "Min TDS": min_tds,
        "Low TDS": low_tds,
        "Mid TDS": mid_tds,
        "Max TDS": max_tds,
    }
    try: # Load existing thresholds or create a new structure
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

def save_turbidity_settings(min_turbidity, low_turbidity, mid_turbidity, max_turbidity): # Save turbidity settings
    turbidity = {
        "Min Turbidity": min_turbidity,
        "Low Turbidity": low_turbidity,
        "Mid Turbidity": mid_turbidity,
        "Max Turbidity": max_turbidity,
    }
    try: # Load existing thresholds or create a new structure
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

def save_settings(min_temp, low_temp, mid_temp, max_temp): # Save temperature settings
    temperature = {
        "Min Temperature": min_temp,
        "Low Temperature": low_temp,
        "Mid Temperature": mid_temp,
        "Max Temperature": max_temp,
    }
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


def generate_default_settings():  # Generate default settings file if it doesn't exist
    if not os.path.exists("thresholds.json"):  # Check if the file already exists
        try:
            with open("thresholds.json", "x") as file:  # Use "x" mode to create the file if it doesn't exist
                json.dump(DEFAULT_THRESHOLDS, file, indent=4)
                print("Default thresholds.json file created.")
        except FileExistsError:
            print("File already exists, no action taken.")


@ui.page("/thresholds")  # Route for thresholds page
def thresholds():
    thresholds_page()