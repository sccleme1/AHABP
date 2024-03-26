# Written by Scott Clemens
# for EEE 488/489 Senior Design I & II
# Autonomous High-Altitude Balloon Payload 

from machine import Pin, PWM, Timer
from time import sleep

revolutions = 0
hits = 0
current_time = 0
dt = 0.1

#### CONSTANTS ###
pi = 3.141592653589
diameter = 0.095      # m
radius = diameter/2   # m

### GLOBAL VARIABLES ###

# PWM Value for motor
# Minimum = 
PWM_val = 13000

# Setup pins and PWM frequency
pwm_built_in = PWM(Pin(25))
pwm_motor = PWM(Pin(0))

pwm_built_in.freq(100)
pwm_motor.freq(100)

# open file for writing
file=open("rpm_data.csv", "w")
file.write(f"PWM-RPMs Data\n")
file.write(f"PWM = {PWM_val}\n")


def IR_handler(pin):
    global revolutions
    global hits
    flags = IR_pin.irq().flags()

    if Pin.IRQ_RISING:
        hits += 1
        if hits >= 3:
            revolutions += 1
            hits = 0


def record_rpms():
    global revolutions
    global current_time
    global dt
    revolutions = 0

    IR_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=IR_handler)
    sleep(dt) # test for 0.01 seconds
    IR_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=None)

    #print(str(current_time) + "," + str(revolutions) + "\n")

    file.write(str(round(current_time, 1)) + "," + str(revolutions) + "\n")
    

# Setup IR pin and IR interrupt handler
IR_pin = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)  # GPIO 15 with internal pull-up resistor
#IR_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=IR_handler)

# start auto calibration of ESC
pwm_motor.duty_u16(10000)
pwm_built_in.duty_u16(1000)
sleep(1) # delay 1 second

print(f"*** Program starting ***")
print(f" 5 seconds at {PWM_val} PWM")
# turn on motor
pwm_motor.duty_u16(PWM_val) # turn on motor
pwm_built_in.duty_u16(PWM_val)

while current_time <= 5:
    record_rpms()
    current_time += dt
    print(f"Time: {round(current_time, 1)}", end="\r")
    
pwm_motor.duty_u16(0) # turn off motor
    
file.close()
print(f"*** Program ended ***")


