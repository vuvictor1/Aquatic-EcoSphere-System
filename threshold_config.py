# Authors: Jordan Morris and Victor Vu
# File: threshold_config.py
# Description: Handles threshold and color configuration for sensor data.
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html

DEFAULT_TEMPERATURE_THRESHOLDS = {  # Default thresholds/colors for temp
    "min": {"value": 50, "color": "bg-blue-200"},  # light blue
    "low": {"value": 60, "color": "bg-green-200"},  # light green
    "mid": {"value": 80, "color": "bg-red-200"},  # light red
    "max": {"value": 90, "color": "bg-red-500"},  # intense red
}

DEFAULT_TDS_THRESHOLDS = {  # Default thresholds/colors for TDS
    "min": {"value": 0, "color": "bg-blue-200"},  # light blue
    "low": {"value": 500, "color": "bg-green-200"},  # light green
    "mid": {"value": 1000, "color": "bg-red-200"},  # light red
    "max": {"value": 2000, "color": "bg-red-500"},  # intense red
}

DEFAULT_TURBIDITY_THRESHOLDS = {  # Default thresholds/colors for turbidity
    "min": {"value": 0, "color": "bg-blue-200"},  # light blue
    "low": {"value": 5, "color": "bg-green-200"},  # light green
    "mid": {"value": 50, "color": "bg-red-200"},  # light red
    "max": {"value": 100, "color": "bg-red-500"},  # intense red
}

# User-defined thresholds (initially set to default)
temperature_thresholds = DEFAULT_TEMPERATURE_THRESHOLDS.copy()
tds_thresholds = DEFAULT_TDS_THRESHOLDS.copy()
turbidity_thresholds = DEFAULT_TURBIDITY_THRESHOLDS.copy()

def set_temperature_thresholds(new_thresholds: dict) -> None:
    """
    Set temperature thresholds.
    :param new_thresholds: A dictionary containing new thresholds and colors.
    """
    global temperature_thresholds
    temperature_thresholds = new_thresholds

def get_temperature_thresholds() -> dict:
    """
    Get temperature thresholds.
    :return: A dictionary of thresholds.
    """
    return temperature_thresholds

def interpolate_color(current_temp: float, thresholds: dict) -> str:
    """
    Interpolate the color based on the current temperature and thresholds.
    The color intensity increases or decreases based on the percentile within the threshold range.
    :param current_temp: The current temperature value.
    :param thresholds: A dictionary containing thresholds and colors.
    :return: A Tailwind CSS class.
    """
    try:
        sorted_thresholds = sorted(thresholds.items(), key=lambda x: x[1]["value"])

        for i in range(len(sorted_thresholds) - 1):  # Find the range current_temp falls into
            lower_threshold = sorted_thresholds[i]
            upper_threshold = sorted_thresholds[i + 1]
            if lower_threshold[1]["value"] <= current_temp <= upper_threshold[1]["value"]:
                return lower_threshold[1]["color"]

        if current_temp < sorted_thresholds[0][1]["value"]:  # If temp is below the lowest threshold
            return sorted_thresholds[0][1]["color"]
        else:
            return sorted_thresholds[-1][1]["color"]

    except Exception as e:  # Handle exceptions
        print(f"An error occurred: {e}")
        return None