import ephem
import datetime
from geomag import declination

pi = 3.14159265358979323846

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

    zenith_angle = 90 - int(sun.alt*180/pi)
    azimuth_angle = int(sun.az*180/pi) + 90
    compass_direction = get_compass_direction(azimuth_angle)

    return zenith_angle, azimuth_angle, compass_direction


def movement_needed(payload_heading, azimuth_angle, zenith_angle):
    # calculated yaw and pitch needed
    yaw = round(azimuth_angle - payload_heading, 2)
    pitch = round(zenith_angle - camera_angle, 2)

    return yaw, pitch

if __name__ == "__main__":

    # Tempe, AZ
    latitude = 33.4213
    longitude = -111.9268

    # actual payload heading in degrees
    payload = 88
    declination_angle = declination(latitude, longitude)
    payload_heading = int(payload + declination_angle)
    # actual camera pitch in degrees
    # 0 is horizontal
    # +76 is maximum
    # -28 is minimum
    camera_angle = 0

    # date format: '2024-03-12 12:00:00'
    date = datetime.datetime.now()
    zenith_angle, azimuth_angle, compass_direction = sun_angle_and_direction(latitude, longitude, date)
    yaw, pitch = movement_needed(payload_heading, azimuth_angle, zenith_angle)


    # print out the given information
    # not to be used in actual operation
    print("Date", date)
    print("Latitude:", latitude)
    print("Longitude:", longitude)
    print("Sun's zenith angle:", round(zenith_angle, 2), "degrees")
    print("Sun's azimuth angle:", round(azimuth_angle, 2), "degrees")
    print()
    print("Payload's heading", payload_heading, "degrees")
    print("Camera's angle", camera_angle, "degrees")
    print("Yaw needed", yaw, "degrees")
    print("Pitch needed", pitch, "degrees")
