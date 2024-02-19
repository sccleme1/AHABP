import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)


GPIO.setup(11, GPIO.OUT)
servo = GPIO.PWM(11, 50) # Pin 11, 50 Hz
servo.start(0)

print("Camera swing arm can only go between 0 and 90 degrees")
print("Testing full range")

for i in range(18):
        print(f"Angle: {i*5} deg")
        servo.ChangeDutyCycle(2 + (i*5)/18)
        time.sleep(0.5)
        servo.ChangeDutyCycle(0)

servo.ChangeDutyCycle(2 + 45/18)
print("Test complete")

try:
        while True:
                angle = float(input("Enter angle between 0 and 90: "))
                if (angle >= 0) and (angle <= 90):
                        servo.ChangeDutyCycle(2 + (angle/18))
                        time.sleep(0.5)
                        servo.ChangeDutyCycle(0)
                else:
                        print("Not a valid angle")

finally:
        servo.stop()
        GPIO.cleanup()
        print("End")
