import ephem
import datetime
from geomag import declination
import matplotlib.pyplot as plt


pi = 3.14159265358979323846
day = 24
month = 4
year = 2024

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
    
    if azimuth_angle > 360:
        azimuth_angle -= 360
    if azimuth_angle < 0:
        azimuth_angle += 360
        
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
    hours = []
    zeniths = []
    azimuths = []
    time = 0
    while time <= 23.95:
        hour = int(time)
        minute = int((time - hour) * 60)
        
        # Specify the year, month, day, hour, minute, and second
        date = datetime.datetime(year, month, day, hour, minute, 0)
        zenith_angle, azimuth_angle, compass_direction = sun_angle_and_direction(latitude, longitude, date)
        azimuths.append(azimuth_angle)
        zeniths.append(zenith_angle)
        hours.append(time)
        #print(f"time: {hour}:{minute}\tzenith: {zenith_angle}\tazimuth: {azimuth_angle}")
        time += 0.05

    now = datetime.datetime.now()
    zenith_angle_now, azimuth_angle_now, compass_direction = sun_angle_and_direction(latitude, longitude, now)
    hour_now = now.hour
    minute_now = now.minute
    time_now = round(hour_now + minute_now/60, 2)
    #print("Current:")
    #print(f"time: {hour_now}:{minute_now}\tzenith: {zenith_angle_now}\tazimuth: {azimuth_angle_now}")


    a_color = (0.777, 0.449, 0.063)
    z_color = (0.019, 0.494, 0.777)

    plt.figure(1)
    plt.plot(hours, zeniths, "--", color=z_color, label="Zenith")
    plt.plot(hours, azimuths, "--", color=a_color, label="Azimuth")
    plt.plot(time_now, zenith_angle_now, "bo")
    plt.plot(time_now, azimuth_angle_now, "ro")
    plt.annotate(f'({hour_now}:{minute_now}, {zenith_angle_now}°)', (time_now, zenith_angle_now), textcoords="offset points", xytext=(-25,25), ha='center')
    plt.annotate(f'({hour_now}:{minute_now}, {azimuth_angle_now}°)', (time_now, azimuth_angle_now), textcoords="offset points", xytext=(0,-35), ha='center')
    plt.legend()
    plt.xlabel("Time [hr]")
    plt.ylabel("Angle [°]")
    plt.title(f"Sun Zenith and Azimuth Angles\n{month}/{day}/{year}")
    plt.savefig(f"{day}-{month}-{year}_Azimuth_Zenith.png")
    plt.show()
    
