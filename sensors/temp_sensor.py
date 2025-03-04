# Author: Victor Vu
# File: temp_sensor.py
# Description: Reads temp from a DS18B20 sensor and outpu in Fahrenheit
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from w1thermsensor import W1ThermSensor
from connect_timer import control_timer, create_connection

connection = create_connection()  # Create a connection to the database
sensor = W1ThermSensor()  # Create a sensor object


def insert_data_into_db(  # Function to insert data into the database
    sensor_type, value
):
    try:
        with connection.cursor() as cursor:  # cursor object
            sql = "INSERT INTO sensor_data (sensor_type, value, timestamp) VALUES (%s, %s, NOW())"  # sql query
            cursor.execute(sql, (sensor_type, value))  # execute the query
            connection.commit()  # commit the changes

    except Exception as e:  # Catch any errors
        print(f"Error inserting data into database: {e}")
        reconnect_to_db()  # attempt to reconnect to the database


def reconnect_to_db():  # Function to reconnect to the database
    global connection
    try:
        connection.close()  # close the existing connection
    except Exception as e:
        print(f"Error closing the connection: {e}")
    connection = create_connection()  # recreate the connection


# Main loop to read and store the temperature value
while True:
    celsius = sensor.get_temperature()  # get the temperature in Celsius
    fahrenheit = celsius * 9 / 5 + 32  # convert to Fahrenheit
    print(f"Temperature: {fahrenheit} °F")
    insert_data_into_db("temperature", fahrenheit)  # insert the temps in database
    control_timer()  # wait for a specified time
