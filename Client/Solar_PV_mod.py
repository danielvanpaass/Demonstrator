"""An implementation of a solar energy model"""
# size, angle(panel), irradiance, efficiency, temperature reliance
import numpy as np

# Power calculation with ambient temp as operating temp
def power_out(irradiance, temperature, **pv_parameters):
    p_nom = pv_parameters['length'] * pv_parameters['width'] * pv_parameters['efficiency'] * irradiance
    p_out = (((pv_parameters['t_coefficient'] * (temperature - 25)) / 100) * p_nom) + p_nom
    return p_out


pv_type = 'HIT-N240SE10'

# Datasheet imported values
PVPANEL = {
    'RSM72-6-360M': {'length': 1.956, 'width': 0.992, 'efficiency': 0.186, 't_coefficient': -0.39},
    'HIT-N240SE10': {'length': 1.580, 'width': 0.798, 'efficiency': 0.19, 't_coefficient': -0.30},
    'Type3': {'length': 2500, 'width': 8.5, 'efficiency': 12, 't_coefficient': 3.0},
    'Type4': {'length': 2500, 'width': 8.5, 'efficiency': 12, 't_coefficient': 3.0},
}

pv_parameters = PVPANEL[pv_type]

# Internet imported values for NL
irradiance = np.array([1000, 1000, 1000, 1000])
temperature = np.array([27, 25, 26, 25])
timehour = np.array([0, 1, 2, 3])

power = power_out(**pv_parameters, irradiance, temperature)
