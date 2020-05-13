import json
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import pvlib

# choose good model params
temp_params = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

#get weather paramameters
with open('weather.txt') as json_file:
    weather = json.load(json_file)


"""Power calculation solar panel with ambient temp as operating temp"""


def power_calc(length, width, efficiency, coefficient, irradiance, temperature):
    p_nom = length * width * efficiency * irradiance
    p_out = (((coefficient * (temperature - 25)) / 100) * p_nom) + p_nom
    return p_out


# Datasheet imported values
length, width, efficiency, coefficient = 1.956, 0.992, 0.186, -0.39

# calculate power per solar panel
global_ir = np.array(weather['irradiance_diffuse']) + np.array(weather['irradiance_direct'])
temp = np.array(weather['temp'])
wind = np.array(weather['wind'])
tcell = pvlib.temperature.sapm_cell(global_ir, temp, wind, **temp_params)
power = power_calc(length, width, efficiency, coefficient, global_ir, tcell)
# timehour = np.arange(0, temp.size)

"""Main function to be called in this file, for total power out in a year per hour"""


def power_out_solar(N_panels):
    data = {}  # empty dictionary
    tot_power = power * N_panels
    tot_power = np.around(tot_power.astype(np.float), 3)  # rounding for reducing the message size
    data.update({'power': tot_power.tolist()})

    return json.dumps(data)

    # m_in=json.loads(m_decode) #decode json data
    # plt.plot(timehour[0:24], power[0:24])
    # plt.xlabel("Time (hr)")
    # plt.ylabel("Power (W)")
    # plt.show()
    #
