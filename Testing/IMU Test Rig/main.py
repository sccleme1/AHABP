from imu import MPU6050
from time import sleep
from machine import Pin, I2C

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)
led = Pin(25, Pin.OUT)

imu.accel_range = 3

file=open("imu_data.csv", "w")
file.write("t [100ms], |a| [m/s^2], ax [m/s^2], ay [m/s^2], az [m/s^2]\n")

time = 5
t = 0
sleep(5)
led.toggle() # on 1
sleep(0.5)
led.toggle() # off
sleep(0.5)
led.toggle() # on 2
sleep(0.5)
led.toggle() # off
sleep(0.5)
led.toggle() # on 3
sleep(0.5)

# start drop test recording

while (t <= time):
    ax=round(imu.accel.x,2)
    ay=round(imu.accel.y,2)
    az=round(imu.accel.z,2)
    gx=round(imu.gyro.x)
    gy=round(imu.gyro.y)
    gz=round(imu.gyro.z)
    tem=round(imu.temperature,2)
    a = round((ax**2 + ay**2 + az**2)**0.5, 2)
    #print("ax",ax,"\t","ay",ay,"\t","az",az,"\t","gx",gx,"\t","gy",gy,"\t","gz",gz,"\t","Temperature",tem,"        ",end="\r")
    file.write(str(t)+","+str(a)+","+str(ax)+","+str(ay)+","+str(az)+"\n")
    #print("a =", a, "m/s^2", end="\r")
    sleep(0.005)
    t += 0.005
    if t >= time:
        file.close()
        led.toggle() # off