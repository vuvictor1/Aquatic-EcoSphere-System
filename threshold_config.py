# Authors: Jordan Morris and Victor Vu
# File: threshold_config.py
# Description: Handles threshold and color configuration for sensor data.
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html

DEFAULT_TEMPERATURE_THRESHOLDS = { # Default thresholds/colors for temp
    'min': {'value': 50, 'color': '#ADD8E6'}, # light blue
    'low': {'value': 60, 'color': '#90EE90'}, # light green
    'mid': {'value': 80, 'color': '#FFA07A'}, # light red
    'max': {'value': 90, 'color': '#FF0000'}  # intense red
}

DEFAULT_TDS_THRESHOLDS = { # Default thresholds/colors for TDS
    'min': {'value': 0, 'color': '#ADD8E6'},   # light blue
    'low': {'value': 500, 'color': '#90EE90'}, # light green
    'mid': {'value': 1000, 'color': '#FFA07A'},# light red
    'max': {'value': 2000, 'color': '#FF0000'} # intense red
}

DEFAULT_TURBIDITY_THRESHOLDS = { # Default thresholds/colors for turbidity
    'min': {'value': 0, 'color': '#ADD8E6'}, # light blue
    'low': {'value': 5, 'color': '#90EE90'}, # light green
    'mid': {'value': 50, 'color': '#FFA07A'},# light red
    'max': {'value': 100, 'color': '#FF0000'}# intense red
}

# User-defined thresholds (initially set to default)
temperature_thresholds = DEFAULT_TEMPERATURE_THRESHOLDS.copy()
tds_thresholds = DEFAULT_TDS_THRESHOLDS.copy()
turbidity_thresholds = DEFAULT_TURBIDITY_THRESHOLDS.copy()
MAX_COLOR_INTENSITY = 255 # max value for RGB color intensity

def set_temperature_thresholds(new_thresholds: dict) -> None: # Set temperature thresholds
    # param new_thresholds: A dictionary containing new thresholds and colors.
    global temperature_thresholds # use the global variable
    temperature_thresholds = new_thresholds # update the thresholds

def get_temperature_thresholds() -> dict: # Get temperature thresholds
    return temperature_thresholds # dictionary of thresholds

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
        sorted_thresholds = sorted(thresholds.items(), key=lambda x: x[1]['value'])
        # print(f"Sorted thresholds: {sorted_thresholds}")

        for i in range(len(sorted_thresholds) - 1): # Find the range current_temp falls into
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

                base_color = lower_threshold[1]['color'] # interpolate between these two colors
                # print(f"Base color: {base_color}")
                intense_color = get_intense_color(base_color, percentile)
                # print(f"Interpolated color: {intense_color}")
                return intense_color

        if current_temp < sorted_thresholds[0][1]['value']: # If temp is below the lowest threshold
            # print(f"Temperature is below the lowest threshold: {sorted_thresholds[0][1]['value']}")
            return sorted_thresholds[0][1]['color']
        else:
            # print(f"Temperature is above the highest threshold: {sorted_thresholds[-1][1]['value']}")
            return sorted_thresholds[-1][1]['color']

    except Exception as e: # Handle exceptions
        print(f"An error occurred: {e}")
        return None

def get_intense_color(base_color: str, intensity: float) -> str: # Adjust color intensity based on percentile
    """
    :param base_color: The base hex color code.
    :param intensity: A value between 0 and 1 representing the percentile.
    :return: A more intense version of the base color.
    """
    try: # Convert hex color to RGB
        r = int(base_color[1:3], 16)
        g = int(base_color[3:5], 16)
        b = int(base_color[5:7], 16)

        # Increase intensity for green, decrease for red and blue (for hotter colors)
        r = max(0, r - int(MAX_COLOR_INTENSITY * intensity * 0.75)) # reduce red component
        g = min(MAX_COLOR_INTENSITY, g + int(MAX_COLOR_INTENSITY *
                intensity * 1.25)) # increase green component
        b = max(0, b - int(MAX_COLOR_INTENSITY * intensity))

        return f'#{r:02x}{g:02x}{b:02x}' # convert back to hex
        
    except Exception as e:
        print(f"An error occurred while adjusting color intensity: {e}")
        return base_color

# The interpolate_hex_color function is not used in the current implementation.
# If not needed, consider removing it to keep the code clean.