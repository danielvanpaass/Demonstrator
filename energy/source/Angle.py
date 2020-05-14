#Angle to sun calculation, azimuth TEST
import pandas as pd
import math
import datetime
import numpy as np
import matplotlib.pyplot as plt
year = 2019
hour = pd.date_range(start=year, end='2020', freq='1h')

def solar_angle(latitude, longitude, year, hour):
    start_year = datetime.datetime(year, 1, 1, 0, 0, 0, 0)
    utc_datetime = start_year + datetime.timedelta(hours=hour)

    # Angular distance of the sun north or south of the earths equator
    # Determine the day of the year.
    day_of_year = utc_datetime.timetuple().tm_yday

    declination = 23.45 * math.sin((360 / 365.0) * (day_of_year - 81))

    angle_of_day = (day_of_year - 81) * (360 / 365)

    equation_of_time = (9.87 * math.sin(2 * angle_of_day)) - \
                       (7.53 * math.cos(angle_of_day)) - (1.5 * math.sin(angle_of_day))

    # True Solar Time
    solar_time = ((utc_datetime.hour * 60) + utc_datetime.minute +
                  (4 * longitude) + equation_of_time) / 60.0

    # Angle between the local longitude and longitude where the sun is at
    # higher altitude
    hour_angle = (15 * (12 - solar_time))

    # Altitude Position of the Sun in Radians
    altitude = math.asin(math.cos(latitude) * math.cos(declination) * math.cos(hour_angle) +
                         math.sin(latitude) * math.sin(declination))

    # Azimuth Position fo the sun in radians
    azimuth = math.asin(
              math.cos(declination) * math.sin(hour_angle) / math.cos(altitude))

    # I don't really know what this code does, it has been imported from
    # PySolar
    if (math.cos(hour_angle) >= (math.tan(declination) / math.tan(latitude))):
         altitude, azimuth
    else:
         altitude, 180 - azimuth
    return altitude, azimuth

latitude_deg = 52.0
longitude_deg = 4.3571

numhours = 8760


alt, azi = solar_angle(52.0, 4.3571, 2019, hour)
print("Azimuth angle:",azi)
print("Altitude angle", alt)
plt.plot(hour, azi)
plt.show()
