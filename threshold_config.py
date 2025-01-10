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
    The color intensity increases or decreases based on the percentile within the threshold range.
    :param current_temp: The current temperature value.
    :param thresholds: A dictionary containing thresholds and colors.
    :return: A hex color code.
    """
    sorted_thresholds = sorted(thresholds.items(), key=lambda x: x[1]['value'])

    # Find the threshold range the current temperature falls into
    for i in range(len(sorted_thresholds) - 1):
        lower_threshold = sorted_thresholds[i]
        upper_threshold = sorted_thresholds[i + 1]

        if lower_threshold[1]['value'] <= current_temp <= upper_threshold[1]['value']:
            # Calculate the percentile within this range
            range_min = lower_threshold[1]['value']
            range_max = upper_threshold[1]['value']
            percentile = (current_temp - range_min) / (range_max - range_min)

            # Interpolate the color intensity based on the percentile
            base_color = lower_threshold[1]['color']
            intense_color = get_intense_color(base_color, percentile)
            return intense_color

    # If temperature is outside the defined range, return the closest color
    if current_temp < sorted_thresholds[0][1]['value']:
        return sorted_thresholds[0][1]['color']
    else:
        return sorted_thresholds[-1][1]['color']


def get_intense_color(base_color, intensity):
    """
    Adjust the intensity of a base color based on a percentile value.
    :param base_color: The base hex color code.
    :param intensity: A value between 0 and 1 representing the percentile.
    :return: A more intense version of the base color.
    """
    # Convert hex color to RGB
    r = int(base_color[1:3], 16)
    g = int(base_color[3:5], 16)
    b = int(base_color[5:7], 16)

    # Increase intensity for red, decrease for green and blue (for hotter colors)
    r = min(255, r + int(255 * intensity))
    g = max(0, g - int(255 * intensity))
    b = max(0, b - int(255 * intensity))

    # Convert back to hex
    return f'#{r:02x}{g:02x}{b:02x}'


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
