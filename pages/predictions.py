# File: predictions.py
# Description: Page for basic machine learning future predictions

import numpy as np
from datetime import datetime, timedelta
from nicegui import ui
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from web_functions import inject_style, eco_footer, eco_header
from collect_database import get_latest_data, get_all_data
from ml_model import get_predictions

# Constants
SENSOR_TYPES = ['turbidity', 'total dissolved solids', 'temperature']
END_TIMESTAMP = datetime.now() + timedelta(hours=1)
INTERVAL_MINUTES = 10


def predictions_page():
    """
    Display predictions for the next sensor values.
    """
    # Display the header and inject custom CSS styles
    eco_header()
    inject_style()

    # Create a title
    with ui.row().classes('justify-center w-full'):
        ui.label('Sensor Predictions').classes(
            'text-3xl sm:text-5xl text-white')

    # Create a container to display predictions
    predictions_container = ui.row().classes('justify-center w-full')

    # Create a button to trigger prediction calculation and display
    with ui.row().classes('justify-center w-full'):
        ui.button('Calculate Predictions', on_click=lambda: (
            display_predictions(get_predictions(
                SENSOR_TYPES, END_TIMESTAMP, INTERVAL_MINUTES), predictions_container, INTERVAL_MINUTES)
        ))

    # Display the footer
    eco_footer()


def display_predictions(predictions, container, interval_minutes):
    """
    Display the predictions for the next sensor values.

    Args:
        predictions (dict): Dictionary with sensor types as keys and lists of predictions, accuracy, and last reading as values.
        container (ui.row): Container to display the predictions.
    """
    sensor_units = {  # sensor_type: unit
        'total dissolved solids': 'ppm',
        'turbidity': 'NTU',
        'temperature': '°F'
    }
    container.clear()  # Clear the container before displaying predictions
    with container:
        for sensor_type, prediction_data in predictions.items():
            unit = sensor_units.get(sensor_type, '')
            with ui.column().classes('outline_label bg-gray-800 rounded-lg shadow-lg p-4').style('align-items: center; margin-bottom: 20px;'):
                # Display sensor type
                ui.label(f'{sensor_type.title()}').classes(
                    'text-3xl sm:text-4xl text-white font-bold')

                # Display last reading
                last_reading = prediction_data["last_reading"]
                ui.label(f'Current Reading: {last_reading:.2f} {unit}').classes(
                    'text-lg sm:text-xl text-gray-300')  # Lighter gray

                # Display next predicted reading
                next_predicted_value = prediction_data['predictions'][0]
                next_timestamp = prediction_data['timestamps'][0]
                ui.label(f'Next Predicted Reading: {next_timestamp.strftime("%Y-%m-%d %H:%M")}: {next_predicted_value:.2f} {unit}').classes(
                    'text-lg sm:text-xl text-blue-500')  # Blue

                # Display expected change
                expected_change = next_predicted_value - last_reading
                expected_change_color = 'text-green-500' if expected_change > 0 else 'text-red-500'
                ui.label(f'Expected Change: {expected_change:+.2f} {unit}').classes(
                    f'text-lg sm:text-xl {expected_change_color}')

                # Display model accuracy
                accuracy = prediction_data["accuracy"]
                ui.label(f'Model Accuracy (R² Score): {accuracy:.2f}').classes(
                    'text-lg sm:text-xl text-amber-500')  # Gold color

                # Print the many predictions
                print(
                    f"Predictions for {sensor_type} (every {interval_minutes} minutes):")
                for i, (predicted_value, timestamp) in enumerate(zip(prediction_data['predictions'], prediction_data['timestamps'])):
                    print(
                        f"  {timestamp.strftime('%Y-%m-%d %H:%M')}: {predicted_value:.2f} {unit}")


@ui.page('/predictions')
def predictions():
    predictions_page()
