# timers test
# from Electrocredible

from machine import Pin, Timer
from time import sleep

led = Pin(25, Pin.OUT) # built-in LED
tim = Timer(-1)
toggles = 0

print("Starting program, initiating timer")

def PIT(t):
    global toggles
    led.toggle()
    toggles += 1
    
# instead of 'period', you can put 'freq' for frequency in Hz
tim.init(mode=Timer.PERIODIC, period=100, callback=PIT) # period in ms


i = 0

# after 10 seconds, stop timer
while True:
    print("i =", i)
    i += 1
    sleep(1)
    if i >= 7:
        # turn off LED, stop timer, end function
        led.value(0)
        tim.deinit()
        break
    
print(f"Timer stopped after {i} cycles and {toggles} toggles; program ended")