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
import pymysql
from dotenv import load_dotenv
import os
from urllib.parse import urlparse

load_dotenv() # Load environment variables from .env 

# Parse the database URL
db_url = os.getenv('DATABASE_URL')
parsed_url = urlparse(db_url)

connection = pymysql.connect( # Connect to MySQL database
    host=parsed_url.hostname,
    user=parsed_url.username,
    password=parsed_url.password,
    database=parsed_url.path[1:],  
    port=parsed_url.port
)

i2c = busio.I2C(board.SCL, board.SDA) # I2C interface that reads from GPIO pins SCL and SDA
ads = ADS.ADS1115(i2c) # ADS1115 object that converts the analog signal to digital
channel_3 = AnalogIn(ads, ADS.P3) # Read from analog input channel on Pin 3

def read_turbidity(analog_voltage): # Uses analog voltage to find turbidity
    turbidity = (analog_voltage / 5.0) * 4550 # convert voltage to turbidity
    return turbidity

def insert_data_into_db(sensor_type, value): # Function to insert data into the database
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO sensor_data (sensor_type, value, timestamp) VALUES (%s, %s, NOW())"
            cursor.execute(sql, (sensor_type, value)) # Execute the query
            connection.commit() # commit to the database
    except Exception as e:
        print(f"Error inserting data into database: {e}")

try:
    while True: # Main loop to read and store the turbidity value
        voltage = channel_3.voltage # read voltage from the sensor
        turbidity = read_turbidity(voltage) # read turbidity value
        turbidity = round(turbidity, 2) # round to 2 decimal places

        print(f"Turbidity: {turbidity:.2f} NTU")  
        insert_data_into_db('turbidity_sensor', turbidity) # insert turbidity data indatabase
        
        time.sleep(2)  
finally:
    connection.close() # Close connection when done
