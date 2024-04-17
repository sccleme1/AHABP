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
    
    ##### CALIBRATION #####   
    x /= 0.9565
    y /= 1.0578
    z /= 0.9873
    
    x -= 0.015
    y += 0.022
    z -= 0.037
    
    heading = degrees(atan2(x, y))
    heading2 = degrees(atan2(y, z))
    heading3 = degrees(atan2(z, x))
    
    if heading < 0:
        heading += 360
    if heading2 < 0:
        heading2 += 360
    if heading3 < 0:
        heading3 += 360
        
    if heading > 360:
        heading -= 360
    if heading2 > 360:
        heading2 -= 360
    if heading3 > 360:
        heading3 -= 360
    print("x:\t", round(x, 2), " y:\t", round(y, 2), " z:\t", round(z, 2), " heading:", round(heading, 2), " heading2:", round(heading2, 2), " heading3:", round(heading3, 2), end="\r")
    file.write(f"{x},{y},{z},{heading},{heading2},{heading3},{time}\n")
    # Ts = 0.01, fs = 100 Hz
    sleep(0.01)
    time += 0.01
    if time >= 20:
        break
    
print("program ended")
file.close()