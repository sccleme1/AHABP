# Scott Clemens
# March 2024
# High Altitude Autonomous Balloon Payload

import numpy as np
import cv2 as cv
import time
import RPi.GPIO as GPIO


### This is for servo driving using RPi ###
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
servo = GPIO.PWM(11, 50) # Pin 11, 50 Hz

# camera servo can only go between 0 and 130 degrees
servo.start(0)
angle = 80

capture = cv.VideoCapture(0)

# on Raspberry Pi Camera v2 the image size is:
# 480 rows
# 640 columns
cx = 320
cy = 240
minimum = 250

i = 0
while True:
    istrue, frame = capture.read()
    
    # image center
    gray = cv.rotate(frame, cv.ROTATE_180)
    frame = cv.rotate(frame, cv.ROTATE_180)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    thresholding, thresh = cv.threshold(gray, minimum, 255, cv.THRESH_BINARY)
    
    # copy and convert image to grayscale then process
    (minVal, maxVal, minLoc, maxLoc) = cv.minMaxLoc(gray)
    #ret, thresh = cv.threshold(gray, min_threshold, 255, 0)
    M = cv.moments(thresh)

    # calculate centroid
    targx = int(M["m10"] / (M["m00"]+1))
    targy = int(M["m01"] / (M["m00"]+1))

    # calculate direction vector from center to centroid
    vx = targx - cx
    vy = targy - cy

    cv.putText(frame, "target", (targx - 35, targy + 35), cv.FONT_HERSHEY_SIMPLEX, 2, (100, 255, 100), 2)
    cv.circle(frame, [targx, targy], 25, (255, 255, 32), 2)
    cv.arrowedLine(frame, [cx, cy], [targx, targy], (255, 255, 0), 2) # center >> target

    ### Output screens ###
    #cv.imshow('Output', thresh)
    #cv.imshow('Camera', frame)
    
    if (vy/10) > 0:
        if angle >= 5:
            angle -= 1
        servo.ChangeDutyCycle(2 + (angle/18))
        #print(vy/10, "pitch DOWN", angle, " ", end=")
    elif (vy/10) < 0:
        if angle <= 95:
            angle += 1
        servo.ChangeDutyCycle(2 + (angle/18))
        #print(vy/10, "pitch UP", angle)
    
    if cv.waitKey(20) & 0xFF==ord('d'):
        break

    # save images every 100 times
    if i >= 100:
        cv2.imwrite("thresh" + str(i) + ".jpg", thresh)
        cv2.imwrite("frame" + str(i) + ".jpg", frame)
        i = 0
        
    # increment i
    i += 1


capture.release()
cv.destroyAllWindows
