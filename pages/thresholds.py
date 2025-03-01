# File: thresholds.py
# Description: Settings page for thresholds.
from nicegui import ui
from web_functions import inject_style, eco_header, eco_footer


def thresholds_page():  # Renders the thresholds page
    eco_header()  # add header
    inject_style()  # inject css

    ui.html(""" 
        <style>
            .q-field__native {
                color: white;
            }
            .q-field__label {
                color: white;
            }
        </style>
    """)

    with ui.row().classes("justify-center w-full mt-2"):  # Title for the page
        ui.label("Settings").classes("text-4xl text-white text-center sm:text-3xl")

    with ui.card().classes(
        "outline_label bg-gray-800 p-5 rounded-lg w-full max-w-2xl mx-auto"
    ):  # Main card
        with ui.row().classes("justify-center w-full mt-5"):  # Temperature Thresholds
            ui.label("Temperature Thresholds").classes(
                "text-2xl text-white text-center sm:text-xl"
            )

        input_fields = [  # Input fields for temp thresholds
            ("Min Temperature", "50"),
            ("Low Temperature", "60"),
            ("Mid Temperature", "75"),
            ("Max Temperature", "90"),
        ]

        # Store references to the input fields
        input_references = {}

        for label, value in input_fields:  # Loop through input fields to display them
            with ui.row().classes("justify-center items-center w-full mt-2"):
                ui.label(label).classes("text-lg text-white text-center sm:text-base")
                input_references[label] = ui.input(label, value=value).classes(
                    "w-24 bg-gray-800 mx-2 sm:w-20"
                )
                ui.label("°F").classes("text-lg text-white sm:text-base")

        with ui.row().classes("justify-center w-full mt-5"):  # Save button
            ui.button(
                "Save Settings",
                on_click=lambda: save_settings(
                    input_references["Min Temperature"].value,
                    input_references["Low Temperature"].value,
                    input_references["Mid Temperature"].value,
                    input_references["Max Temperature"].value,
                ),
            ).classes("bg-teal-500 text-white w-full sm:w-auto")
    eco_footer()  # add footer


# Save settings to database or file (not implemented)
def save_settings(min_temp, low_temp, mid_temp, max_temp):
    print(
        f"Saving settings: Min Temperature={min_temp}, Low Temperature={low_temp}, Mid Temperature={mid_temp}, Max Temperature={max_temp}"
    )


@ui.page("/thresholds")  # Route for thresholds page
def thresholds():
    thresholds_page()