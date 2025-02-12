# Author: Victor Vu
# File: tds_sensor.py
# Description: Script for reading TDS (Total Dissolved Solids) value from the TDS sensor
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from connect_timer import create_connection, control_timer

connection = create_connection()  # Create a connection to the database
i2c = busio.I2C( # I2C interface that reads from GPIO pins SCL and SDA
    board.SCL, board.SDA
)  
ads = ADS.ADS1115(i2c)  # ADS1115 object that converts the analog signal to digital
channel_1 = AnalogIn(ads, ADS.P1)  # Read from analog input channel on Pin 1

V_REFERENCE = 2.3  # Reference voltage for the sensor for formula
TDS_FACTOR = 0.5  # Factor to convert voltage to TDS value (ppm)


def read_tds():  # Function to read the TDS value
    voltage = channel_1.voltage  # read voltage from sensor
    tds_value = (voltage / V_REFERENCE) * TDS_FACTOR * 1000  # convert voltage to TDS
    return tds_value


def insert_data_into_db(
    sensor_type, value
):  # Function to insert data into the database
    try:
        with connection.cursor() as cursor:  # Cursor object
            sql = "INSERT INTO sensor_data (sensor_type, value, timestamp) VALUES (%s, %s, NOW())"  # the SQL query to insert data
            cursor.execute(sql, (sensor_type, value))  # execute the query
            connection.commit()  # commit the changes to database

    except Exception as e:  # Catch any errors
        print(f"Error inserting data into database: {e}")


# Main loop to read and store the TDS value
while True:
    tds = read_tds()
    print(f"TDS: {tds} ppm")
    insert_data_into_db("total dissolved solids", tds)  # insert the TDS data
    control_timer()  # wait for a speficied time
