import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 4


def getCurrentTempAndHummidity():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return humidity, temperature
