"""An implementation of a solar energy model"""
# size, angle(panel), irradiance, efficiency, temperature reliance
import numpy as np

# Datasheet imported values
PV_PARAMETERS = {
    'RSM72-6-360M': {'length': 1.956, 'width': 0.992, 'efficiency': 0.186, 't_coefficient': -0.39},
    'HIT-N240SE10': {'length': 1.580, 'width': 0.798, 'efficiency': 0.19, 't_coefficient': -0.30},
    'Type3': {'length': 2500, 'width': 8.5, 'efficiency': 12, 't_coefficient': 3.0},
    'Type4': {'length': 2500, 'width': 8.5, 'efficiency': 12, 't_coefficient': 3.0},
}


# Power calculation with ambient temp as operating temp
def power_calc_solar(irradiance, temperature, pv_type):
    selectedpv = PV_PARAMETERS[pv_type]
    p_nom = selectedpv['length'] * selectedpv['width'] * selectedpv['efficiency'] * irradiance
    p_out = (((selectedpv['t_coefficient'] * (temperature - 25)) / 100) * p_nom) + p_nom
    return p_out

