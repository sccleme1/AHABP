# Scott Clemens
# 26 March 2024
# Autonomous High-Altitude Balloon Payload
#
#
### TRACKING FUNCTIONS ###

import ephem
import datetime

pi = 3.14159265358979323846

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

