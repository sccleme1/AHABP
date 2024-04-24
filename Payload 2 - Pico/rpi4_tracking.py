#!/usr/bin/python

'''
Scott Clemens
11 April 2024
Autonomous High-Altitude Balloon Payload
This program is meant to run on a Raspberry Pi 4
to track the sun and send information back to a
Raspberry Pi Pico that does real-time control
'''
### TRACKING ###

import ephem
from geomag import declination
import cv2 as cv
import time
import datetime
import os
import serial

ser = serial.Serial(
    port = '/dev/serial0',
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 0
)

date = datetime.datetime.now()

# global variables
pi = 3.14159265358979323846

# camera servo angle limits
# +76 is maximum
# 0 is horizontal
# -28 is minimum
camera_angle = 0
centroids_x = [0, 0, 0, 0, 0]
centroids_y = [0, 0, 0, 0, 0]

# magnetometer offset in degrees
offset = 0

# folder to store images within workspace
path = '/home/pi/Documents/images'

# file to save log information to
data_file = f'launch_data_{date}.txt'
file = open(data_file, 'w')

capture = cv.VideoCapture(0)
cx = 320
cy = 240

print("#### Running tracking.py ####")


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

    zenith_angle = int(sun.alt*180/pi)
    azimuth_angle = int((sun.az*180/pi) % 360)
    compass_direction = get_compass_direction(azimuth_angle)

    return zenith_angle, azimuth_angle, compass_direction


def movement_needed(payload_heading, azimuth_angle, zenith_angle):
    ''' This function calculates yaw and pitch error '''

    yaw = int(azimuth_angle - payload_heading)
    pitch = int(zenith_angle - camera_angle)

    return yaw, pitch


def ephem_update(latitude, longitude):
    ''' This function calculates the zenith and azimuth of the Sun
        based on the real-time GPS and heading data from the payload '''

    date = datetime.datetime.now()
    zenith_angle, azimuth_angle, compass_direction = sun_angle_and_direction(latitude, longitude, date)

    return zenith_angle, azimuth_angle

def rolling_average(values, new_value):
    ''' This function calculates a rolling average to avoid jittering between edge cases '''
    values.append(new_value)
    if len(values) >= 5:
        values.pop(0)

    return sum(values) / len(values)


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

    # calculate rolling average of last 5
    yaw_target_smooth = rolling_average(centroids_x, yaw_target)
    pitch_target_smooth = rolling_average(centroids_y, pitch_target)


    # place vector arrow and label
    cv.putText(frame, "target", (targx - 45, targy + 45), cv.FONT_HERSHEY_SIMPLEX, 1, (25, 25, 255), 2)
    cv.circle(frame, [targx, targy], 25, (25, 25, 255), 2)
    cv.arrowedLine(frame, [cx, cy], [targx, targy], (25, 25, 255), 2) # center --> target

    return yaw_target_smooth, pitch_target_smooth, frame, thresh

##### INITIALIZE SERIAL AND WAIT FOR LATITUDE AND LONGITUDE VALUES #####
while True:

    #
    try:
        #msg = ser.read(ser.inWaiting()).decode('utf-8')
        msg = ser.readline().decode('utf-8')

        if msg != "":
            print(msg)
            parsed = msg.split(',')
            #print(parsed)
            if parsed[0] and parsed[1] and parsed[2] and parsed[3] and parsed[4]:
                #print(parsed)
                latitude = float(parsed[1])
                longitude = float(parsed[3])
                print("LATITUDE:", latitude, " LONGITUDE:", longitude)
                break
            time.sleep(1)
            msg = ""  # to avoid continuously reading blank
    except:
        #print("something went wrong")
        pass

zenith_angle, azimuth_angle = ephem_update(latitude, longitude)
declination_angle = int(declination(latitude, longitude))
#print("finished reading, writing to serial")
heading = azimuth_angle
print("ZENITH:", zenith_angle, "AZIMUTH:", azimuth_angle)
msg_out = "{},{},{}".format(heading, zenith_angle, declination_angle)
msg_out_bytes = msg_out.encode('utf-8')
ser.write(msg_out_bytes)
#print(f"wrote '{msg_out}' to serial")
#print("PROGRAM ENDED SUCCESSFULLY")
# append the data to the log file
try:
    file.write(f"{date}\n")
    file.write(f"Latitude: {latitude}\tLongitude: {longitude}\n")
    file.write(f"Zenith: {zenith_angle}\tAzimuth: {azimuth_angle}\tDeclination: {declination_angle}\n")
except:
    pass

yaw_target = heading
pitch_target = zenith_angle

picture = 1
i = 0
while True:
    istrue, frame = capture.read()
    date = datetime.datetime.now()
    original = frame.copy()

    # ephem Sun location:
    zenith_angle, azimuth_angle = ephem_update(latitude, longitude)
    # camera tracking Sun location:
    yaw, pitch, targeted, thresh = target(frame)
    declination_angle = int(declination(latitude, longitude))
    # yaw thresholds
    if (yaw > 100) and (yaw <= 220):
        yaw_target = 10 + azimuth_angle
    if (yaw < -100) and (yaw >= -220):
        yaw_target = azimuth_angle - 10
    if (yaw > 220):
        yaw_target = 21 + azimuth_angle
    if (yaw < -220):
        yaw_target = azimuth_angle - 21
    else:
        yaw_target = azimuth_angle

    # pitch thresholds
    if (pitch > 80) and (pitch <= 160):
        pitch_target = zenith_angle + 8
    if (pitch < -80) and (pitch >= -160):
        pitch_target = zenith_angle - 8
    if (pitch > 160):
        pitch_target = zenith_angle + 16
    if (pitch < -160):
        pitch_target = zenith_angle - 16
    else:
        pitch_target = zenith_angle

    ### Output screens ###
    #cv.imshow('Output', thresh)
    #cv.imshow('Camera', frame)

    try:
        ser.write(f"{yaw_target},{pitch_target},{declination_angle}").encode('utf-8')
        file.write(f"Heading: {yaw_target}\tPitch: {pitch_target}\n")
    except:
        file.write(f"ERROR: could not write '{yaw_target},{pitch_target}' to serial\n")
        pass
    if cv.waitKey(20) & 0xFF==ord('d'):
        break

    try:
        if i >= 900:
            # every 30 seconds, save the images
            cv.imwrite(os.path.join(path, "raw_" + str(picture) + "_" + str(datetime.datetime.now()) + ".jpg"), original)
            cv.imwrite(os.path.join(path, "threshold_" + str(picture) + "_" + str(datetime.datetime.now()) + ".jpg"), thresh)
            cv.imwrite(os.path.join(path, "targeted_" + str(picture) + "_" + str(datetime.datetime.now()) + ".jpg"), targeted)
            #print(f"Saved picture {picture} at {date}"
            file.write(f"Saved picture {picture} at {date}\n")
            i = 0
            picture += 1
    except:
        file.write(f"ERROR: failed to save pictures\n")

    #increment i
    i += 1
    if picture >= 5:
        break

##### END PROGRAM #####
file.write(f"Program ended at {date}\n")
file.close()
capture.release()
cv.destroyAllWindows


