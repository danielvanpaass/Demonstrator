"Wind model modelled by cubic function based on data sheet values"
import matplotlib.pyplot as plt
import numpy as np

WIND_PARAMETERS = {
    #'WES5': {'P_rated': 2500, 'V_rated': 8.5, 'height': 12, 'cut_inspeed': 3.0, 'cut_outspeed': 20, 'diameter': 5},
    'Aria55+': {'P_rated': 57000, 'V_rated': 11, 'height': 19, 'cut_inspeed': 3.0, 'cut_outspeed': 25, 'diameter': 19},
    'Hummer60': {'P_rated': 60000, 'V_rated': 7.5, 'height': 12, 'cut_inspeed': 2.5, 'cut_outspeed': 20,
                 'diameter': 25},
    'Aeolos10': {'P_rated': 10000, 'V_rated': 11.0, 'height': 6, 'cut_inspeed': 2.5, 'cut_outspeed': 52.5,
                 'diameter': 5.5},
    'Ades60': {'P_rated': 60000, 'V_rated': 8.0, 'height': 26.5, 'cut_inspeed': 3.5, 'cut_outspeed': 20,
               'diameter': 29},
    'Aria60': {'P_rated': 60000, 'V_rated': 11.0, 'height': 19, 'cut_inspeed': 3.0, 'cut_outspeed': 25, 'diameter': 19},
}

#calculated wind power in KW
def power_calc_wind(wind_speed, turbine_type):
    selected_turbine = WIND_PARAMETERS[turbine_type]

    wind_speed = np.array(wind_speed)

    winddelta = wind_speed ** 3 - selected_turbine['cut_inspeed'] ** 3

    wind_power = winddelta * selected_turbine['P_rated'] / (
                selected_turbine['V_rated'] ** 3 - selected_turbine['cut_inspeed'] ** 3)

    # power losses connection to bus and step-up voltage
    p_open = 200
    v_grid = 400
    resistance_c = 0.11
    resistance_load = 2.4
    p_load = (((wind_power - p_open) / v_grid) ** 2) * resistance_load
    p_wt = wind_power - p_open - p_load
    p_losses = wind_power - p_wt + (p_wt ** 2 * resistance_c / (v_grid ** 2))

    for x in range(0, len(wind_speed)):
        if wind_speed[x] < selected_turbine['cut_inspeed'] or wind_speed[x] > selected_turbine['cut_outspeed']:
            wind_power[x] = 0
            p_losses[x] = 0

    for x in range(0, len(wind_speed)):
        if wind_power[x] > selected_turbine['P_rated']:
            wind_power[x] = selected_turbine['P_rated']

    # power output
    p_out_wind = wind_power/1000
    return p_out_wind
