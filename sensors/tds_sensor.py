"""
Author: Victor Vu
File: tds_sensor.py
Description: This script reads the TDS (Total Dissolved Solids) value from the TDS sensor

Copyright (C) 2024 Victor V. Vu and Jordan Morris
License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
"""
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA) # I2C interface that reads from GPIO pins SCL and SDA
ads = ADS.ADS1115(i2c) # ADS1115 object that converts the analog signal to digital
channel_1 = AnalogIn(ads, ADS.P1) # Read from analog input channel on Pin 1

V_REFERENCE = 2.3 # Reference voltage for the sensor for formula
TDS_FACTOR = 0.5 # Factor to convert voltage to TDS value (ppm)

def read_tds(): # Function to read the TDS value
    voltage = channel_1.voltage # read the voltage from the sensor
    tds_value = (voltage / V_REFERENCE) * TDS_FACTOR * 1000 # convert voltage to TDS value
    return tds_value

while True: # Loop to read the TDS value
    tds = read_tds() # start reading 
    print(f'TDS: {tds:.2f} ppm')
    time.sleep(2) 
