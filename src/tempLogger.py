#!/usr/bin/python

import platform
import time
from datetime import datetime


def isLinux():
    return platform.system() == "Linux"


def debugSensorData():
    return -1, -1


class Settings:
    def __init__(self):
        if (isLinux()):
            # Production settings
            from .tempUtil import getCurrentTempAndHummidity
            self.getSensorData = getCurrentTempAndHummidity
            self.readingPeriod = 60  # Seconds
            self.FILE_PATH = "/home/pi/code/tempReadings.log"
        else:
            # Debug settings
            self.getSensorData = debugSensorData
            self.readingPeriod = 5  # Seconds
            self.FILE_PATH = "./tempReadings.log"


def start():
    settings = Settings()
    oldtime = time.time()
    while True:
        if time.time() - oldtime > settings.readingPeriod:
            temp, humidity = settings.getSensorData()
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            if humidity is not None and temp is not None:
                with open(settings.FILE_PATH, "a") as myfile:
                    myfile.write('{0},{1:0.0f},{2:0.0f}\n'.format(dt_string, temp, humidity))
            else:
                myfile.write('Failed to get reading. Try again!\n')
            oldtime = time.time()


start()
