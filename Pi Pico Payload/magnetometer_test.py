# Example for Pycom device.
# Connections:
# xxPy | QMC5883
# -----|-------
# P9   |  SDA
# P10  |  SCL
#
from machine import I2C, Pin
from QMC5883L import *
from time import sleep
from math import atan2, degrees

i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=100000)

qmc5883 = QMC5883L(i2c)


while True:
    x, y, z, temp = qmc5883.read_scaled()
    heading = degrees(atan2(x, y))
    print("x:\t", round(x, 2), " y:\t", round(y, 2), " z:\t", round(z, 2), " heading:", round(heading, 2), end="\r")
    sleep(0.1)