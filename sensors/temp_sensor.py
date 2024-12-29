"""
Author: Victor Vu
File: temp_sensor.py
Description: Reads the temperature from a DS18B20 sensor and outputs it in Fahrenheit

Copyright (C) 2024 Victor V. Vu and Jordan Morris
License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
"""
from w1thermsensor import W1ThermSensor
from connect_timer import *

connection = create_connection() # Create a connection to the database
sensor = W1ThermSensor() # Create a sensor object

def insert_data_into_db(sensor_type, value): # Function to insert data into the database
    try:
        with connection.cursor() as cursor: # cursor object
            sql = "INSERT INTO sensor_data (sensor_type, value, timestamp) VALUES (%s, %s, NOW())" # sql query
            cursor.execute(sql, (sensor_type, value)) # execute the query
            connection.commit() # commit the changes

    except Exception as e: # catch any errors
        print(f"Error inserting data into database: {e}")

try: # Main loop to read and store the temperature value
    while True:
        try:
            celsius = sensor.get_temperature() # get the temperature in Celsius
            fahrenheit = celsius * 9 / 5 + 32 # convert to Fahrenheit
            print(f"Temperature: {fahrenheit} °F")
            insert_data_into_db('temperature', fahrenheit) # insert the temps in database

        except Exception as e: # catch any errors
            print(f"Error reading temperature: {e}")

        control_timer() # wait for a specified time
finally:
    connection.close() # close connection when done
