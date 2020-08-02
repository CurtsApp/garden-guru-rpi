#!/usr/bin/python

import Adafruit_DHT
import time
from datetime import datetime

sensor = Adafruit_DHT.DHT11
pin = 4


# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).


# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
oldtime = time.time()

while True:
    if time.time() - oldtime > 60:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if humidity is not None and temperature is not None:
            with open("/home/pi/code/test.txt", "a") as myfile:
                myfile.write('{0},{1:0.0f},{2:0.0f}\n'.format(dt_string,temperature, humidity))
        else:
            myfile.write('Failed to get reading. Try again!\n')
        oldtime = time.time()

