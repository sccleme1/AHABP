import cv2 as cv
import time
import datetime
import os

print("Hello from ahabp_node_opencv.py")
print("began at", datetime.datetime.now())

# camera servo can only go between 0 and 130 degrees
angle = 80

path = "/home/scott/Documents/AHABP/OpenCV_Tests/Images"

capture = cv.VideoCapture(0)

# on Raspberry Pi Camera v2 the image size is:
# 480 rows
# 640 columns
cx = 320
cy = 240
minimum = 250

picture = 1
i = 0
while True:
    istrue, frame = capture.read()
    date = datetime.datetime.now()
    gray = cv.rotate(frame, cv.ROTATE_180)
    frame = cv.rotate(frame, cv.ROTATE_180)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    thresholding, thresh = cv.threshold(gray, minimum, 255, cv.THRESH_BINARY)
    #thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,5,2)
        
    # copy and convert image to grayscale then process
    (minVal, maxVal, minLoc, maxLoc) = cv.minMaxLoc(gray)
    M = cv.moments(thresh)

    # calculate centroid
    targx = int(M["m10"] / (M["m00"]+1))
    targy = int(M["m01"] / (M["m00"]+1))

    # calculate direction vector from image center to centroid
    vx = targx - cx
    vy = targy - cy

    # place vector arrow and label
    cv.putText(frame, "target", (targx - 45, targy + 45), cv.FONT_HERSHEY_SIMPLEX, 1, (25, 25, 255), 2)
    cv.circle(frame, [targx, targy], 25, (25, 25, 255), 2)
    cv.arrowedLine(frame, [cx, cy], [targx, targy], (25, 25, 255), 2) # center >> target
    
    ### Output screens ###
    cv.imshow('Output', thresh)
    cv.imshow('Camera', frame)
    
    if (vy/10) > 0:
        if angle >= 5:
            angle -= 1
        #servo.ChangeDutyCycle(2 + (angle/18)) # This is where the actuator stuff goes
        #print(vy/10, "pitch DOWN", angle)
    elif (vy/10) < 0:
        if angle <= 95:
            angle += 1
        #servo.ChangeDutyCycle(2 + (angle/18))
        #print(vy/10, "pitch UP", angle)
    
    if cv.waitKey(20) & 0xFF==ord('d'):
        break

    if i >= 900:
        cv.imwrite(os.path.join(path, "thresh_" + str(picture) + "_" + str(datetime.datetime.now()) + ".jpg"), thresh)
        cv.imwrite(os.path.join(path, "frame_" + str(picture) + "_" + str(datetime.datetime.now()) + ".jpg"), frame)
        print(f"Saved picture {picture} at {date}")
        i = 0
        picture += 1
    
    #increment i
    i += 1

capture.release()
cv.destroyAllWindows
