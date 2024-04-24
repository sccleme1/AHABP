import utime
from servo import Servo

s1 = Servo(18)       # Servo pin is connected to GP18
# UP = 0
# Horizontal = 80
# DOWN = 135
def servo_Map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
 
def servo_Angle(angle):
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    s1.goto(round(servo_Map(angle,0,180,0,1024))) # Convert range value to angle value
    print("angle", angle, "           ", end="\r")
    
if __name__ == '__main__':
    while True:
        print("Looking horizontal")
        servo_Angle(80)
        utime.sleep(2)
        print("Looking UP")
        servo_Angle(0)
        utime.sleep(2)
        print("Looking horizontal")
        servo_Angle(80)
        utime.sleep(2)
        print("Looking DOWN")
        servo_Angle(135)
        utime.sleep(2)
