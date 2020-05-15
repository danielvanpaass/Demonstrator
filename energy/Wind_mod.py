"An implementation of a wind energy model for a wind turbine"
import

wind_params = WINDTURBINE_MODEL_PARAMETERS = {

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
def power_calc_wind(wind_speed, **windturbine_params, air_density):

    efficiency =

    area =

    wind_power =

    p_out =
    return p_out
