"""
Author: Victor Vu
File: temp_sensor.py
Description: Reads the temperature from a DS18B20 sensor and outputs it in Fahrenheit

Copyright (C) 2024 Victor V. Vu and Jordan Morris
License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
"""
import time
from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor() # Create a sensor object

while True: # Loop to read the temperature
    try: 
        celsius = sensor.get_temperature() # get the temperature in Celsius
        fahrenheit = celsius * 9/5 + 32 # convert to Fahrenheit
        print(f"Temperature: {fahrenheit:.2f} °F") 

    except Exception as e: # catch any errors
        print(f"Error reading temperature: {e}")

    time.sleep(2) # wait 2 seconds before reading again