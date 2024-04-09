# Written by Scott Clemens
# for EEE 488/489 Senior Design I & II
# Autonomous High-Altitude Balloon Payload 

from machine import Pin, PWM, Timer
from time import sleep
import time
import math

revolutions = 0
hits = 0
current_time = 0
dt = 0.1

#### CONSTANTS ###
pi = 3.141592653589
diameter = 0.095      # m
radius = diameter/2   # m
frequency = 100 	      # Hz
### GLOBAL VARIABLES ###

# PWM Value for motor
# Minimum = 7000
# Maximum = 8000
PWM_val = 7000
duty_time = int(1e6 * PWM_val/ (frequency * 65535) ) # us

# Setup pins and PWM frequency
pwm_built_in = PWM(Pin(25))
pwm_motor_top = PWM(Pin(15))    # CW
pwm_motor_bottom = PWM(Pin(14)) # CCW

#pwm_built_in.freq(100)
pwm_built_in.freq(frequency)
pwm_motor_top.freq(frequency)
pwm_motor_bottom.freq(frequency)


max_duty_cycle = 7800
min_duty_cycle = 0
# MIN 7400
# MAX 

# open file for writing
#file=open(f"rpm_data_duty_{duty_time}.csv", "w")
#file.write(f"{PWM_val}\n")


def IR_handler(pin):
    global revolutions
    global hits
    flags = IR_pin.irq().flags()

    if Pin.IRQ_RISING:
        hits += 1


def record_rpms():
    global revolutions
    global current_time
    global dt
    global hits
    revolutions = 0

    IR_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=IR_handler)
    sleep(dt) # test for 0.01 seconds
    #file.write(str(round(current_time, 1)) + "," + str(hits*200) + "\n")
    hits = 0
    IR_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=None)
    

    #print(str(current_time) + "," + str(revolutions) + "\n")

    

# Setup IR pin and IR interrupt handler
IR_pin = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)  # GPIO 21 with internal pull-up resistor
#IR_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=IR_handler)

# start auto calibration of ESC
pwm_motor_top.duty_u16(3277)
pwm_motor_bottom.duty_u16(3277)
pwm_built_in.duty_u16(1000)
sleep(1) # delay 1 second

print(f"*** Test starting ***")
print(f" 5 seconds at {PWM_val} PWM, for duty time of {duty_time} us")
# turn on motor
pwm_motor_top.duty_u16(PWM_val) # turn on motor

pwm_motor_bottom.duty_u16(PWM_val) # turn on motor
pwm_built_in.duty_u16(PWM_val)

while current_time <= 5:
    #record_rpms()
    print(f"Time: {round(current_time, 1)}", end="\r")
    current_time += dt
    sleep(dt)


    
pwm_motor_top.duty_u16(0) # turn off motor
pwm_motor_bottom.duty_u16(0) # turn off motor

#file.close()
print(f"*** Test ended ***")


