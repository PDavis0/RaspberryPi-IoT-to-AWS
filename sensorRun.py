#Simple Adafruit BNO055 sensor reading example.  Will print the orientation
# and calibration data every second.
#
# Copyright (c) 2015 Adafruit Industries
# Author: Tony DiCola

import logging
import sys
import time
import datetime
import boto3
from botocore.client import Config

from Adafruit_BNO055 import BNO055

# Create and configure the BNO sensor connection.  Make sure only ONE of the
# below 'bno = ...' lines is uncommented:
# Raspberry Pi configuration with serial UART and RST connected to GPIO 18:
bno = BNO055.BNO055(serial_port='/dev/ttyS0', rst=18)

# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Write to file
stringTime = time.strftime('%y%m%d-%H%M%S')
fileName ='z'+stringTime+'.csv'

print fileName
with open(fileName,'w') as data:

    # Print system status and self test result.
    status, self_test, error = bno.get_system_status() 
    print('System status: {0}'.format(status)) 
    print('Self_test result (0x0F is normal): 0x{0:02X}'.format(self_test))
    # Print out an error if system status is in error mode.
    if status == 0x01:
        print('System error: {0}'.format(error))
        print('See datasheet section 4.3.59 for the meaning.')
        while status == 0x01:
            status,self_test,error =bno.get_system_status()
            print('System error: {0}'.format(status))
            setup()

    # Print BNO055 software revision and other diagnostic data.
    sw, bl, accel, mag, gyro = bno.get_revision()
    print('Software version:   {0}'.format(sw))
    print('Bootloader version: {0}'.format(bl))
    print('Accelerometer ID:   0x{0:02X}'.format(accel))
    print('Magnetometer ID:    0x{0:02X}'.format(mag))
    print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

    # Set up columns for human reading of csv
    #data.write('Number Collected,Heading,Roll,Pitch,Sys,GyroCal,AccelCal,MagCal,TimeStamp, Magn X,Magn Y,Magn Z,Gyro X,Gyro Y,Gyro Z,Acc X,Acc Y,Acc Z,Lin Acc X,Lin Acc Y,Lin Acc Z,Gravity X,Gravity Y,Gravity Z\n')
    data.write('numberRead,X acc,Y acc,Z acc,time stamp\n')
    DATA_POINT_READING_THRESHOLD = 1000
    numCollected = 0
    print(datetime.datetime.utcnow())
    print('Reading BNO055 data, press Ctrl-C to quit...')
    while (numCollected-1 < DATA_POINT_READING_THRESHOLD):
        # Read the Euler angles for heading, roll, pitch (all in degrees).
       # heading, roll, pitch = bno.read_euler()
        # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
       # sys, gyro, accel, mag = bno.get_calibration_status()
        # Print everything out.

        #data.write('{0},{1:0.2F},{2:0.2F},{3:0.2F},{4},{5},{6},{7},{8}'.format(
         #   numCollected,heading, roll, pitch, sys, gyro, accel, mag,datetime.datetime.utcnow()))

        numCollected += 1
        # Other values you can optionally read:
        # Orientation as a quaternion:
        #x,y,z,w = bno.read_quaterion()
        #data.write('{0:0.2F},{1:0.2F},{2:0.2F},{3:0.2F}'.format(x,y,z,w))
        # Sensor temperature in degrees Celsius:
        #temp_c = bno.read_temp()
        #temp_f = temp_c * 1.8 + 32
        #data.write('{0:0.2F},'.format(temp_c))
        # Magnetometer data (in micro-Teslas):
       # x,y,z = bno.read_magnetometer()
       # data.write('{0:0.2F},{1:0.2F},{2:0.2F},'.format(x,y,z))
        # Gyroscope data (in degrees per second):
       # x,y,z = bno.read_gyroscope()
       # data.write('{0:0.2F},{1:0.2F},{2:0.2F},'.format(x,y,z))
        # Accelerometer data (in meters per second squared):
        x,y,z = bno.read_accelerometer()
        data.write('{0},{1:0.3F},{2:0.3F},{3:0.3F},'.format(numCollected,x,y,z))
        data.write(str(datetime.datetime.utcnow())+',')
        # Linear acceleration data (i.e. acceleration from movement, not gravity--
        # returned in meters per second squared):
        #x,y,z = bno.read_linear_acceleration()
        #data.write('{0:0.2F},{1:0.2F},{2:0.2F},'.format(x,y,z))
        # Gravity acceleration data (i.e. acceleration just from gravity--returned
        # in meters per second squared):
       # x,y,z = bno.read_gravity()
       # data.write('{0:0.2F},{1:0.2F},{2:0.2F},'.format(x,y,z))
        data.write('\n')

ACCESS_KEY_ID = 'XXXXXXXXXXX'
ACCESS_SECRET_KEY = 'XXXXXXXXXX'
BUCKET_NAME = 'XXXXXXXXX'
data = open(fileName, 'rb')

s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)
s3.Bucket(BUCKET_NAME).put_object(Key='sensorData/'+fileName, Body=data)

print ("Done with file: "+fileName)

def setup():
    # Create and configure the BNO sensor connection.  Make sure only ONE of the
    #below 'bno = ...' lines is uncommented:
    # Raspberry Pi configuration with serial UART and RST connected to GPIO 18:
    bno = BNO055.BNO055(serial_port='/dev/ttyS0', rst=18)


    # Enable verbose debug logging if -v is passed as a parameter.
    if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
        logging.basicConfig(level=logging.DEBUG)

    # Initialize the BNO055 and stop if something went wrong.
    if not bno.begin():
        raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')
'''
#csvPath = '/home/pi/Adafruit_Python_BNO055/scripts/sensorData.csv'
#csvExe = r''
#subprocess.Popen("%s %s" % (csvExe,csvPath))
'''