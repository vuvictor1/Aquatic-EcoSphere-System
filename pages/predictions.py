from nicegui import ui
from web_functions import eco_header, eco_footer, inject_style
from collect_database import get_latest_data
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from collect_database import get_all_data
import numpy as np


def predictions_page():
    """
    Display predictions for the next sensor values.
    """
    # Display the header and inject custom CSS styles
    eco_header()
    inject_style()

    # Display the footer
    eco_footer()


def prepare_data(latest_data, sensor_types):
    """
    Prepare the data for training by splitting it into features (X) and target values (y).
    """
    X = []
    y = []
    for sensor_type in sensor_types:
        values = [entry['value'] for entry in get_all_data(
            sensor_type)]  # get the list of values
        for i in range(len(values) - 1):  # iterate over the values
            X.append([values[i]])  # use the current value as a feature
            y.append(values[i + 1])  # use the next value as a target value
    return X, y


def train_model(X, y):
    """
    Train a linear regression model using the prepared data.
    """
    model = LinearRegression()
    model.fit(np.array(X).reshape(-1, 1), np.array(y))
    return model


def make_predictions(model, X):
    """
    Make predictions on the next sensor values using the trained model.
    """
    next_values = model.predict(np.array(X).reshape(-1, 1))
    return next_values


def display_predictions(next_values, sensor_types):
    """
    Display the predictions for the next sensor values.
    """
    with ui.row().classes('justify-center w-full'):
        ui.label('Predictions for the next sensor values:').classes(
            'text-2xl sm:text-4xl text-white')
        for i, sensor_type in enumerate(sensor_types):
            ui.label(f'{sensor_type.title()}: {next_values[i]:.2f}').classes(
                'text-xl sm:text-2xl text-white')


@ui.page('/predictions')  # Route to graphs page
def graphs():
    predictions_page()
