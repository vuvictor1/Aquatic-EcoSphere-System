"""
Author: Victor Vu
File: temp_sensor.py
Description: Reads the temperature from a DS18B20 sensor and outputs it in Fahrenheit

Copyright (C) 2024 Victor V. Vu and Jordan Morris
License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
"""
import time
from w1thermsensor import W1ThermSensor
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

sensor = W1ThermSensor() # Create a sensor object

def insert_data_into_db(sensor_type, value): # Function to insert data into the database
    try:
        with connection.cursor() as cursor: # cursor object
            sql = "INSERT INTO sensor_data (sensor_type, value, timestamp) VALUES (%s, %s, NOW())" # SQL query
            cursor.execute(sql, (sensor_type, value)) # execute the query
            connection.commit() # commit the changes

    except Exception as e: # catch any errors
        print(f"Error inserting data into database: {e}")

try: # Main loop to read and store the temperature value
    while True:
        try:
            celsius = sensor.get_temperature() # get the temperature in Celsius
            fahrenheit = celsius * 9 / 5 + 32 # convert to Fahrenheit
            fahrenheit = round(fahrenheit, 2)  # round to 2 decimal places
            print(f"Temperature: {fahrenheit:.2f} °F")
            insert_data_into_db('temperature_sensor', fahrenheit) # insert the temps in database

        except Exception as e: # catch any errors
            print(f"Error reading temperature: {e}")

        time.sleep(2) # wait 2secs before reading again
finally:
    connection.close() # close connection when done
