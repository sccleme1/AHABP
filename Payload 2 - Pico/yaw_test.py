# Scott Clemens
# 5 April 2024
# Autonomous High Altitude Balloon Payload
#   This program is meant to test yaw control with
#   differential outputs of top and bottom wheels
from imu import MPU6050
from time import sleep
from machine import Pin, UART, I2C, Timer, PWM
import utime, time
from QMC5883L import *
from math import atan2, degrees
from servo import Servo

# PID gains
KP = 5
KI = 0.1
KD = 0.1
integral = 0
last_error = 0

# global setpoints
HEADING = 0
SETPOINT = 90
# minimum disarm value for motors
FREQUENCY = 100     # Hz
DISARM = 3277
PWM_BASE = 8000
DIFFERENTIAL_CHANGE = 1000
# MIN 7000
# MAX 8000

# timer for PID control
#PID_timer = Timer(-1)

# PWM control for ESCs
pwm_motor_top = PWM(Pin(15)) #
pwm_motor_bottom = PWM(Pin(14)) #
pwm_motor_top.freq(FREQUENCY)
pwm_motor_bottom.freq(FREQUENCY)
pwm_motor_top.duty_u16(DISARM) # disarm value on top motor
pwm_motor_bottom.duty_u16(DISARM) # disarm value on bottom motor
sleep(1)

# PWM control for camera servo on GP13
camera_servo = Servo(13)
# UP = 0
# Horizontal = 80
# DOWN = 135


def PID(t):
    global KP, KI, KD, integral, last_error, heading, SETPOINT, DIFFERENTIAL_CHANGE
    DT = 0.1 # s
    
    error = SETPOINT - heading
    integral += error*DT
    derivative = (error - last_error)/DT
    last_error = error
    pid_output = KP*error + KI*integral + KD*derivative
    # TODO: determine left/right directional spin
    #       set top_output and bottom_output
    #       limit outputs max and min values
    output = max(0, min(pid_output, 1000))
    #print("setpoint:", setpoint, "heading:", round(heading, 2), "error", round(error, 2), "PID output:", output, "integral", integral, "          ", end="\r")


##### START PID CONTROL #####
#PID_timer.init(mode=Timer.PERIODIC, freq=10, callback=PID)


##### START WHEELS AT BASE SPEED #####
print("starting wheels")
pwm_motor_top.duty_u16(PWM_BASE)
pwm_motor_bottom.duty_u16(PWM_BASE)
sleep(2)

i = 0
while True:
    ##### LEFT TURN #####
    print("left turn")
    pwm_motor_top.duty_u16(PWM_BASE - DIFFERENTIAL_CHANGE)
    pwm_motor_bottom.duty_u16(PWM_BASE + DIFFERENTIAL_CHANGE)
    sleep(0.5)
    ##### STOP #####
    print("stop")
    pwm_motor_top.duty_u16(PWM_BASE)
    pwm_motor_bottom.duty_u16(PWM_BASE)
    sleep(2)
    ##### RIGHT TURN #####
    print("right turn")
    pwm_motor_top.duty_u16(PWM_BASE + DIFFERENTIAL_CHANGE)
    pwm_motor_bottom.duty_u16(PWM_BASE - DIFFERENTIAL_CHANGE)
    sleep(0.5)
    ##### STOP #####
    print("stop")
    pwm_motor_top.duty_u16(PWM_BASE)
    pwm_motor_bottom.duty_u16(PWM_BASE)
    sleep(2)
    i += 1
    if i >= 5:
        # turn off motors
        pwm_motor_top.duty_u16(0)
        pwm_motor_bottom.duty_u16(0)
        break

print("program ended")