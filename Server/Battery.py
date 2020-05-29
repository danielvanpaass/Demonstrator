import numpy as np
from math import sqrt

N_EV = 100
EV_eff = 92
EV_P_max_global = 80 * N_EV
EV_E_max_global = 30 * sqrt(EV_eff) *N_EV
EV_E_min_global = 0.5 * EV_E_max_global
EV_E_commute_global = 8 * N_EV #round trip for 1 car in kwh
EV_E_current_global = 0.6 * EV_E_max_global
H_eff = 0.7
H_P_max = 100
H_E_max = 300 * sqrt(H_eff)
H_E_current = 0.6 * H_E_max


def power_battery(powers):
    power_load = np.array(powers['power_load'])
    power_source = np.array(powers['power_solar']) + np.array(powers['power_wind'])
    PEV_out = np.zeros((8760,), dtype=int)
    PH_out = np.zeros((8760,), dtype=int)
    Pgrid_out = np.zeros((8760,), dtype=int)


    for x in range(0, len(power_load)):
        day_of_week = x % 7
        hour_of_day = x % 24
        if day_of_week > 4: #so in the weekend
            if 9<hour_of_day<20:
                cars_leaving = 0.2 #percentage

        cars_staying = 1-cars_leaving
        EV_E_homecoming = (EV_E_current_global - EV_E_commute_global)*cars_leaving#starting energy level minus commute energy take for all cars, times the % of cars leaving
        EV_E_current = EV_E_current_global * cars_staying
        EV_P_max = EV_P_max_global * cars_staying # max EV power is lower because less cars
        EV_E_max = EV_E_max_global * cars_staying
        EV_E_min = EV_E_min_global * cars_staying
        EV_E_left = EV_E_max - EV_E_current  # How much energy can be filled in the EV
        H_E_left = H_E_max - H_E_current
        EV_E_over = EV_E_current - EV_E_min  # How much energy can still be extracted from the EV
        H_E_over = H_E_current
        Pexcess = power_source[x]-power_load[x]
        Pgrid, PH, PEV = excesspowerflow(Pexcess)
        Pgrid_out[x] = Pgrid, PH_out[x] = PH, PEV_out[x] = PEV
        global EV_E_current_global, H_E_current
        EV_E_current_global = EV_E_current - PEV
        H_E_current = H_E_current - PH
        if hour_of_day == 19:#when the cars return home
            EV_E_current_global = EV_E_current_global + EV_E_homecoming



    def excesspowerflow(Pexcess):
        Pgrid = PH = PEV = 0
        if Pexcess > 0:  # this means the batteries will have an incoming power flow
            enough_power = Pexcess < EV_P_max
            enough_energy = Pexcess < EV_E_left
            if enough_energy and enough_power:
                PEV = -Pexcess
            if enough_energy and not enough_power:
                PEV = - EV_P_max
                Pexcess = Pexcess - EV_P_max
                enough_power = Pexcess < H_P_max
                enough_energy = Pexcess < H_E_left
                if enough_power and enough_energy:
                    PH = -Pexcess
                if enough_energy and not enough_power:
                    Pgrid = H_P_max - Pexcess
                    PH = -H_P_max
                else:
                    Pgrid = -Pexcess
            else:  # EV doesnt have enough energy so start looking at hydrogen
                enough_power = Pexcess < H_P_max
                enough_energy = Pexcess < H_E_left
                if enough_power and enough_energy:
                    PH = -Pexcess
                if enough_energy and not enough_power:
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
            if enough_energy and not enough_power:
                PEV = EV_P_max
                Pexcess = Pexcess - EV_P_max
                enough_power = Pexcess < H_P_max
                enough_energy = Pexcess < H_E_over
                if enough_power and enough_energy:
                    PH = Pexcess
                if enough_energy and not enough_power:
                    Pgrid = Pexcess - H_P_max
                    PH = H_P_max
                else:
                    Pgrid = Pexcess
            else:  # EV doesnt have enough energy so start looking at hydrogen
                enough_power = Pexcess < H_P_max
                enough_energy = Pexcess < H_E_over
                if enough_power and enough_energy:
                    PH = Pexcess
                if enough_energy and not enough_power:
                    Pgrid = Pexcess - H_P_max
                    PH = H_P_max
                else:
                    Pgrid = Pexcess
        return Pgrid, PH, PEV
