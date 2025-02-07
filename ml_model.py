# ml_model.py
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from collect_database import get_all_data
import numpy as np
import pandas as pd

# Constants
WINDOW_SIZE = 20  # 20
TEST_SIZE = 0.1  # .2
RANDOM_STATE = 42  # 42
N_ESTIMATORS = 20  # 20

# Prepare data function


def prepare_data(sensor_type: str) -> tuple:
    """
    Prepares dataset with a larger window of past values.

    Args:
        sensor_type (str): Type of sensor data to prepare.

    Returns:
        tuple: X_train, X_test, y_train, y_test, latest_data
    """
    data = get_all_data()

    if sensor_type not in data or len(data[sensor_type]) < WINDOW_SIZE + 1:
        print(f"Warning: Not enough data for {sensor_type}.")
        return None, None, None, None, None

    df = pd.DataFrame(data[sensor_type])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values(by='timestamp', inplace=True)

    # Generate lag features using ALL available past readings
    for i in range(1, WINDOW_SIZE + 1):
        df[f'lag_{i}'] = df['value'].shift(i)

    df.dropna(inplace=True)  # Remove NaNs from shifting

    # Train-test split
    X = df[[f'lag_{i}' for i in range(1, WINDOW_SIZE + 1)]].values
    y = df['value'].values
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)

    # Get the most recent sample for future prediction
    last_reading = df.iloc[-1]['value']
    latest_X = X[-1].reshape(1, -1)  # Latest input values for prediction

    return X_train, X_test, y_train, y_test, (latest_X, last_reading)

# Train model using Random Forest


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


def get_predictions(sensor_types):
    """
    Returns the predictions and accuracy for each sensor type.

    Args:
        sensor_types (list): List of sensor types.

    Returns:
        dict: Dictionary with sensor types as keys and tuples of predictions, accuracy, and last reading as values.
    """
    predictions = {}
    for sensor_type in sensor_types:
        X_train, X_test, y_train, y_test, latest_data = prepare_data(
            sensor_type)
        if X_train is not None:
            model = train_model(X_train, y_train)
            latest_X, last_reading = latest_data
            next_prediction = model.predict(latest_X)[0]
            accuracy = calculate_accuracy(model, X_test, y_test)
            predictions[sensor_type] = (
                next_prediction, accuracy, last_reading)
    return predictions

# Evaluate accuracy


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

# Main function


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
