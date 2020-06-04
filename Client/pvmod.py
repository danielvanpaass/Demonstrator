"""An implementation of a solar energy model"""
# size, angle(panel), irradiance, efficiency, temperature reliance
import numpy as np

# Datasheet imported values
PV_PARAMETERS = {
    'RSM72-6-360M': {'length': 1.956, 'width': 0.992, 'efficiency': 0.186, 't_coefficient': -0.39},
    'HIT-N245SE10': {'length': 1.580, 'width': 0.798, 'efficiency': 0.194, 't_coefficient': -0.258},
    'JAP60S01-290/SC': {'length': 1.689, 'width': 0.996, 'efficiency': 0.171, 't_coefficient': -0.37},
}


# Power calculation with ambient temp as operating temp in KW
def power_calc_solar(irradiance, temperature, pv_type):
    selectedpv = PV_PARAMETERS[pv_type]
    p_nom = selectedpv['length'] * selectedpv['width'] * selectedpv['efficiency'] * irradiance
    p_out = (((selectedpv['t_coefficient'] * (temperature - 25)) / 100) * p_nom) + p_nom
    return p_out*0.961

