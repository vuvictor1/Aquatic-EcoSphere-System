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
import pymysql
from dotenv import load_dotenv
import os
from urllib.parse import urlparse

load_dotenv() # Load environment variables from .env file

# Parse the database URL
db_url = os.getenv('DATABASE_URL')
parsed_url = urlparse(db_url)

connection = pymysql.connect( # Connect to MySQL
    host=parsed_url.hostname,
    user=parsed_url.username,
    password=parsed_url.password,
    database=parsed_url.path[1:],  
    port=parsed_url.port
)

i2c = busio.I2C(board.SCL, board.SDA) # I2C interface that reads from GPIO pins SCL and SDA
ads = ADS.ADS1115(i2c) # ADS1115 object that converts the analog signal to digital
channel_1 = AnalogIn(ads, ADS.P1) # Read from analog input channel on Pin 1

V_REFERENCE = 2.3 # Reference voltage for the sensor for formula
TDS_FACTOR = 0.5 # Factor to convert voltage to TDS value (ppm)

def read_tds(): # Function to read the TDS value
    voltage = channel_1.voltage # read voltage from sensor
    tds_value = (voltage / V_REFERENCE) * TDS_FACTOR * 1000 # convert voltage to TDS 
    return tds_value

def insert_data_into_db(sensor_type, value): # Function to insert data into the database
    try: 
        with connection.cursor() as cursor: # Cursor object 
            sql = "INSERT INTO sensor_data (sensor_type, value, timestamp) VALUES (%s, %s, NOW())" # the SQL query to insert data
            cursor.execute(sql, (sensor_type, value)) # execute the query
            connection.commit() # commit the changes to database

    except Exception as e: # catch any errors
        print(f"Error inserting data into database: {e}")

try: # Main loop to read and store the TDS value
    while True: 
        tds = read_tds() 
        print(f'TDS: {tds} ppm') 
        insert_data_into_db('total dissolved solids', tds) # insert the TDS data
        time.sleep(600) # wait 10min before reading again
finally:
    connection.close() # close the connection when done
