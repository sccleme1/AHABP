# Scott Clemens
# 2024
# This program imports and image and identifes the brightest pixel,
#  the centroid of brightness values above an arbitrary threshold,
#  and determines the vector from the center of the image to those points.

#import numpy as np
from picamera2 import Picamera2
#from picamera2.array import PiRGBArray
import cv2 as cv
import time
import RPi.GPIO as GPIO

angle = 45
min_threshold = 225

def get_image():
    # this function takes an image and returns it as an array
    camera = Picamera2()
    camera.options['quality'] = 90
    #raw = PiRGBArray(camera)
    #camera.start_preview()
    camera.start()
    time.sleep(0.05)
    camera.capture_file("test_image.jpg")
    camera.stop()


def setup_servo():
    # sets up the servo
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    servo = GPIO.PWM(11, 50) # Pin 11, 50 Hz
    servo.start(0)
    # set direction to horizontal
    servo.ChangeDutyCycle(2 + angle/18)


def active_track(picture):
    # take an image and save it, then import and manipulate
    get_image()
    
    # import image
    filename = "test_image.jpg"
    imported = cv.imread(filename)
    image = cv.rotate(imported, cv.ROTATE_180)
    rows, columns, _ = image.shape

    # copy and convert image to grayscale then process
    orig = image.copy()
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    (minVal, maxVal, minLoc, maxLoc) = cv.minMaxLoc(gray)
    ret, thresh = cv.threshold(gray, min_threshold, 255, 0)
    M = cv.moments(thresh)

    # calculate image center
    cx = int(columns/2)
    cy = int(rows/2)
    
    # calculate centroid
    targx = int(M["m10"] /(1 + M["m00"]) )
    targy = int(M["m01"] /(1 + M["m00"]) )

    # calculate direction vector from center to centroid
    vx = targx - cx
    vy = targy - cy

    # now comes the tracking portion
    if vy > 0:
        if angle <=85: angle += 5
        servo.ChangeDutyCycle(2 + angle/18)
    if vy < 0:
        if angle >= 5: angle -= 5
        servo.ChangeDutyCycle(2 + angle/18)

    cv.imwrite(picture + "_" + filename, image)


def tracking_data():
    # calculate total time elapsed for processing
    stop = time.perf_counter()
    time_ms = round(1000*(stop - start), 2)
    maxFreq = round(1/(2*(stop - start)), 2)

    # place labels on things
    cv.putText(image, "target", (targx - 25, targy + 25), cv.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 100), 1)
    cv.circle(image, [targx, targy], 10, (32, 255, 32), 1)
    cv.putText(image, "brightest", (maxLoc[0] - 25, maxLoc[1] + 25), cv.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 255), 1)    
    cv.circle(image, maxLoc, 10, (32, 32, 255), 1)
    cv.putText(image, "image center", (cx - 25, cy + 25), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 100), 1)
    cv.circle(image, [cx, cy], 5, (255, 32, 32), 1)

    # draw vector arrows
    cv.arrowedLine(image, [cx, cy], [targx, targy], (255, 255, 0), 1) # center >> target
    cv.arrowedLine(image, [cx, cy], maxLoc, (255, 0, 255), 1) # center >> brightest pixel

    size = round(1e-6*(columns*rows), 1)
    print(f"Image size {rows}px height, {columns}px width, {size} MP")
    print(f"Center of Image at x = {cx}, y = {cy}")
    print(f"Movement vector: yaw: {vx}px, pitch: {vy}px")
    print(f"Time elapsed: {time_ms} ms")
    print(f"Max control loop frequency: {maxFreq} Hz")


def main():
    # minimum threshold value from 0 - 255
    # from the camera, the sun *should* be 255 always
    setup_servo()
    
    for i in range(20):
        active_track(i)
    
    #cv.imshow("Camera", image)
            
if __name__ == "__main__":
    main()

