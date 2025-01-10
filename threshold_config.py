# threshold_config.py
# Description: Handles threshold and color configuration for sensor data.
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html

# Default thresholds and colors for temperature
DEFAULT_TEMPERATURE_THRESHOLDS = {
    'min': {'value': 50, 'color': '#ADD8E6'},  # Light blue
    'low': {'value': 60, 'color': '#90EE90'},  # Light green
    'mid': {'value': 75, 'color': '#FFA07A'},  # Light red
    'max': {'value': 90, 'color': '#FF0000'}   # Intense red
}

# User-defined thresholds (initially set to default)
temperature_thresholds = DEFAULT_TEMPERATURE_THRESHOLDS.copy()


def set_temperature_thresholds(new_thresholds):
    """
    Update the temperature thresholds with user-defined values.
    :param new_thresholds: A dictionary containing new thresholds and colors.
    """
    global temperature_thresholds
    temperature_thresholds = new_thresholds


def get_temperature_thresholds():
    """
    Get the current temperature thresholds.
    :return: A dictionary containing the current thresholds and colors.
    """
    return temperature_thresholds


def interpolate_color(current_temp, thresholds):
    """
    Interpolate the color based on the current temperature and thresholds.
    :param current_temp: The current temperature value.
    :param thresholds: A dictionary containing thresholds and colors.
    :return: A hex color code.
    """
    sorted_thresholds = sorted(thresholds.items(), key=lambda x: x[1]['value'])
    for i in range(len(sorted_thresholds) - 1):
        lower_threshold = sorted_thresholds[i]
        upper_threshold = sorted_thresholds[i + 1]

        if lower_threshold[1]['value'] <= current_temp <= upper_threshold[1]['value']:
            # Linear interpolation between the two colors
            lower_color = lower_threshold[1]['color']
            upper_color = upper_threshold[1]['color']
            ratio = (current_temp - lower_threshold[1]['value']) / (
                upper_threshold[1]['value'] - lower_threshold[1]['value'])
            return interpolate_hex_color(lower_color, upper_color, ratio)

    # If temperature is outside the defined range, return the closest color
    if current_temp < sorted_thresholds[0][1]['value']:
        return sorted_thresholds[0][1]['color']
    else:
        return sorted_thresholds[-1][1]['color']


def interpolate_hex_color(color1, color2, ratio):
    """
    Interpolate between two hex colors.
    :param color1: The starting hex color.
    :param color2: The ending hex color.
    :param ratio: The interpolation ratio (0 to 1).
    :return: A hex color code.
    """
    # Convert hex colors to RGB
    r1, g1, b1 = int(color1[1:3], 16), int(
        color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(
        color2[3:5], 16), int(color2[5:7], 16)

    # Interpolate RGB values
    r = int(r1 + (r2 - r1) * ratio)
    g = int(g1 + (g2 - g1) * ratio)
    b = int(b1 + (b2 - b1) * ratio)

    # Convert back to hex
    return f'#{r:02x}{g:02x}{b:02x}'
