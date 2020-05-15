"An implementation of a wind energy model for a wind turbine"
import math

windturbine_params= WIND_PARAMETERS['WES5'] = {

        'WES5': {'diameter': 5, 'height': 12, 'cut_inspeed': 3, 'cut_outspeed':20},
        'Turbine2': {'diameter': 5, 'height': 12, 'cut_inspeed': 3, 'cut_outspeed':20},
        'Turbine3': {'diameter': 5, 'height': 12, 'cut_inspeed': 3, 'cut_outspeed':20},
        'Turbine4': {'diameter': 5, 'height': 12, 'cut_inspeed': 3, 'cut_outspeed':20},

}


# P = 0.5 * rho * A * v^3 * Coefficient power
# rho = pressure / (gas_coefficient * temperature)
# lambda = v_d/v_u, blade tip speed /  wind speed
# blade tip speed = angular speed turbine * Diameter/2 / wind speed
# Coefficient power = (1 + lambda) * (1 - (lambda)^2)/2, max = 0.59
def power_calc_wind(wind_speed, temperature, **windturbine_params):

    blade_tip_speed = (omega_turbine * **windturbine_params.diameter) / (wind_speed)

    lamda = blade_tip_speed / wind_speed

    # R_g (gasconstant), pressure is pressure at windturbine height
    rho = pressure / (R_g * temperature)

    efficiency = ((1 + lamda) * (1 - (lamda)^2))/2

    area = (**windturbine_params.diameter/4)*math.pi

    wind_power = 0.5 * rho * area * (wind_speed)^3 * efficiency

    p_out = wind_power
    return p_out


print(p_out)
