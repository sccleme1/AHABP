# Scott Clemens
# 5 April 2024
# Autonomous High Altitude Balloon Payload
#   This program is meant to run on a Raspberry Pi Pico microcontroller
#   to control the real-time operations of the payload given IMU, magnetometer
#   and serial data from a Raspberry Pi 4.
from imu import MPU6050
from time import sleep
from machine import Pin, UART, I2C, Timer, PWM
import utime, time
from QMC5883L import *
from math import atan2, degrees
from servo import Servo

# PID gains
kp = 20
ki = 0
kd = 0
integral = 0
last_error = 0

# global setpoints
smooth_heading = 0
setpoint = 0
output = 0
# minimum disarm value for motors
frequency = 100     # Hz
disarm = 3277
PWM_base = 8000
# MIN 7000
# MAX 9000

# timer for PID control
PID_timer = Timer(-1)

# MPU6050 inertial measurement unit (IMU)
IMU_i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
imu = MPU6050(IMU_i2c)
imu.accel_range = 3

# QMC5883L magnetometer (compass)
MAG_i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=100000)
qmc5883 = QMC5883L(MAG_i2c)

# GPS receiver
gpsModule = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
print("GPS is on", gpsModule)

buff = bytearray(255)

latitude = ""
longitude = ""
GPStime = ""
nmea_data = ""

# PWM control for ESCs
pwm_motor_top = PWM(Pin(15)) #
pwm_motor_bottom = PWM(Pin(14)) #
pwm_motor_top.freq(frequency)
pwm_motor_bottom.freq(frequency)
sleep(1)
pwm_motor_top.duty_u16(disarm) # disarm value on top motor
pwm_motor_bottom.duty_u16(disarm) # disarm value on bottom motor

# PWM control for camera servo on GP13
camera_servo = Servo(13)
# UP = 0
# Horizontal = 80
# DOWN = 135
try:
    file=open(f"start_log.txt", "w")
    file.write(f"Start log begin\n")
    file.write(f"kp ={kp}, ki ={ki}, kd ={kd}\n")
    file.write(f"GPS is on {gpsModule}\n")
    file.write(f"Top motor on GP15\n")
    file.write(f"Bottom motor on GP14\n")
    file.write(f"ESC frequency {frequency} Hz\n")
    file.write(f"Disarm: {disarm}\n")
    file.write(f"PWM Base: {PWM_base}\n")
    file.write(f"Servo motor on GP13\n\n")
    file.write(f"Starting GPS, unused NMEA sentences:\n")
except:
    pass


def servo_Map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def servo_Angle(angle):
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    camera_servo.goto(round(servo_Map(angle,0,180,0,1024))) # Convert range value to angle value
    #print("angle", angle, "           ", end="\r")


def PID(t):
    global kp, ki, kd, integral, last_error, smooth_heading, setpoint, output
    dt = 0.1 # s
    
    error = setpoint - smooth_heading
    integral += error*dt
    derivative = (error - last_error)/dt
    last_error = error
    raw_output = kp*error + ki*integral + kd*derivative
    # TODO: determine left/right directional spin
    #       set top_output and bottom_output
    #       limit outputs max and min values
    output = max(0, min(raw_output, 1000))
    #print("setpoint:", setpoint, "heading:", round(heading, 2), "error", round(error, 2), "PID output:", output, "integral", integral, "          ", end="\r")
    pwm_motor_top.duty_u16(PWM_base + output)
    pwm_motor_bottom.duty_u16(PWM_base - output)


def convertToDegree(RawDegrees):

    try:
        RawAsFloat = float(RawDegrees)
        firstdigits = int(RawAsFloat/100) 
        nexttwodigits = RawAsFloat - float(firstdigits*100) 
        
        Converted = float(firstdigits + nexttwodigits/60.0)
        Converted = round(Converted, 6) 
        return Converted
    except:
        pass


def getGPS(gpsModule, timeout=1):
    global latitude, longitude, GPStime, nmea_data
    
    gpsModule.readline()
    buff = str(gpsModule.readline())
    print(buff)
    parts = buff.split(',')
    timeout_ = timeout + time.time()

    while True:
        if (parts[0] == "b'$GPGGA"):
            # eg2. $--GGA,hhmmss.ss,llll.ll,a,yyyyy.yy,a,x,xx,x.x,x.x,M,x.x,M,x.x,xxxx 
            # eg3. $GPGGA,hhmmss.ss,llll.ll,a,yyyyy.yy,a,x,xx,x.x,x.x,M,x.x,M,x.x,xxxx*hh
            if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6]):
                
                latitude = convertToDegree(parts[2])
                longitude = convertToDegree(parts[4])
                
                if (parts[3] == 'S'):
                    latitude = -latitude
                if (parts[5] == 'W'):
                    longitude = -longitude
                GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
        
        if (parts[0] == "b'$GPGLL"):
            # eg1. $GPGLL,3751.65,S,14507.36,E*77
            # eg2. $GPGLL,4916.45,N,12311.12,W,225444,A
            if(parts[1] and parts[2] and parts[3] and parts[4]):
                
                latitude = convertToDegree(parts[1])
                longitude = convertToDegree(parts[3])

                if (parts[2] == 'S'):
                    latitude = -latitude
                if (parts[4] == 'W'):
                    longitude = -longitude                
        
        if (time.time() > timeout_):
            break
        
        return buff

##### START MAIN PROGRAM #####
sleep(10) # wait for Pi to boot up
# set camera servo to horizontal and start uart serial
servo_Angle(80)
uart = machine.UART(0, 115200)
uart.init(bits=8, parity=None, stop=1)
#print(uart)
b = None
msg = ""

##### START BY FINDING GPS LOCATION #####
print("Acquiring GPS lock, unused NMEA sentences:")
uart.write(",--------------------\n\r")
uart.write("Serial from Pico initiated, acquiring GPS lock...\n\r")
new_setpoint = None
start_time = time.time()

while True:
    current_time = time.time()
    elapsed_time = current_time - start_time
    buff = getGPS(gpsModule, 3)
    try:
        file.write(f"t = {elapsed_time} ")
        file.write(buff)
        file.write("\n")
    except:
        pass
    #uart.write(buff)
    sleep(1)
    if (latitude != "") and (latitude != None):
        if (longitude != "") and (longitude != None):
            break

try:
    file.write(f"Latitude: {latitude} Longitude: {longitude}\n")
    file.write(f"Start log end")
    file.close()
except:
    pass

print("Latitude: ", latitude, " Longitude: ", longitude)
##### NOW SEND LOCATION TO PI FOR EPHEM CALCULATION OF SETPOINT #####
# Serial communication with Raspberry Pi
while True:
    uart.write(f"latitude,{latitude},longitude,{longitude},end\n\r")
    if uart.any():
        print("GPS lat/long sent to Pi 4")
        break
#uart.txdone()

##### START PID CONTROL #####
PID_timer.init(mode=Timer.PERIODIC, freq=10, callback=PID)
imu.accel.calibrate

##### START WHEELS AT BASE SPEED #####
pwm_motor_top.duty_u16(PWM_base)
pwm_motor_bottom.duty_u16(PWM_base)
try:
    log_file=open("run_log.csv", "w")
    log_file.write(f"Time,Hx,Hy,Hz,Ax,Ay,Az,Heading,PID_Output,Integral,Setpoint\n")
except:
    pass

start_time = time.time()

# for averaging the heading to smooth it easier
prev_heading_1 = 0
prev_heading_2 = 0

total_time = 0

while True:
    current_time = time.time()
    elapsed_time = current_time - start_time
    
    if uart.any():
        ##### FORMAT: {heading},{pitch}
        b = uart.readline()

        try:
            msg = b.decode('utf-8')
            #print("msg: ", msg)
            msg_parts = msg.split(',')
            #print("msg_parts: ", msg_parts)
            new_setpoint = int(msg_parts[0])
            pitch = int(msg_parts[1])
            #print("New setpoint:", new_setpoint)
            #print("Pitch:", pitch)
            if (new_setpoint != None) and (new_setpoint >= 0) and (new_setpoint <= 360):
                integral = 0    # a new heading requires a reset to integral
                setpoint = new_setpoint
                # set camera servo here
            if (pitch >= 135):
                # might need to fix this with an offset
                servo_Angle(135)
            elif (pitch <= 0):
                servo_Angle(0)
            elif (pitch != None):
                servo_Angle(pitch)
        except:
            #print("error with importing heading and pitch")
            pass
    
    # Heading:
    # N = 0
    # S = 180
    x, y, z, temp = qmc5883.read_scaled()
    heading = degrees(atan2(y, x))
    smooth_heading = (heading + prev_heading_1 + prev_heading_2)/3
    prev_heading_2 = prev_heading_1
    prev_heading_1 = heading
    ax = round(imu.accel.x, 2)
    ay = round(imu.accel.y, 2)
    az = round(imu.accel.z, 2)
    #print("Heading:\t", round(heading, 2), "IMU ax:\t", round(imu.accel.x, 2), "ay:\t", round(imu.accel.y, 2), "az:\t", round(imu.accel.z, 2), "integral\t", integral, end="\r")
    try:
        log_file.write(f"{total_time},{x},{y},{z},{ax},{ay},{az},{smooth_heading},{output},{integral},{setpoint}\n")
    except:
        pass
    
    sleep(0.05)
    total_time += 0.05
    if total_time >= 30:
        PID_timer.deinit()
        break

# turn off motors and close log file
pwm_motor_top.duty_u16(0)
pwm_motor_bottom.duty_u16(0)
log_file.close()
