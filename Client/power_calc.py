import json
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
# get load
with open('load.txt') as json_file:
    load = json.load(json_file)
load_saving = np.array(load['load_saving'])
load_average = np.array(load['load_average'])

"""Power calculation solar panel with ambient temp as operating temp"""


def power_calc_solar(length, width, efficiency, coefficient, irradiance, temperature):
    p_nom = length * width * efficiency * irradiance
    p_out = (((coefficient * (temperature - 25)) / 100) * p_nom) + p_nom
    return p_out


# Datasheet imported values
length, width, efficiency, coefficient = 1.956, 0.992, 0.186, -0.39

# calculate power per solar panel for each tilt
tcell = pvlib.temperature.sapm_cell(global_ir_30, temp, wind, **temp_params)
solpower30 = power_calc_solar(length, width, efficiency, coefficient, global_ir_30, tcell)
tcell = pvlib.temperature.sapm_cell(global_ir_35, temp, wind, **temp_params)
solpower35 = power_calc_solar(length, width, efficiency, coefficient, global_ir_35, tcell)
tcell = pvlib.temperature.sapm_cell(global_ir_40, temp, wind, **temp_params)
solpower40 = power_calc_solar(length, width, efficiency, coefficient, global_ir_40, tcell)

"""Main function to be called in this file, for total power out in a year per hour"""


def power_out_solar(N_panels, tilt_panel, N_load, type_load):
    data = {}  # empty dictionary
    if tilt_panel == 30:
        solpower = solpower30
    elif tilt_panel == 35:
        solpower = solpower35
    elif tilt_panel == 40:
        solpower = solpower40
    else:
        raise ValueError('tilt not defined')
    tot_solpower = solpower * N_panels
    tot_solpower = np.around(tot_solpower.astype(np.float), 3)  # rounding for reducing the message size
    if type_load == "saving":
        load = load_saving
    elif type_load == "average":
        load = load_average
    else:
        raise ValueError('load_type not defined')
    tot_load = load * N_load
    tot_load = np.around(tot_load.astype(np.float), 3)
    data.update({'power_solar': tot_solpower.tolist()})
    data.update({'power_load': tot_load.tolist()})

    return json.dumps(data)


if __name__ == '__main__':
    print(power_out_solar(2, 30, 3, "saving"))
    # print(power_out_solar(2, 40))
