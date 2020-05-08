#Angle to sun calculation, azimuth TEST
def solar_angle(latitude_deg, longitude_deg, year, hour):
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
                  (4 * longitude_deg) + equation_of_time) / 60.0

    # Angle between the local longitude and longitude where the sun is at
    # higher altitude
    hour_angle = (15 * (12 - solar_time))

    # Altitude Position of the Sun in Radians
    altitude = math.asin(math.cos(latitude_deg) * math.cos(declination) * math.cos(hour_angle) +
                         math.sin(latitude_deg) * math.sin(declination))

    # Azimuth Position fo the sun in radians
    azimuth_deg = math.asin(
        math.cos(declination) * math.sin(hour_angle) / math.cos(altitude))

    # I don't really know what this code does, it has been imported from
    # PySolar
    # if (math.cos(hour_angle_rad) >= (math.tan(declination_rad) / math.tan(latitude_rad))):
    #  return math.degrees(altitude_rad), math.degrees(azimuth_rad)
    # else:
    #   return math.degrees(altitude_rad), (180 - math.degrees(azimuth_rad))
    return azimuth_deg

latitude_deg = 52.0
longitude_deg = 4.3571

angle = solar_angle(52.0,4.3571,2020,720)
print("Azimuth angle:",angle)
