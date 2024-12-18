"""
Author: Victor Vu
File: turb_sensor.py
Description: This script reads the analog voltage from a turbidity sensor connected to an ADS1115

Copyright (C) 2024 Victor V. Vu and Jordan Morris
License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
"""
import time
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15.ads1115 as ADS

i2c = busio.I2C(board.SCL, board.SDA) # I2C interface that reads from GPIO pins SCL and SDA
ads = ADS.ADS1115(i2c) # ADS1115 object that converts the analog signal to digital
channel_3 = AnalogIn(ads, ADS.P3) # Read from analog input channel on Pin 3

def read_turbidity(analog_voltage): # Uses analog voltage to find turbidity
    turbidity = (analog_voltage / 5.0) * 4550 # convert voltage to turbidity
    return turbidity

while True: # Loop to read the turbidity value
    voltage = channel_3.voltage # read the voltage from the sensor
    turbidity = read_turbidity(voltage) # read the turbidity value
    
    print(f"Turbidity: {turbidity:.2f} NTU")
    
    time.sleep(2)
