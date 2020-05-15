"An implementation of a wind energy model for a wind turbine"
import math

type = 'WES5'

windturbine_params= WIND_PARAMETERS[type] = {

        'WES5': {'diameter': 5, 'height': 12, 'cut_inspeed': 3, 'cut_outspeed':20},
        'Turbine2': {'diameter': 5, 'height': 12, 'cut_inspeed': 3, 'cut_outspeed':20},
        'Turbine3': {'diameter': 5, 'height': 12, 'cut_inspeed': 3, 'cut_outspeed':20},
        'Turbine4': {'diameter': 5, 'height': 12, 'cut_inspeed': 3, 'cut_outspeed':20},

}


# P = 0.5 * rho * A * v^3 * Coefficient power
# rho = pressure / (gas_coefficient * temperature)
# lambda = v_d/v_u, blade tip speed /  wind speed
# blade tip speed = angular speed turbine * Diameter/2 / wind speed
# Coefficient power = (1 + lambda) * (1 - (lambda)^2)/2, max = 0.59, lambda = tsr
def power_calc_wind(wind_speed, temperature, windturbine_params):
    # angular velocity of turbine is related to tip speed ratio to determine efficiency
    omega_turbine = 60 * wind_speed * tsr / (math.pi * windturbine_params.diameter)

    blade_tip_speed = (omega_turbine * windturbine_params.diameter) / wind_speed

    tsr = blade_tip_speed / wind_speed

    # R_g (gas constant), pressure is pressure at wind turbine height
    pressure = 760 * math.exp(−0.00012 * windturbine_params.height)
    rho = pressure / (R_g * temperature)

    efficiency = ((1 + tsr) * (1 - tsr ^ 2)) / 2

    area = ((windturbine_params.diameter)^2/4)*math.pi

    wind_power = 0.5 * rho * area * wind_speed^3 * efficiency

    if wind_speed < windturbine_params.cut_inspeed | wind_speed > windturbine_params.cut_outspeed:
        p_out = 0
    else:
        p_out = wind_power
    return p_out


print(p_out)
