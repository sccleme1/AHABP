import ephem
from math import degrees
import datetime

pi = 3.14159265358979323846


# eliminate math import
# incorporate into video_thresholding.py for ideal tracking


def get_compass_direction(angle):
    # this just converts to cardinal directions for ease of use
    #  not to be used in actual operation
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(angle / (360. / len(directions))) % len(directions)
    
    return directions[index]


def sun_angle_and_direction(latitude, longitude, date):
    
    observer = ephem.Observer()
    observer.lat = str(latitude)
    observer.lon = str(longitude)

    observer.date = date
    sun = ephem.Sun(observer)

    zenith_angle = 90 - degrees(sun.alt)
    azimuth_angle = degrees(sun.az)
    azimuth_angle_degrees = azimuth_angle % 360
    compass_direction = get_compass_direction(azimuth_angle_degrees)

    return zenith_angle, azimuth_angle_degrees, compass_direction


def movement_needed(payload_heading, azimuth_angle, zenith_angle):
    # calculated yaw and pitch needed
    yaw = round(azimuth_angle - payload_heading, 2)
    pitch = round(zenith_angle - camera_angle, 2)

    return yaw, pitch

if __name__ == "__main__":

    # Tempe, AZ lat/long
    # actual location needs to be streamed from the GPS
    latitude = 33.427204
    longitude = -111.939896

    # actual payload heading in degrees
    payload_heading = 88

    # actual camera pitch in degrees
    # 0 corresponds to horizontal
    camera_angle = 0

    # date format: '2024-03-12 12:00:00'
    date = datetime.datetime(2024, 4, 8, 13, 9, 1, 130320, tzinfo=datetime.timezone.utc)
    zenith_angle, azimuth_angle, compass_direction = sun_angle_and_direction(latitude, longitude, date)
    yaw, pitch = movement_needed(payload_heading, azimuth_angle, zenith_angle)

    # print out the given information
    #  not to be used in actual operation
    print("Date", date)
    print("Latitude:", latitude)
    print("Longitude:", longitude)
    print("Sun's zenith angle:", round(zenith_angle, 2), "degrees")
    print("Sun's azimuth angle:", round(azimuth_angle, 2), "degrees")
    print("Sun's compass direction:", compass_direction)
    print()
    print("Payload's heading", payload_heading, "degrees")
    print("Camera's angle", camera_angle, "degrees")
    print("Yaw needed", yaw, "degrees")
    print("Pitch needed", pitch, "degrees")
