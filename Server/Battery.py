import numpy as np
from math import sqrt

N_EV = 1
EV_eff = 0.92
EV_P_max = 80 * N_EV
EV_E_max = 30 * sqrt(EV_eff) * N_EV
EV_E_min = 0.5 * EV_E_max
EV_E_commute = 8 * N_EV  # round trip for all car in kwh
EV_E_current = 0.6 * EV_E_max  # initial conditions
H_eff = 0.7
H_P_max = 100
H_E_max = 300 * sqrt(H_eff)
H_E_current = 0.6 * H_E_max


def power_battery(powers):
    if 'power_load' in powers:
        power_load = np.array(powers['power_load'])
    else:
        return "no_load"
    power_source = np.zeros((len(power_load),), dtype=int)
    if 'power_solar' in powers:
        power_source = power_source + np.array(powers['power_solar'])
    elif 'power_wind' in powers:
        power_source = power_source + np.array(powers['power_wind'])
    else:
        return 'no sources'
    PEV_out = np.zeros((len(power_load),), dtype=int)
    PH_out = np.zeros((len(power_load),), dtype=int)
    Pgrid_out = np.zeros((len(power_load),), dtype=int)
    wknd_factor = 0.8
    weekday_factor = 0.4
    night_factor = 1

    EV_P_max_wknd = EV_P_max * wknd_factor
    EV_E_max_wknd = EV_E_max * wknd_factor
    EV_E_min_wknd = EV_E_min * wknd_factor

    EV_P_max_weekday = EV_P_max * weekday_factor
    EV_E_max_weekday = EV_E_max * weekday_factor
    EV_E_min_weekday = EV_E_min * weekday_factor

    EV_P_max_night = EV_P_max * night_factor
    EV_E_max_night = EV_E_max * night_factor
    EV_E_min_night = EV_E_min * night_factor

    for x in range(0, len(power_load)):
        Pexcess = power_source[x] - power_load[x]
        global H_E_current, EV_E_current
        H_E_left = H_E_max - H_E_current
        H_E_over = H_E_current
        day = x // 24
        day_of_week = day % 7
        hour_of_day = x % 24
        if day_of_week > 4:  # so in the weekend
            if 9 < hour_of_day < 20:
                if hour_of_day == 10:
                    EV_E_returning_cars = (EV_E_current - EV_E_commute)*(1 - wknd_factor)  # calculate how much energy the departed cars will have upon return
                    EV_E_current = EV_E_current * wknd_factor
                EV_E_left = EV_E_max_wknd - EV_E_current
                EV_E_over = EV_E_current - EV_E_min_wknd
                Pgrid, PH, PEV = excesspowerflow(Pexcess, EV_P_max_wknd, EV_E_left, EV_E_over, H_E_left, H_E_over)
                EV_E_current = EV_E_current - PEV
                H_E_current = H_E_current - PH
                PEV_out[x] = PEV
                PH_out[x] = PH
                Pgrid_out[x] = Pgrid
                if hour_of_day == 19:  # add the returning cars to current EV
                    EV_E_current = EV_E_current + EV_E_returning_cars
            else:  # so at night
                if hour_of_day == 20:
                    EV_E_current = EV_E_current * night_factor
                EV_E_left = EV_E_max_night - EV_E_current
                EV_E_over = EV_E_current - EV_E_min_night
                Pgrid, PH, PEV = excesspowerflow(Pexcess, EV_P_max_night, EV_E_left, EV_E_over, H_E_left, H_E_over)
                EV_E_current = EV_E_current - PEV
                H_E_current = H_E_current - PH
                PEV_out[x] = PEV
                PH_out[x] = PH
                Pgrid_out[x] = Pgrid
        if day_of_week < 5:  # on workdays
            if 7 < hour_of_day < 19:
                if hour_of_day == 8:
                    EV_E_returning_cars = (EV_E_current - EV_E_commute)*(1 - weekday_factor)  # calculate how much energy the departed cars will have upon return
                    EV_E_current = EV_E_current * weekday_factor
                EV_E_left = EV_E_max_weekday - EV_E_current
                EV_E_over = EV_E_current - EV_E_min_weekday
                Pgrid, PH, PEV = excesspowerflow(Pexcess, EV_P_max_weekday, EV_E_left, EV_E_over, H_E_left, H_E_over)
                EV_E_current = EV_E_current - PEV
                H_E_current = H_E_current - PH
                PEV_out[x] = PEV
                PH_out[x] = PH
                Pgrid_out[x] = Pgrid
                if hour_of_day == 18:  # add the returning cars to current EV
                    EV_E_current = EV_E_current + EV_E_returning_cars
            else:  # so at night
                if hour_of_day == 19 or x == 0:
                    EV_E_current = EV_E_current * night_factor
                EV_E_left = EV_E_max_night - EV_E_current
                EV_E_over = EV_E_current - EV_E_min_night
                Pgrid, PH, PEV = excesspowerflow(Pexcess, EV_P_max_night, EV_E_left, EV_E_over, H_E_left, H_E_over)
                EV_E_current = EV_E_current - PEV
                H_E_current = H_E_current - PH
                PEV_out[x] = PEV
                PH_out[x] = PH
                Pgrid_out[x] = Pgrid
    return Pgrid_out, PH_out, PEV_out


def excesspowerflow(Pexcess, EV_P_max, EV_E_left, EV_E_over, H_E_left, H_E_over):
    Pgrid = PH = PEV = 0
    if Pexcess > 0:  # this means the batteries will have an incoming power flow
        enough_power = Pexcess < EV_P_max
        enough_energy = Pexcess < EV_E_left
        if enough_energy and enough_power:
            PEV = -Pexcess
        elif enough_energy and not enough_power:
            PEV = - EV_P_max
            Pexcess = Pexcess - EV_P_max
            enough_power = Pexcess < H_P_max
            enough_energy = Pexcess < H_E_left
            if enough_power and enough_energy:
                PH = -Pexcess
            elif enough_energy and not enough_power:
                Pgrid = H_P_max - Pexcess
                PH = -H_P_max
            else:
                Pgrid = -Pexcess
        else:  # EV doesnt have enough energy so start looking at hydrogen
            enough_power = Pexcess < H_P_max
            enough_energy = Pexcess < H_E_left
            if enough_power and enough_energy:
                PH = -Pexcess
            elif enough_energy and not enough_power:
                Pgrid = H_P_max - Pexcess
                PH = -H_P_max
            else:
                Pgrid = -Pexcess
        PH * H_eff  # the efficiency conversion sqrt(eff) is applied twice at the conversion to storage
        PEV * EV_eff
    else:  # if Pexcess is negative or 0, so the batteries are discharging
        Pexcess = abs(Pexcess)
        enough_power = Pexcess < EV_P_max
        enough_energy = Pexcess < EV_E_over
        if enough_energy and enough_power:
            PEV = Pexcess  # this creates positive EV power flow so it's extracting power from the EV
        elif enough_energy and not enough_power:
            PEV = EV_P_max
            Pexcess = Pexcess - EV_P_max
            enough_power = Pexcess < H_P_max
            enough_energy = Pexcess < H_E_over
            if enough_power and enough_energy:
                PH = Pexcess
            elif enough_energy and not enough_power:
                Pgrid = Pexcess - H_P_max
                PH = H_P_max
            else:
                Pgrid = Pexcess
        else:  # EV doesnt have enough energy so start looking at hydrogen
            enough_power = Pexcess < H_P_max
            enough_energy = Pexcess < H_E_over
            if enough_power and enough_energy:
                PH = Pexcess
            elif enough_energy and not enough_power:
                Pgrid = Pexcess - H_P_max
                PH = H_P_max
            else:
                Pgrid = Pexcess
    return Pgrid, PH, PEV


powers = {'power_load': [4, 6, 8, 5, 7, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'power_solar': [3, 6, 3, 6, 7, 7, 0,0, 0, 0, 0, 0, -120, 0, 0, 0, 0, 0, 0, 0, -2, 2]}
power_battery(powers)
