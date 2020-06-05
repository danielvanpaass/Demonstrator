from time import sleep
from Client import hhub


def actuator_hhub(hour, powers, wind, solar, load, hydrogen, EV):
    if solar:
        power = powers['power_solar']
        power_min = min(power) #the maxes will be calculated every time, this could be done once every new power list
        power_max = max(power)
        power = power[hour]
        hhub.setModel(power, hhub.Model.SOLARPV, power_min, power_max)
    if wind:
        power = powers['power_wind']
        power_min = min(power)
        power_max = max(power)
        power = power[hour]
        hhub.setModel(power, hhub.Model.WINDTURBINE, power_min, power_max)
    if load:
        power = powers['power_load']
        power_min = min(power)
        power_max = max(power)
        power = power[hour]
        hhub.setModel(power, hhub.Model.HOUSEHOLD, power_min, power_max)
    if hydrogen:
        power = powers['power_hydrogen']
        power_min = min(power)
        power_max = max(power)
        power = power[hour]
        hhub.setModel(power, hhub.Model.HOUSEHOLD, power_min, power_max)
    if EV:
        power = powers['power_load']
        power_min = min(power)
        power_max = max(power)
        power = power[hour]
        hhub.setModel(power, hhub.Model.HOUSEHOLD, power_min, power_max)


def sensor_hhub(hour, powers, wind, solar, load):
    data_out_rt = {}
    if solar:
        power = powers['power_solar']
        power_min = min(power)
        power_max = max(power)
        output = hhub.getModel(hhub.Model.SOLARPV, power_min, power_max)
        if output == -1:
            output =power[hour]
        data_out_rt.update({'solar_power': output})
        powers['power_solar'][hour]=output #this replaces the element within the list of the full year as well
    if wind:
        power = powers['power_wind']
        power_min = min(power)
        power_max = max(power)
        output = hhub.getModel(hhub.Model.WINDTURBINE, power_min, power_max)
        if output == -1:
            output =power[hour]
        data_out_rt.update({'wind_power': output})
        powers['power_wind'][hour]=output #this replaces the element within the list of the full year as well

    sleep(0.008)
    if load:
        power = powers['power_load']
        power_min = min(power)
        power_max = max(power)
        output = hhub.getModel(hhub.Model.HOUSEHOLD, power_min, power_max)
        if output == -1:
            output =power[hour]
        data_out_rt.update({'load_power': output})
        powers['power_load'][hour]=output #this replaces the element within the list of the full year as well
    data_out_rt.update({'hour_simul': hour})
    return data_out_rt, powers
