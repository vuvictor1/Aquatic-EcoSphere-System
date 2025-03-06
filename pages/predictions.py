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
import asyncio

# Constants
SENSOR_TYPES = ['turbidity', 'total dissolved solids', 'temperature']
END_TIMESTAMP = datetime.now() + timedelta(hours=1)
INTERVAL_MINUTES = 10


def get_target_time(current_time):
    """
    Calculate the target time 10 minutes ahead of the current time.

    Args:
        current_time (datetime): Current time.

    Returns:
        datetime: Target time.
    """
    return current_time + timedelta(minutes=10)


def get_filtered_predictions(predictions, current_time):
    """
    Filter predictions that are only for current time and beyond.

    Args:
        predictions (dict): Dictionary with sensor types as keys and lists of predictions, accuracy, and last reading as values.
        current_time (datetime): Current time.

    Returns:
        list: Filtered predictions.
    """
    return [
        (value, timestamp) for sensor_type, prediction_data in predictions.items()
        for value, timestamp in zip(prediction_data['predictions'], prediction_data['timestamps'])
        if timestamp >= current_time
    ]


def get_closest_prediction(filtered_predictions, target_time):
    """
    Find the prediction closest to the target time.

    Args:
        filtered_predictions (list): Filtered predictions.
        target_time (datetime): Target time.

    Returns:
        tuple: Closest prediction.
    """
    return min(filtered_predictions, key=lambda x: abs(x[1] - target_time))


def display_sensor_data(sensor_type, prediction_data, unit, target_time, closest_prediction):
    """
    Display sensor data.

    Args:
        sensor_type (str): Sensor type.
        prediction_data (dict): Prediction data.
        unit (str): Unit of measurement.
        target_time (datetime): Target time.
        closest_prediction (tuple): Closest prediction.
    """
    with ui.column().classes('outline_label bg-gray-800 rounded-lg shadow-lg p-4').style('align-items: center; margin-bottom: 20px;'):
        # Display sensor type
        ui.label(f'{sensor_type.title()}').classes(
            'text-3xl sm:text-4xl text-white font-bold mt-0')

        # Display last reading
        last_reading = prediction_data["last_reading"]
        ui.label(f'Current Reading: {last_reading:.2f} {unit}').classes(
            'text-lg sm:text-xl text-gray-300 my-2')

        # Display next predicted reading
        predicted_value, predicted_timestamp = closest_prediction
        ui.label(f'Predicted Reading at {target_time.strftime("%Y-%m-%d %H:%M")}: {predicted_value:.2f} {unit}').classes(
            'text-lg sm:text-xl text-blue-500 my-2')

        # Display expected change
        expected_change = predicted_value - last_reading
        expected_change_color = 'text-green-500' if expected_change > 0 else 'text-red-500'
        ui.label(f'Expected Change: {expected_change:+.2f} {unit}').classes(
            f'text-lg sm:text-xl {expected_change_color} my-2')

        # Display model accuracy
        accuracy = prediction_data["accuracy"]
        ui.label(f'Model Accuracy (R² Score): {accuracy:.2f}').classes(
            'text-lg sm:text-xl text-amber-500 my-2')


async def display_predictions(predictions, container, interval_minutes):
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

    current_time = datetime.now()
    target_time = get_target_time(current_time)
    container.clear()  # Clear the container before displaying predictions

    with container:
        for sensor_type, prediction_data in predictions.items():
            unit = sensor_units.get(sensor_type, '')

            filtered_predictions = get_filtered_predictions(
                {sensor_type: prediction_data}, current_time)

            if not filtered_predictions:
                ui.label(f'No upcoming predictions available for {sensor_type}.').classes(
                    'text-lg sm:text-xl text-gray-300')
                continue

            closest_prediction = get_closest_prediction(
                filtered_predictions, target_time)

            display_sensor_data(
                sensor_type, prediction_data, unit, target_time, closest_prediction)
            await asyncio.sleep(0)


def predictions_page():
    """
    Display predictions for the next sensor values.
    """
    # Display the header and inject custom CSS styles
    eco_header()
    inject_style()

    # Create a title
    with ui.row().classes('justify-center w-full mt-0'):
        ui.label('Sensor Predictions').classes(
            'text-3xl sm:text-5xl text-white mt-0')

    # Create a container to display predictions
    predictions_container = ui.row().classes('justify-center w-full mt-0')

    spinner = ui.spinner('audio', size='xl', color='green')
    spinner.set_visibility(False)
    spinner.style('margin:auto; display: block;')

    # Create a button to trigger prediction calculation and display
    with ui.row().classes('justify-center w-full mt-0'):
        async def calculate_predictions():
            # Show the spinner
            spinner.set_visibility(True)
            button.set_text('Loading . . .')
            ui.update()  # Force UI update so the spinner appears

            # Run the computation in a separate thread
            predictions = await asyncio.to_thread(get_predictions, SENSOR_TYPES, END_TIMESTAMP, INTERVAL_MINUTES)

            # Display predictions
            await display_predictions(predictions, predictions_container, INTERVAL_MINUTES)

            # Hide the spinner after computation
            spinner.set_visibility(False)
            button.set_text('Calculate Predictions')
            ui.update()  # Ensure the UI updates

        button = ui.button('Calculate Predictions',
                           on_click=lambda: asyncio.create_task(calculate_predictions()))
    # Display the footer
    eco_footer()


@ui.page('/predictions')
def predictions():
    predictions_page()
