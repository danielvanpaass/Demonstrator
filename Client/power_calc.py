import json
import numpy as np
import pvlib

try:
    from Client import windmod
except:
    import windmod
try:
    from Client import pvmod
except:
    import pvmod

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
# calculate temperature per solar panel for each tilt
tcell30 = pvlib.temperature.sapm_cell(global_ir_30, temp, wind, **temp_params)
tcell35 = pvlib.temperature.sapm_cell(global_ir_35, temp, wind, **temp_params)
tcell40 = pvlib.temperature.sapm_cell(global_ir_40, temp, wind, **temp_params)

"""Main function to be called in this file, for total power out in a year per hour"""


def power_out_wind(type_turbine):
    windpower = windmod.power_calc_wind(wind, type_turbine)
    windpower = np.around(windpower.astype(np.float), 3)
    data = {'power_wind': windpower.tolist()}
    return json.dumps(data)


def power_out_solar(N_panels, tilt_panel, type_pvpanel):
    if tilt_panel == 30:
        solpower = pvmod.power_calc_solar(global_ir_30, tcell30, type_pvpanel)
    elif tilt_panel == 35:
        solpower = pvmod.power_calc_solar(global_ir_35, tcell35, type_pvpanel)
    elif tilt_panel == 40:
        solpower = pvmod.power_calc_solar(global_ir_40, tcell40, type_pvpanel)
    else:
        raise ValueError('tilt not defined')
    tot_solpower = solpower * N_panels
    tot_solpower = np.around(tot_solpower.astype(np.float), 3)  # rounding for reducing the message size
    data = {'power_solar': tot_solpower.tolist()}
    return json.dumps(data)


def power_out_load(N_load, type_load):
    if type_load == "saving":
        load = load_saving
    elif type_load == "average":
        load = load_average
    else:
        raise ValueError('load_type not defined')
    tot_load = load * N_load
    tot_load = np.around(tot_load.astype(np.float), 3)
    data = {'power_load': tot_load.tolist()}

    return json.dumps(data)


if __name__ == '__main__':
    print(power_out(30, 30, 3, "saving", 'RSM72-6-360M', 'WES5'))
    # print(power_out(2, 40))
