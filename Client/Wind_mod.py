"An implementation of a wind energy model for a wind turbine"
import math
import matplotlib.pyplot as plt
import numpy as np

type_turbine = 'WES5'
wind = [2, 2, 3, 15, 18, 4, 19, 21, 18, 16]
temp = [2, 5, 8, 12, 15, 17, 20, 22, 18, 10]

WIND_PARAMETERS = {

    'WES5': {'diameter': 5, 'height': 12, 'cut_inspeed': 3, 'cut_outspeed': 20},
    'Turbine2': {'diameter': 5, 'height': 12, 'cut_inspeed': 3, 'cut_outspeed': 20},
    'Turbine3': {'diameter': 5, 'height': 12, 'cut_inspeed': 3, 'cut_outspeed': 20},
    'Turbine4': {'diameter': 5, 'height': 12, 'cut_inspeed': 3, 'cut_outspeed': 20},
}

windturbine_params = WIND_PARAMETERS[type_turbine]


# P = 0.5 * rho * A * v^3 * Coefficient power
# rho = pressure / (gas_coefficient * temperature)
# lambda = v_d/v_u, blade tip speed /  wind speed
# blade tip speed = angular speed turbine * Diameter/2 / wind speed
# Coefficient power = (1 + lambda) * (1 - (lambda)^2)/2, max = 0.59, lambda = tsr
def power_calc_wind(wind_speed, temperature, **windturbine_params):
    # angular velocity of turbine is related to tip speed ratio to determine efficiency
    omega_turbine = wind_speed

    blade_tip_speed = (omega_turbine * windturbine_params['diameter'] / 2) / wind_speed

    tsr = blade_tip_speed / wind_speed

    # R_g (gas constant dry air = 287.058), pressure at sea level
    pressure = 101325
    rho = pressure / (287.058 * (temperature + 273.15))

    efficiency = ((1 + tsr) * (1 - (tsr ** 2)) / 2)

    area = ((windturbine_params['diameter']) ** 2 / 4) * math.pi

    wind_power = 0.5 * rho * area * wind_speed ** 3 * efficiency

    return wind_power, efficiency


#bln = (wind >= windturbine_params['cut_inspeed']).any() and (wind <= windturbine_params['cut_outspeed']).any()


if windturbine_params['cut_inspeed'] <= wind <= windturbine_params['cut_outspeed']:
     windpower, c = power_calc_wind(wind, temp, **windturbine_params)
else:
     windpower = 0


print(windpower)
plt.plot(windpower)
plt.show()
