# Written by Scott Clemens
# for EEE 488/489 Senior Design I & II
# Autonomous High-Altitude Balloon Payload 

from machine import Pin, PWM
from time import sleep

#### CONSTANTS ###
pi = 3.141592653589
diameter = 0.95       # m
radius = diameter/2   # m

### GLOBAL VARIABLES ###
revolutions = 0
rising_hit = 0
sleep_time = 1
# PWM Value for motor
# Minimum = 3180
# Tested 3200
PWM_val = 3180

# Setup pins and PWM frequency
pwm_built_in = PWM(Pin(25))
pwm_motor = PWM(Pin(0))

pwm_built_in.freq(1000)
pwm_motor.freq(50)

# Setup IR pin and IR interrupt handler
#IR_pin = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)  # GPIO 17 with internal pull-up resistor
IR_pin = Pin(15, Pin.IN, Pin.PULL_UP)  # GPIO 15 with internal pull-up resistor
IR_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=IR_handler)

# start auto calibration of ESC
pwm_motor.duty_u16(1000)
sleep(1) # delay 1 second


def IR_handler(pin):
    flags = IR_pin.irq().flags()
    if flags & Pin.IRQ_RISING:
        # handle rising edge
        global rising_hit = 1
    else:
        # handle falling edge
        if rising_hit == 1:
            global revolutions += 1
        global rising_hit = 0


def loop():
    # turn on motor
    if (sleep_time <= 15):
        pwm_motor.duty_u16(PWM_val) # turn on motor
        sleep(sleep_time) # wait to get up to speed
        IR_pin.irq().init() # enable interrupt
        sleep(1) # test for 1 second
        IR_pin.irq().deinit() # turn off interrupt
        pwm_motor.duty_u16(0) # turn off motor
        
        RPMs = revolutions*60
        omega = revolutions*2*pi/60

        print(f"PWM: {PWM_val} for {sleep_time} s")
        print(f"Recorded interrupts: {revolitions}")
        print(f"Estimated RPMs: {RPMs}")
        print(f"Estimated angular velocity: {omega} rad/s")
        print()
        
        # reset revolutions
        global revolutions = 0
        global sleep_time += 1
        
    else:
        print(f"Reached limit of program, please restart")

    sleep(10)


while True:
    loop()
