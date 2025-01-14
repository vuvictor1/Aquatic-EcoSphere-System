# threshold_config.py
# Description: Handles threshold and color configuration for sensor data.
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html

# Default thresholds and colors for temperature
DEFAULT_TEMPERATURE_THRESHOLDS = {
    'min': {'value': 50, 'color': '#ADD8E6'},  # Light blue
    'low': {'value': 60, 'color': '#90EE90'},  # Light green
    'mid': {'value': 80, 'color': '#FFA07A'},  # Light red
    'max': {'value': 90, 'color': '#FF0000'}   # Intense red
}

# User-defined thresholds (initially set to default)
temperature_thresholds = DEFAULT_TEMPERATURE_THRESHOLDS.copy()

# Maximum color intensity value
MAX_COLOR_INTENSITY = 255


def set_temperature_thresholds(new_thresholds: dict) -> None:
    """
    Update the temperature thresholds with user-defined values.
    :param new_thresholds: A dictionary containing new thresholds and colors.
    """
    global temperature_thresholds
    temperature_thresholds = new_thresholds


def get_temperature_thresholds() -> dict:
    """
    Get the current temperature thresholds.
    :return: A dictionary containing the current thresholds and colors.
    """
    return temperature_thresholds


def interpolate_color(current_temp: float, thresholds: dict) -> str:
    """
    Interpolate the color based on the current temperature and thresholds.
    The color intensity increases or decreases based on the percentile within the threshold range.
    :param current_temp: The current temperature value.
    :param thresholds: A dictionary containing thresholds and colors.
    :return: A hex color code.
    """
    try:
        # print(f"Interpolating color for temperature: {current_temp}°F")
        # print(f"Thresholds: {thresholds}")

        sorted_thresholds = sorted(
            thresholds.items(), key=lambda x: x[1]['value'])
        # print(f"Sorted thresholds: {sorted_thresholds}")

        # Find the threshold range the current temperature falls into
        for i in range(len(sorted_thresholds) - 1):
            lower_threshold = sorted_thresholds[i]
            upper_threshold = sorted_thresholds[i + 1]
            if lower_threshold[1]['value'] <= current_temp <= upper_threshold[1]['value']:
                # print(f"Temperature falls within range: {lower_threshold[1]['value']} - {upper_threshold[1]['value']}")
                # Calculate the percentile within this range
                range_min = lower_threshold[1]['value']
                range_max = upper_threshold[1]['value']
                percentile = (current_temp - range_min) / \
                    (range_max - range_min)
                # print(f"Percentile: {percentile:.2f}")

                # Interpolate the color intensity based on the percentile
                base_color = lower_threshold[1]['color']
                # print(f"Base color: {base_color}")
                intense_color = get_intense_color(base_color, percentile)
                # print(f"Interpolated color: {intense_color}")
                return intense_color

        # If temperature is outside the defined range, return the closest color
        if current_temp < sorted_thresholds[0][1]['value']:
            # print(f"Temperature is below the lowest threshold: {sorted_thresholds[0][1]['value']}")
            return sorted_thresholds[0][1]['color']
        else:
            # print(f"Temperature is above the highest threshold: {sorted_thresholds[-1][1]['value']}")
            return sorted_thresholds[-1][1]['color']
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_intense_color(base_color: str, intensity: float) -> str:
    """
    Adjust the intensity of a base color based on a percentile value.
    :param base_color: The base hex color code.
    :param intensity: A value between 0 and 1 representing the percentile.
    :return: A more intense version of the base color.
    """
    try:
        # Convert hex color to RGB
        r = int(base_color[1:3], 16)
        g = int(base_color[3:5], 16)
        b = int(base_color[5:7], 16)

        # Increase intensity for green, decrease for red and blue (for hotter colors)
        # reduce red component
        r = max(0, r - int(MAX_COLOR_INTENSITY * intensity * 0.75))
        g = min(MAX_COLOR_INTENSITY, g + int(MAX_COLOR_INTENSITY *
                intensity * 1.25))  # increase green component
        b = max(0, b - int(MAX_COLOR_INTENSITY * intensity))

        # Convert back to hex
        return f'#{r:02x}{g:02x}{b:02x}'
    except Exception as e:
        print(f"An error occurred while adjusting color intensity: {e}")
        return base_color

# The interpolate_hex_color function is not used in the current implementation.
# If not needed, consider removing it to keep the code clean.
