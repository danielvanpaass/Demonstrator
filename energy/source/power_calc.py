import json
import pandas as pd
import numpy as np
import pvlib

# choose good model params
temp_params = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

# get weather paramameters
with open('wind.txt') as json_file:
    wind = json.load(json_file)
wind = np.array(wind['wind'])
with open('solar30.txt') as json_file:
    solar30 = json.load(json_file)
global_ir_30 = np.array(solar30['irradiance_diffuse']) + np.array(solar30['irradiance_direct'])
with open('solar35.txt') as json_file:
    solar35 = json.load(json_file)
global_ir_35 = np.array(solar35['irradiance_diffuse']) + np.array(solar35['irradiance_direct'])
with open('solar40.txt') as json_file:
    solar40 = json.load(json_file)
global_ir_40 = np.array(solar40['irradiance_diffuse']) + np.array(solar40['irradiance_direct'])
temp = np.array(solar40['temp'])

"""Power calculation solar panel with ambient temp as operating temp"""


def power_calc_solar(length, width, efficiency, coefficient, irradiance, temperature):
    p_nom = length * width * efficiency * irradiance
    p_out = (((coefficient * (temperature - 25)) / 100) * p_nom) + p_nom
    return p_out


# Datasheet imported values
length, width, efficiency, coefficient = 1.956, 0.992, 0.186, -0.39

# calculate power per solar panel for each tilt
tcell = pvlib.temperature.sapm_cell(global_ir_30, temp, wind, **temp_params)
power30 = power_calc_solar(length, width, efficiency, coefficient, global_ir_30, tcell)
tcell = pvlib.temperature.sapm_cell(global_ir_35, temp, wind, **temp_params)
power35 = power_calc_solar(length, width, efficiency, coefficient, global_ir_35, tcell)
tcell = pvlib.temperature.sapm_cell(global_ir_40, temp, wind, **temp_params)
power40 = power_calc_solar(length, width, efficiency, coefficient, global_ir_40, tcell)

"""Main function to be called in this file, for total power out in a year per hour"""


def power_out_solar(N_panels, tilt_panel):
    data = {}  # empty dictionary
    if tilt_panel == 30:
        power = power30
    elif tilt_panel == 35:
        power = power35
    elif tilt_panel == 40:
        power = power40
    else:
        raise ValueError('tilt not defined')
    tot_power = power * N_panels
    tot_power = np.around(tot_power.astype(np.float), 3)  # rounding for reducing the message size
    data.update({'power': tot_power.tolist()})

    return json.dumps(data)


if __name__ == '__main__':
    print(power_out_solar(2, 30))
    print(power_out_solar(2, 40))
    #power_out_solar(1, 50)  # should throw exception
