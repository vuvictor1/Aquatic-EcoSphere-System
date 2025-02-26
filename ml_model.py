# File: ml_model.py
# Description: Machine learning model for predicting sensor values

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from collect_database import get_all_data

# Constants
WINDOW_SIZE = 50  # Number of past values to use for prediction
TEST_SIZE = 0.1  # Proportion of data to use for testing
RANDOM_STATE = 42  # Random state for reproducibility
N_ESTIMATORS = 20  # Number of estimators for the random forest model

# TODO:
# 1. Implement partial fit for random forest tree for improving model
# 2. Other incremental learning practices


def prepare_data(sensor_type: str) -> tuple:
    """
    Prepares dataset with a larger window of past values.

    Args:
        sensor_type (str): Type of sensor data to prepare.

    Returns:
        tuple: X_train, X_test, y_train, y_test, latest_data
    """
    # Load all data
    data = get_all_data()

    # Check if sensor type has sufficient data
    if not is_sufficient_data(data, sensor_type):
        print(f"Warning: Not enough data for {sensor_type}.")
        return None, None, None, None, None

    # Create a DataFrame from the sensor data
    df = create_dataframe(data, sensor_type)

    # Generate lag features using all available past readings
    df = add_lag_features(df)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(df)

    # Get the most recent sample for future prediction
    latest_data = get_latest_data(df)

    return X_train, X_test, y_train, y_test, latest_data


def is_sufficient_data(data, sensor_type):
    return sensor_type in data and len(data[sensor_type]) >= 5


def create_dataframe(data, sensor_type):
    df = pd.DataFrame(data[sensor_type])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values(by='timestamp', inplace=True)
    return df


def add_lag_features(df):
    for i in range(1, WINDOW_SIZE + 1):
        df[f'lag_{i}'] = df['value'].shift(i)
    df.dropna(inplace=True)
    return df


def split_data(df):
    X = df[[f'lag_{i}' for i in range(1, WINDOW_SIZE + 1)]].values
    y = df['value'].values
    return train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)


def get_latest_data(df):
    last_reading = df.iloc[-1]['value']
    latest_X = df.iloc[-1][[f'lag_{i}' for i in range(
        1, WINDOW_SIZE + 1)]].values.reshape(1, -1)
    return latest_X, last_reading


def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestRegressor:
    """
    Trains a Random Forest Regressor model.

    Args:
        X_train (np.ndarray): Training input data.
        y_train (np.ndarray): Training target data.

    Returns:
        RandomForestRegressor: Trained model.
    """
    model = RandomForestRegressor(
        n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    return model


def get_predictions(sensor_types, end_timestamp, interval_minutes=10) -> dict:
    """
    Returns the predictions and accuracy for each sensor type.

    Args:
        sensor_types (list): List of sensor types.
        end_timestamp (datetime): End timestamp for predictions.
        interval_minutes (int): Interval between predictions in minutes.

    Returns:
        dict: Dictionary with sensor types as keys and lists of predictions, accuracy, and last reading as values.
    """
    predictions = {}
    for sensor_type in sensor_types:
        X_train, X_test, y_train, y_test, latest_data = prepare_data(
            sensor_type)
        if X_train is not None:
            model = train_model(X_train, y_train)
            latest_X, last_reading = latest_data
            accuracy = calculate_accuracy(model, X_test, y_test)

            # Generate multiple predictions
            predicted_values = []
            predicted_timestamps = []
            current_timestamp = pd.to_datetime(
                get_all_data()[sensor_type][-1]['timestamp'])
            while current_timestamp < end_timestamp:
                next_prediction = model.predict(latest_X)[0]
                predicted_values.append(next_prediction)
                predicted_timestamps.append(current_timestamp)
                latest_X = np.roll(latest_X, -1)  # Shift the input values
                latest_X[-1] = next_prediction  # Update the last input value
                current_timestamp += pd.Timedelta(minutes=interval_minutes)

            predictions[sensor_type] = {
                'predictions': predicted_values,
                'timestamps': predicted_timestamps,
                'accuracy': accuracy,
                'last_reading': last_reading
            }
    return predictions


def calculate_accuracy(model: RandomForestRegressor, X_test: np.ndarray, y_test: np.ndarray) -> float:
    """
    Calculates the accuracy of the model.

    Args:
        model (RandomForestRegressor): Trained model.
        X_test (np.ndarray): Testing input data.
        y_test (np.ndarray): Testing target data.

    Returns:
        float: R² score.
    """
    return model.score(X_test, y_test)


def main() -> None:
    sensor_types = ['turbidity', 'total dissolved solids', 'temperature']

    for sensor_type in sensor_types:
        print(f"\nTraining model for {sensor_type}...")

        X_train, X_test, y_train, y_test, latest_data = prepare_data(
            sensor_type)
        if X_train is None:
            print(f"Skipping {sensor_type} due to insufficient data.")
            continue

        model = train_model(X_train, y_train)
        latest_X, last_reading = latest_data
        next_prediction = model.predict(latest_X)[0]
        expected_change = next_prediction - last_reading
        accuracy = calculate_accuracy(model, X_test, y_test)

        # Print predictions first
        print(f"\n--- {sensor_type.title()} Prediction ---")
        print(f"Last Reading: {last_reading:.2f}")
        print(f"Predicted Next Value: {next_prediction:.2f}")
        print(f"Expected Change: {expected_change:+.2f}")
        print(f"Model Accuracy (R² Score): {accuracy:.2f}")
        print("----------------------------")


if __name__ == "__main__":
    main()
