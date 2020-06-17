"Wind model modelled by cubic function based on data sheet values"
import matplotlib.pyplot as plt
import numpy as np

WIND_PARAMETERS = {
    # 'WES5': {'P_rated': 2500, 'V_rated': 8.5, 'height': 12, 'cut_inspeed': 3.0, 'cut_outspeed': 20, 'diameter': 5},
    'V90-2MW': {'P_rated': 2000000, 'V_rated': 13, 'height': 80, 'cut_inspeed': 4.0, 'cut_outspeed': 25,
                'diameter': 90},
    'Aria55+': {'P_rated': 57000, 'V_rated': 11, 'height': 19, 'cut_inspeed': 3.0, 'cut_outspeed': 25, 'diameter': 19},
    'Hummer60': {'P_rated': 60000, 'V_rated': 7.5, 'height': 12, 'cut_inspeed': 2.5, 'cut_outspeed': 20,
                 'diameter': 25},
    'Aeolos10': {'P_rated': 10000, 'V_rated': 11.0, 'height': 6, 'cut_inspeed': 2.5, 'cut_outspeed': 52.5,
                 'diameter': 5.5},
    'Ades60': {'P_rated': 60000, 'V_rated': 8.0, 'height': 26.5, 'cut_inspeed': 3.5, 'cut_outspeed': 20,
               'diameter': 29},
    'Aria60': {'P_rated': 60000, 'V_rated': 11.0, 'height': 19, 'cut_inspeed': 3.0, 'cut_outspeed': 25, 'diameter': 19},
}


# calculated wind power in KW
def power_calc_wind(wind_speed, turbine_type):
    selected_turbine = WIND_PARAMETERS[turbine_type]

    wind_speed = np.array(wind_speed)

    winddelta = wind_speed ** 3 - selected_turbine['cut_inspeed'] ** 3

    wind_power = winddelta * selected_turbine['P_rated'] / (
            selected_turbine['V_rated'] ** 3 - selected_turbine['cut_inspeed'] ** 3)

    for x in range(0, len(wind_speed)):
        if wind_speed[x] < selected_turbine['cut_inspeed'] or wind_speed[x] > selected_turbine['cut_outspeed']:
            wind_power[x] = 0

    for x in range(0, len(wind_speed)):
        if wind_power[x] > selected_turbine['P_rated']:
            wind_power[x] = selected_turbine['P_rated']

    # power output
    p_out_wind = wind_power / 1000
    return p_out_wind


turbine_type = 'Hummer60'
windspeed = np.arange(0, 25, 0.5)

powerwind = power_calc_wind(windspeed, turbine_type)
plt.plot(windspeed, powerwind)
plt.xlabel('Wind speed [m/s]')
plt.ylabel('Power [kW]')
plt.title('Power curve of Hummer60')
plt.annotate('V_rated',
             xy=(7.5, 60),
             xytext=(5.5, 64), arrowprops=dict(facecolor='black', shrink=0.05),
             horizontalalignment='right', verticalalignment='top'
             )
plt.annotate('V_cutin',
             xy=(2.5, 0),
             xytext=(2.5, 8), arrowprops=dict(facecolor='black', shrink=0.05),
             horizontalalignment='right',verticalalignment='bottom'
             )
plt.annotate('V_cutoff',
             xy=(20, 60),
             xytext=(19.5,65), arrowprops=dict(facecolor='black', shrink=0.05),
             horizontalalignment='right', verticalalignment='bottom'
             )
plt.ylim(-0.1, 70)
plt.xlim(-0.1, 22)
plt.savefig('Powercurvehummer60.png', bbox_inches='tight')
plt.show()
