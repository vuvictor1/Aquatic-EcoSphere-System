# File: settings.py
# Description: Settings page for thresholds.
from nicegui import ui
from web_functions import inject_style, eco_header, eco_footer


def settings_page():  # Renders the settings page
    eco_header()
    inject_style()

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

    with ui.row().classes('justify-center w-full mt-2'):  # Title for the page
            ui.label('Settings').classes('text-4xl text-white text-center')

    with ui.card().classes('outline_label bg-gray-800 p-5 rounded-lg w-full max-w-2xl mx-auto'):  # Main card

        with ui.row().classes('justify-center w-full mt-5'):  # Temperature Thresholds
            ui.label('Temperature Thresholds').classes('text-2xl text-white text-center')

        input_fields = [  # Input fields for temp thresholds
            ('Min Temperature', '50'),
            ('Low Temperature', '60'),
            ('Mid Temperature', '75'),
            ('Max Temperature', '90'),
        ]

        for label, value in input_fields:  # Loop through input fields to display them
            with ui.row().classes('justify-center items-center w-full mt-2'):
                ui.label(label).classes('text-lg text-white text-center')
                input_field = ui.input(label, value=value).classes(
                    'w-24 bg-gray-800 mx-2')
                ui.label('°F').classes('text-lg text-white')

        with ui.row().classes('justify-center w-full mt-5'):  # Save button
            ui.button('Save Settings', on_click=lambda: save_settings(
                ui.input('Min Temperature').value,
                ui.input('Low Temperature').value,
                ui.input('Mid Temperature').value,
                ui.input('Max Temperature').value,
            )).classes('bg-teal-500 text-white w-full sm:w-auto')
    eco_footer()  # add footer


# Save settings to database or file (not implemented)
def save_settings(min_temp, low_temp, mid_temp, max_temp):
    print(f'Saving settings: Min Temperature={min_temp}, Low Temperature={low_temp}, Mid Temperature={mid_temp}, Max Temperature={max_temp}')


@ui.page('/settings')  # Route for settings page
def settings():
    settings_page()