# Serial test

import os
import machine
from time import sleep

uart = machine.UART(0, 115200)
uart.init(bits=8, parity=None, stop=1)
print(uart)

b = None
msg = ""
i = 0

while True:
    sleep(1)
    if uart.any():
        b = uart.readline()
        uart.write(f"reply {i} from pico")
        #print(type(b))
        #print(b)
        try:
            msg = b.decode('utf-8')
            #print(type(msg))
            print(msg)
        except:
            pass