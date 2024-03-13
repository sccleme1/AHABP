from datetime import datetime
from pyorbital import astronomy
import math

def get_compass_direction(angle):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(angle / (360. / len(directions))) % len(directions)
    return directions[index]

def sun_angle_and_direction(latitude, longitude, date_time_str):
    # Create a datetime object from the input string
    date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

    # Get the Sun's zenith angle at the specified date and time
    zenith_angle = astronomy.sun_zenith_angle(date_time, latitude, longitude)

    # Get the Sun's position at the specified date and time
    sun_position = astronomy.solar_position(date_time, latitude, longitude)

    # Calculate the azimuth angle (compass heading) of the Sun
    azimuth_angle = sun_position[0]
    
    # Convert azimuth angle to degrees and ensure it's within [0, 360)
    azimuth_angle_degrees = math.degrees(azimuth_angle) % 360

    # Get compass direction from azimuth angle
    compass_direction = get_compass_direction(azimuth_angle_degrees)

    return zenith_angle, azimuth_angle_degrees, compass_direction

if __name__ == "__main__":
    # Example usage
    latitude = 37.7749  # Example latitude (San Francisco)
    longitude = -122.4194  # Example longitude (San Francisco)
    date_time_str = '2024-03-12 12:00:00'  # Example date and time

    zenith_angle, azimuth_angle, compass_direction = sun_angle_and_direction(latitude, longitude, date_time_str)
    print("Sun's zenith angle:", zenith_angle, "degrees")
    print("Sun's azimuth angle:", azimuth_angle, "degrees")
    print("Sun's compass direction:", compass_direction)
