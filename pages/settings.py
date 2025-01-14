from nicegui import ui
from web_functions import inject_style, eco_header


def settings_page():
    """Renders the settings page."""
    eco_header()
    inject_style()

    # Title for the page
    with ui.row().style('justify-content: center; width: 100%; margin-top: 20px;'):
        ui.label('Settings').style('font-size: 32px; color: white;')

    # Temperature Thresholds
    with ui.row().style('justify-content: center; align-items: center;'):
        ui.label('Temperature Thresholds').style(
            'font-size: 24px; color: white;')

    # Input fields for temperature thresholds
    input_fields = [
        ('Min Temperature', '50'),
        ('Low Temperature', '60'),
        ('Mid Temperature', '75'),
        ('Max Temperature', '90'),
    ]

    for label, value in input_fields:
        with ui.row().style('justify-content: center;'):
            ui.label(label).style('font-size: 18px; color: white;')
            input_field = ui.input(label, value=value).style(
                'width: 100px; color: white; background-color: #333333;')
            ui.label('°F').style('font-size: 18px; color: white;')

    # Save Button
    with ui.row().style('justify-content: center;'):
        ui.button('Save', on_click=lambda: save_settings(
            ui.input('Min Temperature').value,
            ui.input('Low Temperature').value,
            ui.input('Mid Temperature').value,
            ui.input('Max Temperature').value,
        )).style('background-color: #3AAFA9; color: white;')


def save_settings(min_temp, low_temp, mid_temp, max_temp):
    """Saves the settings to the database or a file."""
    print(f'Saving settings: Min Temperature={min_temp}, Low Temperature={
          low_temp}, Mid Temperature={mid_temp}, Max Temperature={max_temp}')


@ui.page('/settings')
def settings():
    """Renders the settings page."""
    settings_page()
