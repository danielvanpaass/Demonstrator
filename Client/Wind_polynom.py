"Wind model modelled by cubic function based on data sheet values"
import matplotlib.pyplot as plt
import numpy as np

type_turbine = 'WES5'
wind = [2, 2, 3, 4, 5, 6, 7, 8, 8.8, 9, 21]

WIND_PARAMETERS = {
    'WES5': {'P_rated': 2500, 'V_rated': 8.5, 'height': 12, 'cut_inspeed': 3.0, 'cut_outspeed': 20, 'diameter': 5},
    'Aria55+': {'P_rated': 57000, 'V_rated': 11, 'height': 19, 'cut_inspeed': 3.0, 'cut_outspeed': 25, 'diameter': 5},
    'Hummer60': {'P_rated': 60000, 'V_rated': 7.5, 'height': 12, 'cut_inspeed': 2.5, 'cut_outspeed': 20, 'diameter': 5},
    'Aeolos10': {'P_rated': 10000, 'V_rated': 11.0, 'height': 6, 'cut_inspeed': 2.5, 'cut_outspeed': 52.5, 'diameter': 5},
    'Ades60': {'P_rated': 60000, 'V_rated': 8.0, 'height': 26.5, 'cut_inspeed': 3.5, 'cut_outspeed': 20, 'diameter': 5},
    'Aria60': {'P_rated': 60000, 'V_rated': 11.0, 'height': 19, 'cut_inspeed': 3.0, 'cut_outspeed': 25, 'diameter': 5},
}

windturbine_parameters = WIND_PARAMETERS[type_turbine]


def power_calc_wind(wind_speed, **windturbine_params):
    wind_speed = np.array(wind_speed)

    winddelta = wind_speed ** 3 - windturbine_params['cut_inspeed'] ** 3

    wind_power = winddelta * windturbine_params['P_rated'] / (windturbine_params['V_rated'] ** 3 - windturbine_params['cut_inspeed'] ** 3)

    for x in range(0, len(wind_speed)):
        if wind_speed[x]<windturbine_params['cut_inspeed'] or wind_speed[x]>windturbine_params['cut_outspeed']:
            wind_power[x] = 0

    for x in range(0, len(wind_speed)):
       if wind_power[x]>windturbine_params['P_rated']:
           wind_power[x] = windturbine_params['P_rated']

    # Efficiency losses due to converters and generators
    efficiency = 0.8

    # Output power delivered to grid has losses and multiplied times area
    p_out_wind = (windturbine_params['diameter'] ** 2) / 4 * wind_power * efficiency
    return p_out_wind.tolist()


windpower = power_calc_wind(wind, **windturbine_parameters)
print(windpower)
plt.plot(windpower)
plt.show()
