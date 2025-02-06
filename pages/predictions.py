from sklearn.metrics import mean_squared_error
from nicegui import ui
from web_functions import inject_style, eco_footer, eco_header
from collect_database import get_latest_data, get_all_data
from ml_model import get_predictions
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np


def predictions_page():
    """
    Display predictions for the next sensor values.
    """
    # Display the header and inject custom CSS styles
    eco_header()
    inject_style()

    # Title
    with ui.row().classes('justify-center w-full'):
        ui.label('Sensor Predictions').classes(
            'text-3xl sm:text-5xl text-white')

    # Define sensor types
    sensor_types = ['turbidity', 'total dissolved solids', 'temperature']

    # Create a container to display predictions
    predictions_container = ui.row().classes('justify-center w-full')

    # loading_indicator
    loading_indicator = ui.label('').classes(
        'text-lg sm:text-xl text-gray-400 justify-center w-full')

    # Create a button to trigger prediction calculation and display
    with ui.row().classes('justify-center w-full'):
        ui.button('Calculate Predictions', on_click=lambda: [
            loading_indicator.set_text('Calculating predictions...'),
            predictions_container.clear(),
            ui.timer(0.5, lambda: [
                display_predictions(get_predictions(
                    sensor_types), predictions_container),
                # Clear the loading indicator
                loading_indicator.set_text('Placeholder text')
            ])
        ])

    # Display the footer
    eco_footer()


def display_predictions(predictions, container):
    """
    Display the predictions for the next sensor values.
    """
    sensor_units = {  # sensor_type: unit
        'total dissolved solids': 'ppm',
        'turbidity': 'NTU',
        'temperature': '°F'
    }
    container.clear()  # Clear the container before displaying predictions
    with container:
        for sensor_type, (next_prediction, accuracy, last_reading) in predictions.items():
            unit = sensor_units.get(sensor_type, '')
            with ui.column().classes('outline_label bg-gray-800 rounded-lg shadow-lg p-4').style('align-items: center; margin-bottom: 20px;'):
                ui.label(f'{sensor_type.title()}').classes(
                    'text-xl sm:text-2xl text-white')
                ui.label(f'Last Reading: {last_reading:.2f} {unit}').classes(
                    'text-lg sm:text-xl text-gray-400')  # Gray color for last reading
                ui.label(f'Predicted Next Value: {next_prediction:.2f} {unit}').classes(
                    'text-lg sm:text-xl text-blue-500')  # Blue color for predicted next value
                ui.label(f'Expected Change: {next_prediction - last_reading:+.2f} {unit}').classes(
                    # Green color for positive change, red color for negative change
                    'text-lg sm:text-xl text-green-500' if next_prediction - last_reading > 0 else 'text-lg sm:text-xl text-red-500')
                ui.label(f'Model Accuracy (R² Score): {accuracy:.2f}').classes(
                    'text-lg sm:text-xl text-yellow-500')  # Yellow color for model accuracy


@ui.page('/predictions')  # Route to graphs page
def predictions():
    predictions_page()
