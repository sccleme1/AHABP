# Scott Clemens
# 26 March 2024
# Autonomous High-Altitude Balloon Payload
#
#
### TRACKING ###

import ephem
import cv2 as cv
import time
import datetime
import os


date = datetime.datetime.now()

# global variables
pi = 3.14159265358979323846

# camera servo angle limits
# +76 is maximum
# 0 is horizontal
# -28 is minimum
camera_angle = 0

# folder to store images within workspace
path = '/home/anyell/ahabp_v2_ws/Images'

# file to save log information to
data_file = 'launch_data.csv'
file = open(data_file, 'w')
file.write(f"Data log for {date}\n")
file.write(f"Time,Latitude,Longitude,Altitude,Zenith,Azimuth,Heading,Camera,Yaw,Pitch\n")
file.close()

capture = cv.VideoCapture(0)


print('#### Running ahabp_node_tracking.py ####')


def get_compass_direction(angle):
    ''' This converts degrees to cardinal directions for ease of reading '''
    
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(angle / (360. / len(directions))) % len(directions)
    
    return directions[index]


def sun_angle_and_direction(latitude, longitude, date):
    ''' This function calculates zenith, azimuth, and compass direction
    based on the GPS and date/time data '''
    
    observer = ephem.Observer()
    observer.lat = str(latitude)
    observer.lon = str(longitude)

    observer.date = date
    sun = ephem.Sun(observer)

    zenith_angle = 90 - sun.alt*180/pi
    azimuth_angle = (sun.az*180/pi) % 360
    compass_direction = get_compass_direction(azimuth_angle)

    return zenith_angle, azimuth_angle, compass_direction


def movement_needed(payload_heading, azimuth_angle, zenith_angle):
    ''' This function calculates yaw and pitch error '''
    
    yaw = round(azimuth_angle - payload_heading, 2)
    pitch = round(zenith_angle - camera_angle, 2)

    return yaw, pitch


def ephem_update():
    ''' This function calculates the zenith and azimuth of the Sun
        based on the real-time GPS and heading data from the payload '''

    latitude = 30.266666    # REAL-TIME
    longitude = -97.733330  # REAL-TIME
    altitude = 100          # REAL-TIME
    payload_heading = 88    # REAL-TIME

    date = datetime.datetime.now()
    zenith_angle, azimuth_angle, compass_direction = sun_angle_and_direction(latitude, longitude, date)
    yaw_ephem, pitch_ephem = movement_needed(payload_heading, azimuth_angle, zenith_angle)

    return yaw_ephem, pitch_ephem, latitude, longitude, altitude


def target(frame, minimum=250, cx=320, cy=240):
    ''' This function targets the centroid of a frame and outputs
        vector in x and y of the error between center of frame and the centroid
        
        Raspberry Pi Camera v2 the image size is:
        480 rows (vertical)
        640 columns (horizontal)
    '''
    
    # copy and convert image to grayscale then process
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    thresholding, thresh = cv.threshold(gray, minimum, 255, cv.THRESH_BINARY)   
    (minVal, maxVal, minLoc, maxLoc) = cv.minMaxLoc(gray)
    M = cv.moments(thresh)

    # calculate centroid
    targx = int(M["m10"] / (M["m00"]+1))
    targy = int(M["m01"] / (M["m00"]+1))

    # calculate direction vector from center to centroid
    yaw_target = targx - cx
    pitch_target = targy - cy

    # place vector arrow and label
    cv.putText(frame, "target", (targx - 45, targy + 45), cv.FONT_HERSHEY_SIMPLEX, 1, (25, 25, 255), 2)
    cv.circle(frame, [targx, targy], 25, (25, 25, 255), 2)
    cv.arrowedLine(frame, [cx, cy], [targx, targy], (25, 25, 255), 2) # center --> target

    return yaw_target, pitch_target, frame


def PID():
    ''' This is where the proportional - integral - derivative function will go '''
    pass


picture = 1
i = 0
while True:
    istrue, frame = capture.read()
    date = datetime.datetime.now()
    original = frame.copy()

    # error calculations
    # 'ephem' error is based on calculation with GPS/heading
    # 'target' error is based on what's in the camera frame
    yaw_ephem, pitch_ephem, latitude, longitude, altitude = ephem_update()
    yaw_target, pitch_target, targeted = target(frame)

    
    ### Output screens ###
    #cv.imshow('Output', thresh)
    #cv.imshow('Camera', frame)

    # This is where the actuator stuff goes
    if pitch_target > 50:
        print("Vertical error:", pitch_target, "pitch DOWN")
        # PITCH DOWN
    elif pitch_target < -50:
        print("Vertical error:", pitch_target, "pitch UP")
        # PITCH UP

    if yaw_target > 100:
        # This is where the actuator stuff goes
        print("Horizontal error:", yaw_target - cx, "pitch LEFT")
        # PITCH DOWN
    elif yaw_target < -100:
        print("Horizontal error:", yaw_target - cx, "pitch RIGHT")
        # PITCH UP

    # append the data to the log file
    with open(data_file, "a") as file:
        file.write(f"{date},{latitude},{longitude},{altitude},{zenith_angle},{azimuth_angle},{payload_heading},{camera_angle},{yaw_ephem},{pitch_ephem}\n")
    
    if cv.waitKey(20) & 0xFF==ord('d'):
        break

    if i >= 900:
        # every 30 seconds, save the images
        cv.imwrite(os.path.join(path, "raw_" + str(picture) + "_" + str(datetime.datetime.now()) + ".jpg"), original)
        cv.imwrite(os.path.join(path, "threshold_" + str(picture) + "_" + str(datetime.datetime.now()) + ".jpg"), thresh)
        cv.imwrite(os.path.join(path, "targeted_" + str(picture) + "_" + str(datetime.datetime.now()) + ".jpg"), targeted)
        print(f"Saved picture {picture} at {date}")
        i = 0
        picture += 1
    
    #increment i
    i += 1


capture.release()
cv.destroyAllWindows
