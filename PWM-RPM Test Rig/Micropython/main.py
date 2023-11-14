# Written by Scott Clemens
# for EEE 488/489 Senior Design I & II
# Autonomous High-Altitude Balloon Payload 

from machine import Pin, PWM, SPI
from time import sleep
import sdcard
import os

#### CONSTANTS ###
pi = 3.141592653589
diameter = 0.95       # m
radius = diameter/2   # m

### GLOBAL VARIABLES ###
revolutions = 0
rising_hit = 0
sleep_time = 0.5
# PWM Value for motor
# Minimum = 3180
# Tested 3200
PWM_val = 3400

# Setup pins and PWM frequency
pwm_built_in = PWM(Pin(25))
pwm_motor = PWM(Pin(0))

pwm_built_in.freq(1000)
pwm_motor.freq(50)

# Initialize the SD card reader
spi = SPI(1, baudrate = 40000000, sck = Pin(10), mosi = Pin(11), miso = Pin(12))
sd = sdcard.SDCard(spi, Pin(13))
vfs = os.VfsFat(sd)
 
# Mount the SD card, open file
os.mount(sd, '/sd')
print(os.listdir('/sd'))
file = open("/sd/rpm-pwm_data.txt", "w")
file.write(f"PWM-RPMs Data")
file.write(f"PWM = {PWM_val}")

def IR_handler(pin):
    global revolutions
    global rising_hit
    flags = IR_pin.irq().flags()
    #print("Flags", flags, "Pin.IRQ_RISING", Pin.IRQ_RISING, "Pin.IRQ_FALLING", Pin.IRQ_FALLING)
#     if flags & Pin.IRQ_RISING:
#         # handle rising edge
#         rising_hit = 1
#     else:
#         # handle falling edge
#         if rising_hit == 1:
#             revolutions += 1
    if Pin.IRQ_RISING:
        #rising_hit = 0
        revolutions += 1


# Setup IR pin and IR interrupt handler
IR_pin = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)  # GPIO 15 with internal pull-up resistor
#IR_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=IR_handler)

# start auto calibration of ESC
pwm_motor.duty_u16(1000)
sleep(1) # delay 1 second


def test_loop():
    global revolutions
    global sleep_time
    # turn on motor
    if (sleep_time <= 7):
        pwm_motor.duty_u16(PWM_val) # turn on motor
        
 
        #sleep(7) # wait to get up to speed
        sleep(sleep_time) # wait to get up to speed

        revolutions = 0
        #IR_pin.irq().init() # enable interrupt
        IR_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=IR_handler)
        sleep(0.25) # test for 0.25 seconds
        #IR_pin.irq().deinit() # turn off interrupt
        IR_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=None)

        RPMs = revolutions*60*4
        omega = revolutions*2*pi/60
        pwm_motor.duty_u16(0) # turn off motor
        
        
        print(f"PWM: {PWM_val} for {sleep_time} s")
        print(f"Recorded interrupts: {revolutions}")
        print(f"Estimated RPMs: {RPMs}")
        print(f"Estimated angular velocity: {omega} rad/s")
        print()
        file.write(f"{RPMs},{omega}")
         
        if (sleep_time <= 3.5):
            # increment time
            sleep_time += 0.5
        elif (sleep_time >= 4):
            sleep_time += 1
        
    else:
        print(f"*** Reached limit of program, please close and remove SD card ***")
        file.close()
        
    sleep(40)


while True:
    test_loop()
