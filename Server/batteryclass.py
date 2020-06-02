import numpy as np
from math import sqrt

class Car:
    def __init__(self, SoC):
        self.SoC = SoC
        self.working = 0 #all cars home
        self.powerMax = 8 #takes roughly 4 hours to charge car fully with level 2 station
        self.energyMax = 30
        self.energyMin = 5 #enough for 1 more round trip to work
        self.currentEnergy = SoC*self.energyMax
    def needCharging(self, day, hour):
        pass
    def takePower(self, day, hour):
        pass
    def storePower(self, day, hour):
        pass
    def setWork(self, workStatus):
        self.working = workStatus
class HydrogenTank:
    def __init__(self, SoC):
        self.SoC = SoC
        self.powerMax = 100 #kwh
        self.energyMax = 300
        self.currentEnergy = SoC * self.energyMax

    def takePower(self):
        pass

    def storePower(self):
        pass




def power_battery(powers, N_EV):
    EV_eff = 0.92
    EV_P_max = 80 * N_EV
    EV_E_max = 30 * sqrt(EV_eff) * N_EV
    EV_E_min = 0.5 * EV_E_max
    EV_E_commute = 4 * N_EV  # round trip for all car in kwh, 30km
    EV_E_current = 0.6 * EV_E_max  # initial conditions
    H_eff = 0.7
    H_P_max = 100
    H_E_max = 300 * sqrt(H_eff)
    H_E_current = 0.6 * H_E_max

    power_load = np.array(powers['power_load'])
    power_source = np.zeros((len(power_load)))
    if 'power_solar' in powers:
        power_source = power_source + np.array(powers['power_solar'])
    if 'power_wind' in powers:
        power_source = power_source + np.array(powers['power_wind'])
    PEV_out = np.zeros((len(power_load),))
    PH_out = np.zeros((len(power_load),))
    Pgrid_out = np.zeros((len(power_load),))
    EV_SoC_out =np.zeros((len(power_load),))
    H_SoC_out = np.zeros((len(power_load),))
    Pexcess_out = np.zeros((len(power_load),))
    wknd_factor = 0.8
    weekday_factor = 0.3
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
        Pexcess_out[x]=Pexcess
        H_E_left = H_E_max - H_E_current
        H_E_over = H_E_current
        day = x // 24
        day_of_week = day % 7
        hour_of_day = x % 24
        H_SoC_out[x] = H_E_current/H_E_max
        if day_of_week > 4:  # so in the weekend
            if 9 < hour_of_day < 20:
                if hour_of_day == 10:
                    EV_E_returning_cars = (EV_E_current - EV_E_commute) * (
                            1 - wknd_factor)  # calculate how much energy the departed cars will have upon return
                    EV_E_current = EV_E_current * wknd_factor
                EV_SoC =EV_E_current/EV_E_max_wknd
                EV_E_left = EV_E_max_wknd - EV_E_current
                EV_E_over = EV_E_current - EV_E_min_wknd
                Pgrid, PH, PEV = excesspowerflow(Pexcess, EV_P_max_wknd, EV_E_left, EV_E_over, H_E_left, H_E_over,
                                                 H_P_max, H_eff, EV_eff, EV_E_commute)
                EV_E_current = EV_E_current - PEV
                H_E_current = H_E_current - PH
                PEV_out[x] = PEV
                PH_out[x] = PH
                Pgrid_out[x] = Pgrid
                EV_SoC_out[x] = EV_SoC
                if hour_of_day == 19:  # add the returning cars to current EV
                    EV_E_current = EV_E_current + EV_E_returning_cars
            else:  # so at night
                if hour_of_day == 20:
                    EV_E_current = EV_E_current * night_factor
                EV_SoC =  EV_E_current/EV_E_max_night
                EV_E_left = EV_E_max_night - EV_E_current
                EV_E_over = EV_E_current - EV_E_min_night
                Pgrid, PH, PEV = excesspowerflow(Pexcess, EV_P_max_night, EV_E_left, EV_E_over, H_E_left, H_E_over,
                                                 H_P_max, H_eff, EV_eff, EV_E_commute)
                EV_E_current = EV_E_current - PEV
                H_E_current = H_E_current - PH
                PEV_out[x] = PEV
                PH_out[x] = PH
                Pgrid_out[x] = Pgrid
                EV_SoC_out[x] = EV_SoC
        if day_of_week < 5:  # on workdays
            if 7 < hour_of_day < 19:
                if hour_of_day == 8:
                    EV_E_returning_cars = (EV_E_current - EV_E_commute) * (
                            1 - weekday_factor)  # calculate how much energy the departed cars will have upon return
                    EV_E_current = EV_E_current * weekday_factor
                EV_SoC = EV_E_current/EV_E_max_weekday
                EV_E_left = EV_E_max_weekday - EV_E_current
                EV_E_over = EV_E_current - EV_E_min_weekday
                Pgrid, PH, PEV = excesspowerflow(Pexcess, EV_P_max_weekday, EV_E_left, EV_E_over, H_E_left, H_E_over,
                                                 H_P_max, H_eff, EV_eff, EV_E_commute)
                EV_E_current = EV_E_current - PEV
                H_E_current = H_E_current - PH
                PEV_out[x] = PEV
                PH_out[x] = PH
                Pgrid_out[x] = Pgrid
                EV_SoC_out[x] = EV_SoC
                if hour_of_day == 18:  # add the returning cars to current EV
                    EV_E_current = EV_E_current + EV_E_returning_cars
            else:  # so at night
                if hour_of_day == 19 or x == 0:#since it is initialized at midnight monday, you need to apply this condition there too
                    EV_E_current = EV_E_current * night_factor
                EV_SoC =  EV_E_current/EV_E_max_night
                EV_E_left = EV_E_max_night - EV_E_current
                EV_E_over = EV_E_current - EV_E_min_night
                Pgrid, PH, PEV = excesspowerflow(Pexcess, EV_P_max_night, EV_E_left, EV_E_over, H_E_left, H_E_over,
                                                 H_P_max, H_eff, EV_eff, EV_E_commute)
                EV_E_current = EV_E_current - PEV
                H_E_current = H_E_current - PH
                PEV_out[x] = PEV
                PH_out[x] = PH
                Pgrid_out[x] = Pgrid
                EV_SoC_out[x] = EV_SoC
    Pgrid = np.around(Pgrid_out.astype(np.float), 3)
    PH = np.around(PH_out.astype(np.float), 3)
    PEV = np.around(PEV_out.astype(np.float), 3)
    EV_SoC = np.around(EV_SoC_out.astype(np.float), 3)
    Pexcess = np.around(Pexcess_out.astype(np.float), 3)
    H_SoC = np.around(H_SoC_out.astype(np.float), 3)
    data = {'power_grid': Pgrid.tolist(), 'power_EV': PEV.tolist(), 'power_hydrogen': PH.tolist(), 'EV_SoC':EV_SoC.tolist(), 'Pexcess':Pexcess.tolist(),'H_SoC':H_SoC.tolist()}
    return data


def excesspowerflow(Pexcess, EV_P_max, EV_E_left, EV_E_over, H_E_left, H_E_over, H_P_max, H_eff, EV_eff, EV_E_commute):
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
    if EV_E_over < 0:  # this case is when cars are too low
        Pgrid = Pgrid + EV_E_commute*2 #add two trips worth for all cars from the grid to EV
        PEV = PEV - EV_E_commute*2
    return Pgrid, PH, PEV


if __name__ == '__main__':
    powers = {'power_load': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              'power_solar': [3, 6, 3, 6, 7, 7, 0, 0, 0, 0, 0, 0, -120, 0, 0, 0, 0, 0, 0, 0, -2, 2]}
    a = power_battery(powers, N_EV=5)
