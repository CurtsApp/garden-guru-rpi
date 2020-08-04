#!/usr/bin/python

import platform
import time
from datetime import datetime


def isLinux():
    return platform.system() == "Linux"

def debugSensorData():
    return -1, -1

def start():
    # Debug settings
    getSensorData = debugSensorData
    readingPeriod = 5 #  Seconds
    FILE_PATH = "tempReadings.log"
    if isLinux():
        # Production settings
        from .tempUtil import getCurrentTempAndHummidity
        getSensorData = getCurrentTempAndHummidity
        readingPeriod = 60 # Seconds
        FILE_PATH = "/home/pi/code/tempReadings.log"

    oldtime = time.time()
    while True:
        if time.time() - oldtime > readingPeriod:
            temp, humidity = getSensorData()
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            if humidity is not None and temp is not None:
                with open(FILE_PATH, "a") as myfile:
                    myfile.write('{0},{1:0.0f},{2:0.0f}\n'.format(dt_string, temp, humidity))
            else:
                myfile.write('Failed to get reading. Try again!\n')
            oldtime = time.time()


start()
