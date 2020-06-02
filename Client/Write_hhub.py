from time import sleep
import numpy
from Client import hhub


def actuator_hhub(hour, powers, on):
    if on:                                          # turn on actuator signal
        if 'power_solar' in powers:
            power_min = min(powers)
            power_max = max(powers)
            for x in range(hour, len(powers)):
                power = powers[x]
                hhub.setModel(power, hhub.Model.SOLARPV, power_min, power_max)
                sleep(1)
        if 'power_wind' in powers:
            power_min = min(powers)
            power_max = max(powers)
            for x in range(hour, len(powers)):
                power = powers[x]
                hhub.setModel(power, hhub.Model.WINDTURBINE, power_min, power_max)
                sleep(1)
        if 'power_load' in powers:
            power_min = min(powers)
            power_max = max(powers)
            for x in range(hour, len(powers)):
                power = powers[x]
                hhub.setModel(power, hhub.Model.HOUSEHOLD, power_min, power_max)
                sleep(1)


def sensor_hhub(hour, powers, on):
    if on:
        if hour:
            if 'power_solar' in powers:
                power_min = min(powers)
                power_max = max(powers)
                for x in range(hour, len(powers)):
                    power_of_hour = hhub.getModel(hhub.Model.SOLARPV, power_min, power_max)
                    new_power = powers.insert(hour, power_of_hour)
                    sleep(1)
            if 'power_wind' in powers:
                power_min = min(powers)
                power_max = max(powers)
                for x in range(hour, len(powers)):
                    power_of_hour = hhub.getModel(hhub.Model.WINDTURBINE, power_min, power_max)
                    new_power = powers.insert(hour, power_of_hour)
                    sleep(1)
            if 'power_load' in powers:
                power_min = min(powers)
                power_max = max(powers)
                for x in range(hour, len(powers)):
                    power_of_hour = hhub.getModel(hhub.Model.HOUSEHOLD, power_min, power_max)
                    new_power = powers.insert(hour, power_of_hour)
                    sleep(1)
    return new_power




