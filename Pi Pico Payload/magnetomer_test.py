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

file = open("mag_data.csv", "w")
file.write("x,y,z,heading1,heading2,heading3\n")

time = 0
while True:
    x, y, z, temp = qmc5883.read_scaled()
    heading = degrees(atan2(x, y))
    heading2 = degrees(atan2(y, z))
    heading3 = degrees(atan2(z, x))
    print("x:\t", round(x, 2), " y:\t", round(y, 2), " z:\t", round(z, 2), " heading:", round(heading, 2), " heading2:", round(heading2, 2), " heading3:", round(heading3, 2), end="\r")
    file.write(f"{x},{y},{z},{heading},{heading2},{heading3},{time}\n")
    sleep(0.1)
    time += 0.1
    if time >= 30:
        break
    
print("program ended")
file.close()