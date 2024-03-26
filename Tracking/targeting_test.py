# Scott Clemens
# 2024
# This program imports and image and identifes the brightest pixel,
#  the centroid of brightness values above an arbitrary threshold,
#  and determines the vector from the center of the image to those points.

#import numpy as np
#from picamera import Picamera2
import cv2 as cv
import time


def get_image():
    # this function takes an image and returns it as an array
    camera = PiCamera()
    raw = PiRGBArray(camera)
    time.sleep(0.05)
    camera.capture(raw, format="bgr")
    image = raw.array
    return image


def main():
    # minimum threshold value from 0 - 255
    # from the camera, the sun *should* be 255 always
    min_threshold = 245
    start = time.perf_counter()


    # import image
    ##image = get_image()  # from camera
    filename = "test_image.jpg" # from file
    image = cv.imread(filename)
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
    targx = int(M["m10"] / M["m00"])
    targy = int(M["m01"] / M["m00"])

    # calculate direction vector from center to centroid
    vx = targx - cx
    vy = targy - cy

    # calculate total time elapsed for processing
    stop = time.perf_counter()
    time_ms = round(1000*(stop - start), 2)
    maxFreq = round(1/(2*(stop - start)), 2)

    # place labels on things
    cv.putText(image, "target", (targx - 175, targy + 175), cv.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 100), 4)
    cv.circle(image, [targx, targy], 50, (32, 255, 32), 8)
    cv.putText(image, "brightest", (maxLoc[0] - 175, maxLoc[1] + 175), cv.FONT_HERSHEY_SIMPLEX, 3, (100, 100, 255), 4)    
    cv.circle(image, maxLoc, 50, (32, 32, 255), 8)
    cv.putText(image, "image center", (cx - 175, cy + 175), cv.FONT_HERSHEY_SIMPLEX, 3, (255, 100, 100), 4)
    cv.circle(image, [cx, cy], 50, (255, 32, 32), 8)

    # draw vector arrows
    cv.arrowedLine(image, [cx, cy], [targx, targy], (255, 255, 0), 8) # center >> target
    cv.arrowedLine(image, [cx, cy], maxLoc, (255, 0, 255), 8) # center >> brightest pixel

    size = round(1e-6*(columns*rows), 1)
    print(f"Image size {rows}px height, {columns}px width, {size} MP")
    print(f"Center of Image at x = {cx}, y = {cy}")
    print(f"Movement vector: yaw: {vx}px, pitch: {vy}px")
    print(f"Time elapsed: {time_ms} ms")
    print(f"Max control loop frequency: {maxFreq} Hz")

    cv.imshow("gray", image)
    cv.imwrite("cv_edit_" + filename, image)

            
if __name__ == "__main__":
    main()

