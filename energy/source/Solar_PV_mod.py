"""An implementation of a solar energy model"""
# size, angle(panel), irradiance, efficiency, temperature reliance
import time
import math
import datetime
import numpy as np
import matplotlib.pyplot as pl


# Power calculation with ambient temp as operating temp
def power_out(length, width, efficiency, coefficient, irradiance, temperature):
    p_nom = length * width * efficiency * irradiance
    p_out = (((coefficient * (temperature - 25)) / 100) * p_nom) + p_nom
    return p_out


# Datasheet imported values
lenght, width, efficiency, coefficient = 1.956, 0.992, 0.186, -0.39
# Internet imported values for NL
irradiance = np.array([1000, 1000, 1000, 1000])
temperature = np.array([27, 25, 26, 25])
timehour = np.array([0, 1, 2, 3])

power = power_out(lenght, width, efficiency, coefficient, irradiance, temperature)
