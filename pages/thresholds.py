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

    with ui.card().classes(
        "outline_label bg-gray-800 p-5 rounded-lg w-full max-w-2xl mx-auto mt-0"
    ):  # Main card
        with ui.row().classes("justify-center w-full mt-0"):  # Temperature Thresholds
            ui.label("Temperature Thresholds").classes(
                "text-2xl text-white text-center sm:text-xl mt-0"
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
            with ui.row().classes("justify-center items-center w-full my-2"):
                ui.label(label).classes("text-lg text-white text-center sm:text-base mt-0")
                input_references[label] = ui.input(label, value=value).classes(
                    "w-24 bg-gray-800 mx-2 sm:w-20 mt-0"
                )
                ui.label("°F").classes("text-lg text-white sm:text-base mt-0")

        with ui.row().classes("justify-center w-full my-2"):  # Save button
            ui.button(
                "Save",
                on_click=lambda: save_settings(
                    input_references["Min Temperature"].value,
                    input_references["Low Temperature"].value,
                    input_references["Mid Temperature"].value,
                    input_references["Max Temperature"].value,
                ),
            ).classes("bg-teal-500 text-white w-full sm:w-auto mt-0")

    with ui.card().classes(
        "outline_label bg-gray-800 p-5 rounded-lg w-full max-w-2xl mx-auto my-2"
    ):  # Turbidity card
        with ui.row().classes("justify-center w-full mt-0"):  # Turbidity Thresholds
            ui.label("Turbidity Thresholds").classes(
                "text-2xl text-white text-center sm:text-xl mt-0"
            )

        turbidity_fields = [  # Input fields for turbidity thresholds
            ("Min Turbidity", "0"),
            ("Low Turbidity", "25"),
            ("Mid Turbidity", "50"),
            ("Max Turbidity", "100"),
        ]

        # Store references to the turbidity input fields
        turbidity_references = {}

        for label, value in turbidity_fields:  # Loop through input fields to display them
            with ui.row().classes("justify-center items-center w-full my-2"):
                ui.label(label).classes("text-lg text-white text-center sm:text-base mt-0")
                turbidity_references[label] = ui.input(label, value=value).classes(
                    "w-24 bg-gray-800 mx-2 sm:w-20 mt-0"
                )
                ui.label("NTU").classes("text-lg text-white sm:text-base mt-0")

        with ui.row().classes("justify-center w-full my-2"):  # Save button
            ui.button(
                "Save",
                on_click=lambda: save_turbidity_settings(
                    turbidity_references["Min Turbidity"].value,
                    turbidity_references["Low Turbidity"].value,
                    turbidity_references["Mid Turbidity"].value,
                    turbidity_references["Max Turbidity"].value,
                ),
            ).classes("bg-teal-500 text-white w-full sm:w-auto mt-0")

    with ui.card().classes(
        "outline_label bg-gray-800 p-5 rounded-lg w-full max-w-2xl mx-auto my-2"
    ):  # TDS card
        with ui.row().classes("justify-center w-full mt-0"):  # TDS Thresholds
            ui.label("Total Dissolved Solids Thresholds").classes(
                "text-2xl text-white text-center sm:text-xl mt-0"
            )

        tds_fields = [  # Input fields for TDS thresholds
            ("Min TDS", "0"),
            ("Low TDS", "300"),
            ("Mid TDS", "600"),
            ("Max TDS", "1000"),
        ]

        # Store references to the TDS input fields
        tds_references = {}

        for label, value in tds_fields:  # Loop through input fields to display them
            with ui.row().classes("justify-center items-center w-full my-2"):
                ui.label(label).classes("text-lg text-white text-center sm:text-base mt-0")
                tds_references[label] = ui.input(label, value=value).classes(
                    "w-24 bg-gray-800 mx-2 sm:w-20 mt-0"
                )
                ui.label("ppm").classes("text-lg text-white sm:text-base mt-0")

        with ui.row().classes("justify-center w-full my-2"):  # Save button
            ui.button(
                "Save",
                on_click=lambda: save_tds_settings(
                    tds_references["Min TDS"].value,
                    tds_references["Low TDS"].value,
                    tds_references["Mid TDS"].value,
                    tds_references["Max TDS"].value,
                ),
            ).classes("bg-teal-500 text-white w-full sm:w-auto mt-0")

    eco_footer()  # add footer


# Save settings to database or file (not implemented)
def save_settings(min_temp, low_temp, mid_temp, max_temp):
    print(
        f"Saving settings: Min Temperature={min_temp}, Low Temperature={low_temp}, Mid Temperature={mid_temp}, Max Temperature={max_temp}"
    )

# Save turbidity settings to database or file (not implemented)
def save_turbidity_settings(min_turbidity, low_turbidity, mid_turbidity, max_turbidity):
    print(
        f"Saving turbidity settings: Min Turbidity={min_turbidity}, Low Turbidity={low_turbidity}, Mid Turbidity={mid_turbidity}, Max Turbidity={max_turbidity}"
    )

# Save TDS settings to database or file (not implemented)
def save_tds_settings(min_tds, low_tds, mid_tds, max_tds):
    print(
        f"Saving TDS settings: Min TDS={min_tds}, Low TDS={low_tds}, Mid TDS={mid_tds}, Max TDS={max_tds}"
    )


@ui.page("/thresholds")  # Route for thresholds page
def thresholds():
    thresholds_page()