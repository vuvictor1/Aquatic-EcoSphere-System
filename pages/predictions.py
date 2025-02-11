# File: predictions.py
# Description: Page for basic machine learning future predictions
from sklearn.metrics import mean_squared_error
from nicegui import ui
from web_functions import inject_style, eco_footer, eco_header
from collect_database import get_latest_data, get_all_data
from ml_model import get_predictions
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
from datetime import datetime, timedelta


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

    print("Predictions not calculated yet")
    # Create a container to display predictions
    predictions_container = ui.row().classes('justify-center w-full')

    print("Container made")
    # Create a container to display predictions graph
    predictions_graph_container = ui.row().classes('justify-center w-full')

    print("Graph container made")
    # Create a button to trigger prediction calculation and display
    with ui.row().classes('justify-center w-full'):
        ui.button('Calculate Predictions', on_click=lambda: (
            display_predictions(get_predictions(
                sensor_types), predictions_container),
            display_predictions_graph(get_predictions(
                sensor_types), predictions_graph_container)
        ))

    print("Predictions printed.")
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


def display_predictions_graph(predictions, container):
    """
    Display the predictions graph for the next sensor values.
    """
    sensor_units = {  # sensor_type: unit
        'total dissolved solids': 'ppm',
        'turbidity': 'NTU',
        'temperature': '°F'
    }
    container.clear()  # Clear the container before displaying predictions graph
    with container:
        for sensor_type, (next_prediction, accuracy, last_reading) in predictions.items():
            unit = sensor_units.get(sensor_type, '')
            with ui.column().classes('outline_label bg-gray-800 rounded-lg shadow-lg p-4').style('align-items: center; margin-bottom: 20px;'):
                ui.label(f'{sensor_type.title()}').classes(
                    'text-xl sm:text-2xl text-white')
                timestamps = []  # list to store timestamps
                sensor_values = []  # list to store sensor values

                # Generate timestamps and sensor values for the next hour
                for i in range(60):  # 60 minutes in an hour
                    timestamp = (datetime.now() +
                                 timedelta(minutes=i)).strftime('%m-%d %H:%M')
                    timestamps.append(timestamp)
                    # Use the ml_model to predict the next value
                    # For simplicity, let's assume the model predicts the same value for the next hour
                    # In a real-world scenario, you would use the model to predict the next value based on the current value and other factors
                    sensor_values.append(next_prediction)

                # Calculate y-axis range
                min_value = min(sensor_values)
                max_value = max(sensor_values)
                distance_padding = 0.10  # padding for y-axis
                y_min = max(0, min_value - distance_padding *
                            (max_value - min_value))
                y_max = max_value + distance_padding * (max_value - min_value)

                with ui.column():
                    ui.echart({  # Create an ECharts graph
                        'title': {'text': sensor_type.title(), 'textStyle': {'color': '#FFFFFF'}},
                        'tooltip': {'trigger': 'axis', 'textStyle': {'color': '#rgb(16, 15, 109)'}},
                        'xAxis': {'type': 'category', 'data': timestamps, 'axisLabel': {'color': '#FFFFFF'}},
                        'yAxis': {
                            'type': 'value',
                            'axisLabel': {'color': '#FFFFFF'},
                            'min': round(y_min, 0),
                            'max': round(y_max, 0)
                        },
                        'series': [{
                            'data': sensor_values,
                            'type': 'line',
                            'name': sensor_type,
                            'smooth': True,
                            'areaStyle': {}
                        }],
                        'toolbox': {'feature': {'saveAsImage': {}}},
                    }).classes('w-full sm:w-96 h-72')


@ui.page('/predictions')  # Route to graphs page
def predictions():
    predictions_page()


@ui.page('/predictions')  # Route to graphs page
def predictions():
    predictions_page()
