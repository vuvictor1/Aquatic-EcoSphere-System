# Authors: Jordan Morris and Victor Vu
# File: settings.py
# Description: Settings page for thresholds.
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui
from web_functions import inject_style, eco_header, eco_footer

def settings_page(): # Renders the settings page
    eco_header()
    inject_style()

    # Inject custom CSS styles
    ui.html("""
        <style>
            .q-field__native {
                color: white;
            }
            .q-field__label {
                color: white;
            }
            @media (max-width: 600px) {
                .q-field__native, .q-field__label {
                    font-size: 14px;
                }
                .q-field__label {
                    text-align: center;
                }
            }
        </style>
    """)

    with ui.card().style('background-color: #333333; padding: 20px; border-radius: 10px; width: 90%; max-width: 800px; margin: auto;'): # Main card
        with ui.row().style('justify-content: center; width: 100%; margin-top: 10px;'): # Title for the page
            ui.label('Settings').style('font-size: 32px; color: white;')

        with ui.row().style('justify-content: center; width: 100%; margin-top: 20px;'): # Temperature Thresholds 
            ui.label('Temperature Thresholds').style('font-size: 24px; color: white;')

        input_fields = [ # Input fields for temp thresholds
            ('Min Temperature', '50'),
            ('Low Temperature', '60'),
            ('Mid Temperature', '75'),
            ('Max Temperature', '90'),
        ]

        for label, value in input_fields: # Loop through input fields to display them
            with ui.row().style('justify-content: center; align-items: center; width: 100%; margin-top: 10px;'):
                ui.label(label).style('font-size: 18px; color: white; text-align: center;')
                input_field = ui.input(label, value=value).style(
                    'width: 100px; background-color: #333333; margin-left: 10px; margin-right: 10px;')
                ui.label('°F').style('font-size: 18px; color: white;')

        with ui.row().style('justify-content: center; width: 100%; margin-top: 20px;'): # Save button
            ui.button('Save', on_click=lambda: save_settings(
                ui.input('Min Temperature').value,
                ui.input('Low Temperature').value,
                ui.input('Mid Temperature').value,
                ui.input('Max Temperature').value,
            )).style('background-color: #3AAFA9; color: white;')
    eco_footer() # add footer

def save_settings(min_temp, low_temp, mid_temp, max_temp): # Save settings to database or file (not implemented)
    print(f'Saving settings: Min Temperature={min_temp}, Low Temperature={low_temp}, Mid Temperature={mid_temp}, Max Temperature={max_temp}')

@ui.page('/settings') # Route for settings page
def settings():
    settings_page()