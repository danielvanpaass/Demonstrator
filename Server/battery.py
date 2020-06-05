import numpy as np
import random
import json


class Car():
    def __init__(self, SoC):
        self.SoC = SoC
        # self.working = 0  # all cars home
        self.powerMax = 6.6  # with level 2 station
        self.energyMax = 56
        self.energyMin = 0.1*56  # enough for 1 more round trip to work
        self.currentEnergy = SoC * self.energyMax
        self.workdays = random.sample(range(5), 3) + [
            (random.randint(5, 6))]  # every car leaves home 3x from workdays, + 1 in the weekend, 0 means monday

    def needCharging(self):
        if self.currentEnergy <= self.energyMin + 2:
            self.currentEnergy = self.currentEnergy + 2  # this equals single trip to work
            return 2
        else:
            return 0

    def getSoC(self):
        self.SoC = self.currentEnergy / self.energyMax
        return self.SoC

    def takePower(self, power, day, hour):  # should come in a positieve power
        if day in self.workdays and 9 <= hour <= 18:
            return 0  # car is working so no power
        energy_surplus = max(self.currentEnergy - self.energyMin, 0)  # so surplus has to be larger than 0 or it will give 0
        power_out = min(energy_surplus, self.powerMax,
                        -power)  # you have either the maximum power constraint or the E surplus constraint
        self.currentEnergy = self.currentEnergy - power_out
        return power_out

    def storePower(self, power, day, hour):  # power should be negative because storing power
        if day in self.workdays and 9 <= hour <= 18:
            return 0  # car is working so no power
        energy_chargeble = max(self.energyMax - self.currentEnergy, 0)  # has to be larger than 0 or it will give 0
        power_out = min(energy_chargeble, self.powerMax,
                        -power)  # you have either the maximum power constraint or the E chargeble constraint
        self.currentEnergy = self.currentEnergy + power_out
        return -power_out

    def returnFromWork(self, day):
        if day in self.workdays:
            self.currentEnergy = self.currentEnergy - 4  # takes 4 kwh round trip to work
            return 1  # sucessful
        else:
            return 0

    # def setWork(self, workStatus):
    #     self.working = workStatus


class HydrogenTank:
    def __init__(self, SoC):
        self.SoC = SoC
        self.powerMax = 100  # kwh
        self.energyMax = 300
        self.currentEnergy = SoC * self.energyMax

    def takePower(self, power):
        energy_surplus = max(self.currentEnergy, 0)  # so surplus has to be larger than 0 or it will give 0
        power_out = min(energy_surplus, self.powerMax,
                        -power)  # you have either the maximum power constraint or the E surplus constraint
        self.currentEnergy = self.currentEnergy - power_out
        return power_out

    def storePower(self, power): # power should be negative because storing power
        energy_chargeble = max(self.energyMax - self.currentEnergy, 0)  # has to be larger than 0 or it will give 0
        power_out = min(energy_chargeble, self.powerMax,
                        -power)  # you have either the maximum power constraint or the E chargeble constraint
        self.currentEnergy = self.currentEnergy + power_out
        return -power_out

    def getSoC(self):
        self.SoC = self.currentEnergy / self.energyMax
        return self.SoC

    def resetSoC(self, SoC):
        self.SoC = SoC
        self.currentEnergy = SoC * self.energyMax


global_hydrogen = HydrogenTank(0.5)
global_cars = []


def power_battery(powers, N_EV):
    print(N_EV)
    global global_cars, global_hydrogen
    global_cars = []
    global_hydrogen.resetSoC(0.5)
    power_load = np.array(powers['power_load'])
    power_source = np.zeros((len(power_load)))
    if 'power_solar' in powers:
        power_source = power_source + np.array(powers['power_solar'])
    if 'power_wind' in powers:
        power_source = power_source + np.array(powers['power_wind'])
    PEV_out = np.zeros((len(power_load),))
    PH_out = np.zeros((len(power_load),))
    Pgrid_out = np.zeros((len(power_load),))
    EV_SoC_out = np.zeros((len(power_load),))
    H_SoC_out = np.zeros((len(power_load),))
    excess_power_out = np.zeros((len(power_load),))
    EV_load_out = np.zeros((len(power_load),))
    cars = []
    # create all cars
    for x in range(N_EV):
        car = Car(0.7)
        cars.append(car)  # starting all cars with battery on 70%
        global_cars.append(car)
    for x in range(N_EV): #create a new cars list for the realtime battery as well
        car = Car(0.5)
        global_cars.append(car)
    # create Hydrogen tank
    hydro = HydrogenTank(0.7)
    # go through the year
    for x in range(0, len(power_load)):
        # sort all cars by SoC, starting from lowest
        # cars.sort(key=lambda car: car.getSoC())
        excess_power = power_source[x] - power_load[x]
        day = x // 24
        day_of_week = day % 7
        hour_of_day = x % 24
        EV_load = 0
        if hour_of_day == 19:  # return from work
            for i in range(0, N_EV):
                cars[i].returnFromWork(day_of_week)
        for i in range(0, N_EV):
            EV_load = EV_load + cars[i].needCharging()
        excess_power = excess_power - EV_load
        EV_load_out[x] = EV_load
        excess_power_out[x] = excess_power
        if excess_power > 0:  # positive so needs to store energy
            stored_power_EV = 0
            for i in range(0, N_EV):
                stored_power = cars[i].storePower(-excess_power, day_of_week, hour_of_day)
                stored_power_EV = stored_power_EV + stored_power
                excess_power = excess_power + stored_power
                # the storePower function returns for example -4, meaning 4 kwh has been stored, so update excess power on this
                if abs(
                        excess_power) < 0.001:  # if part of the cars were enough, not the whole list will be looked through
                    break
            PEV_out[x] = stored_power_EV
            if excess_power > 0.001:  # this means that all cars had not enough to store the kwh
                stored_power = hydro.storePower(-excess_power)
                PH_out[x] = stored_power
                excess_power = excess_power + stored_power
            if excess_power > 0.001:
                stored_power = -excess_power
                Pgrid_out[x] = stored_power
        else:  # negative so needs to take energy from batteries
            power_taken_EV = 0
            for i in range(0, N_EV):
                power_taken = cars[i].takePower(excess_power, day_of_week, hour_of_day)
                power_taken_EV = power_taken_EV + power_taken
                excess_power = excess_power + power_taken
                # the storePower function returns for example -4, meaning 4 kwh has been stored, so update excess power on this
                if abs(
                        excess_power) < 0.001:  # if part of the cars were enough, not the whole list will be looked through
                    break
            PEV_out[x] = power_taken_EV
            if abs(excess_power) > 0.001:  # this means that not all cars had enough energy
                power_taken = hydro.takePower(excess_power)
                PH_out[x] = power_taken
                excess_power = excess_power + power_taken
            if abs(excess_power) > 0.001:
                power_taken = -excess_power
                Pgrid_out[x] = power_taken
        for i in range(0, N_EV):
            EV_SoC_out[x] = EV_SoC_out[x] + cars[i].getSoC() / N_EV  # store the average SoC
        H_SoC_out[x] = hydro.getSoC()
    Pgrid = np.around(Pgrid_out.astype(np.float), 3)
    PH = np.around(PH_out.astype(np.float), 3)
    PEV = np.around(PEV_out.astype(np.float), 3)
    EV_SoC = np.around(EV_SoC_out.astype(np.float), 3)
    excess_power = np.around(excess_power_out.astype(np.float), 3)
    H_SoC = np.around(H_SoC_out.astype(np.float), 3)
    EV_load = np.around(EV_load_out.astype(np.float), 3)
    data = {'power_grid': Pgrid.tolist(), 'power_EV': PEV.tolist(), 'power_hydrogen': PH.tolist(),
            'EV_SoC': EV_SoC.tolist(), 'excess_power': excess_power.tolist(), 'H_SoC': H_SoC.tolist(),
            'EV_load': EV_load.tolist()}
    return data


def power_battery_realtime(actuator_powers, hour):
    power_source = 0
    if 'power_solar' in actuator_powers:
        power_source += actuator_powers['power_solar']
    if 'power_wind' in actuator_powers:
        power_source += actuator_powers['power_wind']
    power_load = actuator_powers['power_load']
    global global_hydrogen, global_cars
    N_EV = len(global_cars)
    excess_power = power_source - power_load
    day = hour // 24
    day_of_week = day % 7
    hour_of_day = hour % 24
    if hour_of_day == 19:  # return from work
        for i in range(0, N_EV):
            global_cars[i].returnFromWork(day_of_week)
    EV_load = 0
    for i in range(0, N_EV):
        EV_load = EV_load + global_cars[i].needCharging()
    excess_power = excess_power + EV_load
    excess_power_out = excess_power
    EV_load_out = EV_load
    Pgrid_out = PH_out = 0.0
    if excess_power > 0:  # positive so needs to store energy
        stored_power_EV = 0.0
        for i in range(0, N_EV):
            stored_power = global_cars[i].storePower(-excess_power, day_of_week, hour_of_day)
            stored_power_EV = stored_power_EV + stored_power
            excess_power = excess_power + stored_power
            # the storePower function returns for example -4, meaning 4 kwh has been stored, so update excess power
            # on this
            if abs(
                    excess_power) < 0.001:  # if part of the cars were enough, not the whole list will be looked through
                break
        PEV_out = stored_power_EV
        if excess_power > 0.001:  # this means that all cars had not enough to store the kwh
            stored_power = global_hydrogen.storePower(-excess_power)
            excess_power = excess_power + stored_power
            PH_out = stored_power
        if excess_power > 0.001:
            stored_power = -excess_power
            Pgrid_out = stored_power
    else:  # negative so needs to take energy from batteries
        power_taken_EV = 0.0
        for i in range(0, N_EV):
            power_taken = global_cars[i].takePower(excess_power, day_of_week, hour_of_day)
            power_taken_EV = power_taken_EV + power_taken
            excess_power = excess_power + power_taken

            # the storePower function returns for example -4, meaning 4 kwh has been stored, so update excess power
            # on this
            if abs(excess_power) < 0.001:  # if part of the cars were enough, not the whole list will be looked through
                break
        PEV_out = power_taken_EV
        if abs(excess_power) > 0.001:  # this means that not all cars had enough energy
            power_taken = global_hydrogen.takePower(excess_power)
            excess_power = excess_power + power_taken
            PH_out = power_taken
        if abs(excess_power) > 0.001:
            power_taken = -excess_power  # from grid
            Pgrid_out = power_taken
    EV_SoC_out = 0.0
    for i in range(0, N_EV):
        EV_SoC_out += global_cars[i].getSoC() / N_EV  # store the average SoC
    H_SoC_out = global_hydrogen.getSoC()
    Pgrid = np.around(Pgrid_out, 3)
    PH = np.around(PH_out, 3)
    PEV = np.around(PEV_out, 3)
    EV_SoC = np.around(EV_SoC_out, 3)
    excess_power = np.around(excess_power_out, 3)
    H_SoC = np.around(H_SoC_out, 3)
    EV_load = np.around(EV_load_out, 3)
    data = {'power_grid': Pgrid.tolist(), 'power_EV': PEV.tolist(), 'power_hydrogen': PH.tolist(),
            'EV_SoC': EV_SoC.tolist(), 'excess_power': excess_power.tolist(), 'H_SoC': H_SoC.tolist(),
            'EV_load': EV_load.tolist(), 'hour': hour}
    return data


if __name__ == '__main__':
    with open('powers.txt', 'r') as outfile:
        powers = json.load(outfile)
    # powers = {'power_load': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #           'power_solar': [100, 116, 130, 160, 170, 17, 110, 110, 110, 20, 20, 20, 120, 0, 0, 0, 0, 0, 0, 0, -2, 2]}
    b = power_battery(powers, N_EV=1)
    actuator_powers = {'power_load':5, 'power_wind':10}
    a = power_battery_realtime(actuator_powers, 0)
