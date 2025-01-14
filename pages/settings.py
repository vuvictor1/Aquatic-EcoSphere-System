from nicegui import ui
from web_functions import inject_style, eco_header


def settings_page():
    eco_header()
    inject_style()

    with ui.row().style('justify-content: center; width: 100%; margin-top: 20px;'):  # Title for the page
        ui.label('Graphing').style('font-size: 32px; color: white;')

    # Temperature Thresholds
    with ui.row().style('justify-content: center; align-items: center;'):
        ui.label('Temperature Thresholds').style(
            'font-size: 24px; color: white;')

    with ui.row().style('justify-content: center;'):
        ui.label('Min Temperature').style('font-size: 18px; color: white;')
        min_temp_input = ui.input('Min Temperature', value='50').style(
            'width: 100px; color: white; background-color: #333333;')
        ui.label('°F').style('font-size: 18px; color: white;')

    with ui.row().style('justify-content: center;'):
        ui.label('Low Temperature').style('font-size: 18px; color: white;')
        low_temp_input = ui.input(
            'Low Temperature', value='60').style('width: 100px;')
        ui.label('°F').style('font-size: 18px; color: white;')

    with ui.row().style('justify-content: center;'):
        ui.label('Mid Temperature').style('font-size: 18px; color: white;')
        mid_temp_input = ui.input(
            'Mid Temperature', value='75').style('width: 100px;')
        ui.label('°F').style('font-size: 18px; color: white;')

    with ui.row().style('justify-content: center;'):
        ui.label('Max Temperature').style('font-size: 18px; color: white;')
        max_temp_input = ui.input(
            'Max Temperature', value='90').style('width: 100px;')
        ui.label('°F').style('font-size: 18px; color: white;')

    # Save Button
    with ui.row().style('justify-content: center;'):
        ui.button('Save', on_click=lambda: save_settings(min_temp_input.value, low_temp_input.value,
                                                         mid_temp_input.value, max_temp_input.value)).style('background-color: #3AAFA9; color: white;')


def save_settings(min_temp, low_temp, mid_temp, max_temp):
    # Save the settings to the database or a file
    print(f'Saving settings: Min Temperature={min_temp}, Low Temperature={
          low_temp}, Mid Temperature={mid_temp}, Max Temperature={max_temp}')


@ui.page('/settings')
def settings():
    settings_page()
