#!/usr/bin/python

import platform
import time
from datetime import datetime
from pathlib import Path


def isLinux():
    return platform.system() == "Linux"


def debugSensorData():
    return -1, -1


class Settings:
    def __init__(self):
        if (isLinux()):
            # Production settings
            from tempUtil import getCurrentTempAndHummidity
            self.getSensorData = getCurrentTempAndHummidity
            self.readingPeriod = 60  # Seconds
            self.LOG_DIR_PATH = "/home/pi/code/log/temp"
        else:
            # Debug settings
            self.getSensorData = debugSensorData
            self.readingPeriod = 5  # Seconds
            self.LOG_DIR_PATH = "./log/temp"


def getFilePath(date, directoryPath):
    return '{0}/{1}.log'.format(directoryPath, date)


def start():
    settings = Settings()
    Path(settings.LOG_DIR_PATH).mkdir(parents=True, exist_ok=True)
    oldtime = time.time()
    while True:
        if time.time() - oldtime > settings.readingPeriod:
            humidity, temp = settings.getSensorData()
            dt_string = datetime.now().strftime("%d-%m-%Y,%H:%M:%S")
            dt = dt_string.split(',')
            if humidity is not None and temp is not None:
                with open(getFilePath(dt[0], settings.LOG_DIR_PATH), "a") as myfile:
                    myfile.write('{0},{1:0.0f},{2:0.0f}\n'.format(int(time.time()), temp, humidity))
            else:
                myfile.write('Failed to get reading. Try again!\n')
            oldtime = time.time()


start()
