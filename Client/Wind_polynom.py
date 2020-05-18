import math
import matplotlib.pyplot as plt
import numpy as np

type_turbine = 'WES5'
wind_speed = [2, 2, 3, 4, 5, 6, 7, 8, 8.5, 9, 10]

WIND_PARAMETERS = {

    'WES5': {'P_rated': 2500, 'V_rated': 8.5, 'height': 12, 'cut_inspeed': 3, 'cut_outspeed': 20},
    'Aria libellula 55+': {'P_rated': 57000, 'V_rated': 11, 'height': 19, 'cut_inspeed': 3, 'cut_outspeed': 25},
    'Turbine3': {'P_rated': 2500, 'V_rated': 8.5, 'height': 12, 'cut_inspeed': 3, 'cut_outspeed': 20},
    'Turbine4': {'P_rated': 2500, 'V_rated': 8.5, 'height': 12, 'cut_inspeed': 3, 'cut_outspeed': 20},
}

windturbine_params = WIND_PARAMETERS[type_turbine]


def power_calc_wind(wind_speed, **windturbine_params):
    a = windturbine_params['P_rated'] / (windturbine_params['V_rated'] ** 3 - windturbine_params['cut_inspeed'] ** 3)

    b = (windturbine_params['V_rated'] ** 3) / (windturbine_params['V_rated'] ** 3 - windturbine_params['cut_inspeed'] ** 3)
    wind_speed = np.array(wind_speed)
    wind_power = a * (wind_speed ** 3) - (b * windturbine_params['P_rated'])

    wind_power = wind_speed**3-windturbine_params['cut_inspeed'] ** 3
    wind_power = wind_power * windturbine_params['P_rated']/(windturbine_params['V_rated'] ** 3 - windturbine_params['cut_inspeed'] ** 3)
    for x in range(0, len(wind_speed)):
        if wind_speed[x]<windturbine_params['cut_inspeed'] or wind_speed[x]>windturbine_params['cut_outspeed']:
            wind_power[x] = 0

    for x in range(0, len(wind_speed)):
       if wind_power[x]>windturbine_params['P_rated']:
           wind_power[x] = windturbine_params['P_rated']

    return wind_power.tolist()


windpower = power_calc_wind(wind_speed, **windturbine_params)
print(windpower)
plt.plot(windpower)
plt.show()
