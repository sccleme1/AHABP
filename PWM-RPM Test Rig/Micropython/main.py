from machine import Pin, PWM
from time import sleep

pwm_built_in = PWM(Pin(25))
pwm_motor = PWM(Pin(0))

pwm_built_in.freq(1000)
pwm_motor.freq(50)

IR_pin = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)  # GPIO 17 with internal pull-up resistor

# start auto calibration
pwm_built_in.duty_u16(1000)
pwm_motor.duty_u16(1000)
sleep(1) # in seconds

hits = 0
nohits = 0


# pwm_motor.duty_u16(3180)
# sleep(2) # wait 1.25 seconds to get up to speed
# 
# for i in range(100000):
#   if IR_pin.value() == 1:
#       hits += 1
#       #print("Hit")
#   else:
#       nohits += 1
#       #print("No Hit")
#   sleep(0.00001)
#   
# pwm_motor.duty_u16(0) # turn off
# 
# print(f"At 10 us polling:")
# print(f"Hits: {hits} \t No Hits: {nohits}")
# print(f"Total hit percentage: {100*hits/(nohits+hits)}%")
# print(f"Estimated RPMs: {hits*60/8}")
# print()

# sleep(10)
# 
# pwm_motor.duty_u16(3200)
# sleep(1.25) # wait 1.25 seconds to get up to speed
# pwm_motor.duty_u16(3175)
# sleep(0.5)
# 
# for i in range(10000):
#   if IR_pin.value() == 1:
#       hits += 1
#       #print("Hit")
#   else:
#       nohits += 1
#       #print("No Hit")
#   sleep(0.0001)
#   
# pwm_motor.duty_u16(0) # turn off
# 
# print(f"At 100 us polling:")
# print(f"Hits: {hits} \t No Hits: {nohits}")
# print(f"Total hit percentage: {100*hits/(nohits+hits)}%")
# print(f"Estimated RPMs: {hits*60}")
sleep_time = 1
while True:

#     for duty in range(6):
#          pwm_built_in.duty_u16(duty*1200)
#          pwm_motor.duty_u16(10*duty + 3150)
#          print(f"PWM = {10*duty + 3150}")
#          sleep(1)
     
     #pwm_motor.duty_u16(0)
    pwm_motor.duty_u16(3180) # 3180
    sleep(sleep_time)
     
    for i in range(100000):
        if IR_pin.value() == 1:
            hits += 1
              #print("Hit")
        else:
            nohits += 1
              #print("No Hit")
        sleep(0.00001)
          
    pwm_motor.duty_u16(0) # turn off

    print(f"At 10 us polling with drive time {sleep_time} s:")
    print(f"Hits: {hits} \t No Hits: {nohits}")
    print(f"Total hit percentage: {100*hits/(nohits+hits)}%")
    print(f"Estimated RPMs: {hits*60/8} RPMs")
    print()
    hits = 0
    nohits = 0
    sleep_time += 1
    sleep(10)
     
#     for duty in range(5, 0, -1):
#          pwm_built_in.duty_u16(duty*1200)
#          pwm_motor.duty_u16(10*duty + 3150)
#          print(f"PWM = {10*duty + 3150}")
#          sleep(1)
         
#     sleep(10)
#      
     