from pysolar.solar import *
import datetime

# Tempe, AZ
latitude = 33.427204
longitude = -111.939896

date = datetime.datetime(2024, 4, 8, 13, 9, 1, 130320, tzinfo=datetime.timezone.utc)
print("Date", date)
print("Angle between Sun and tangent to Earth:", get_altitude(latitude, longitude, date), "deg")
print("Azimuth between Sun and tangent to Earth:", get_azimuth(latitude, longitude, date), "deg")
