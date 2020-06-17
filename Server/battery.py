import numpy as np
import random
import matplotlib.pyplot as plt


class Car():
    def __init__(self, SoC):
        self.SoC = SoC
        self.powerMax = 10
        self.energyMax = 56
        self.energyMin = 0.2 * 56 + 4  # 20% plus enough for round trip to work
        self.currentEnergy = SoC * self.energyMax
        self.workdays = random.sample(range(5), 3) + [
            (random.randint(5, 6))]  # every car leaves home 3x from workdays, + 1 in the weekend, 0 means monday
        self.efficiency_store = 0.9  # percentage
        self.efficiency_take = 0.93  # percentage

    # check if car needs to charge
    def needCharging(self):
        if self.currentEnergy <= self.energyMin:
            self.currentEnergy = self.currentEnergy + 2 * self.efficiency_store
            return 2
        else:
            return 0

    def getSoC(self):
        self.SoC = self.currentEnergy / self.energyMax
        return self.SoC

    # this method can be requested with a certain power that needs to be discharged, and will check how much of it
    # can be provided
    def takePower(self, power, day, hour):
        if day in self.workdays and 9 <= hour <= 18:
            return 0
        energy_surplus = max(self.currentEnergy - self.energyMin,
                             0) * self.efficiency_take
        power_out = min(energy_surplus, self.powerMax,
                        -power)
        self.currentEnergy = self.currentEnergy - power_out / self.efficiency_take
        return power_out

    def storePower(self, power, day, hour):
        if day in self.workdays and 9 <= hour <= 18:
            return 0
        energy_chargeble = max(self.energyMax - self.currentEnergy,
                               0) / self.efficiency_store
        power_out = min(energy_chargeble, self.powerMax,
                        -power)
        self.currentEnergy = self.currentEnergy + power_out * self.efficiency_store
        return -power_out

    # this function is to be called at the end of the day, cars that were at work will now have less charge
    def returnFromWork(self, day):
        if day in self.workdays:
            self.currentEnergy = self.currentEnergy - 4  # takes 4 kwh, a round trip to work
            return 1
        else:
            return 0


class HydrogenTank:
    def __init__(self, SoC, energyMax):
        self.SoC = SoC
        self.powerMax = 98  # kwh
        self.energyMax = energyMax
        self.currentEnergy = SoC * self.energyMax
        self.efficiency_store = 0.70
        self.efficiency_take = 0.60

    def takePower(self, power):
        energy_surplus = max(self.currentEnergy,
                             0) * self.efficiency_take

        power_out = min(energy_surplus, self.powerMax,
                        -power)
        self.currentEnergy = self.currentEnergy - power_out / self.efficiency_take
        return power_out

    def storePower(self, power):
        energy_chargeble = max(self.energyMax - self.currentEnergy,
                               0) / self.efficiency_store
        power_out = min(energy_chargeble, self.powerMax,
                        -power)
        self.currentEnergy = self.currentEnergy + power_out * self.efficiency_store
        return -power_out

    def getSoC(self):
        self.SoC = self.currentEnergy / self.energyMax
        return self.SoC

    def resetSoC(self, SoC):
        self.SoC = SoC
        self.currentEnergy = SoC * self.energyMax


def power_battery(powers, N_EV, N_hydro):
    """Go through the list of all powers and decide how the storage should be charged/discharged"""
    if 'power_load' in powers:
        power_load = np.array(powers['power_load'])
    else:
        power_load = np.zeros(8760)
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
    for x in range(N_EV):  # create a new cars list for the realtime battery as well
        car = Car(0.5)
        cars.append(car)
    # create Hydrogen tank
    hydro = HydrogenTank(0.5, N_hydro * 396)

    # go through the year
    eps = 0.00000001  # define epsilon for comparisons with floats
    for x in range(0, len(power_load)):
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
        for i in range(0, N_EV):
            EV_SoC_out[x] = EV_SoC_out[x] + cars[i].getSoC() / N_EV * 100  # store the average SoC in %
        if N_hydro:
            H_SoC_out[x] = hydro.getSoC() * 100
        if excess_power > 0:  # positive so needs to store energy
            stored_power_EV = 0
            for i in range(0, N_EV):
                stored_power = cars[i].storePower(-excess_power, day_of_week, hour_of_day)
                stored_power_EV = stored_power_EV + stored_power
                excess_power = excess_power + stored_power
                # the storePower function returns for example -4, meaning 4 kwh has been stored, so update excess
                # power on this
                if abs(
                        excess_power) < eps:
                    break
            PEV_out[x] = stored_power_EV
            if excess_power > eps and N_hydro:  # this means that the cars had not enough to store the kwh

                stored_power = hydro.storePower(-excess_power)
                PH_out[x] = stored_power
                excess_power = excess_power + stored_power
            # assign what's left to the grid
            if excess_power > eps:
                stored_power = -excess_power
                Pgrid_out[x] = stored_power
        else:  # negative so needs to take energy from batteries
            power_taken_EV = 0
            for i in range(0, N_EV):
                power_taken = cars[i].takePower(excess_power, day_of_week, hour_of_day)
                power_taken_EV = power_taken_EV + power_taken
                excess_power = excess_power + power_taken
                if abs(
                        excess_power) < eps:
                    break
            PEV_out[x] = power_taken_EV
            # cars could not provide enough, look at the hydro tank
            if abs(excess_power) > eps and N_hydro:
                power_taken = hydro.takePower(excess_power)
                PH_out[x] = power_taken
                excess_power = excess_power + power_taken
            if abs(excess_power) > eps:
                power_taken = -excess_power
                Pgrid_out[x] = power_taken
    # Assign the values for export
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


if __name__ == '__main__':
    # with open('powers.txt', 'r') as outfile:
    #     powers = json.load(outfile)
    # powers = {}
    powers = {'power_load': [0] * 24,
              'power_solar': [2] * 12 + [-2] * 12}
    b = power_battery(powers, N_EV=1, N_hydro=1)
    power_EV = b['power_EV']
    power_hydrogen = b['power_hydrogen']
    power_grid = b['power_grid']
    EV_SoC = b['EV_SoC']
    H_SoC = b['H_SoC']

    time = np.arange(0, 24)

    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('Time (hour)')
    ax1.set_ylabel('Power output (kW)', color=color)
    ax1.plot(time, power_EV, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    plt.grid(axis='both')
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    plt.grid(axis='both')
    color = 'tab:blue'
    ax2.set_ylabel('SoC (%)', color=color)  # we already handled the x-label with ax1
    ax2.plot(time, EV_SoC, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    # plt.legend()
    plt.grid(axis='both')
    plt.title('Power flow and SoC of the EV')
    # plt.gca().set_ylim(bottom=0)
    plt.xticks(np.arange(0, 25, step=1))
    plt.xlim(0, 23)
    plt.savefig('EVnormal.png', bbox_inches='tight')
    plt.close()

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Time (hour)')
    ax1.set_ylabel('Power output (kW)', color=color)
    ax1.plot(time, power_hydrogen, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    plt.grid(axis='both')
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    plt.grid(axis='both')
    color = 'tab:blue'
    ax2.set_ylabel('SoC (%)', color=color)  # we already handled the x-label with ax1
    ax2.plot(time, H_SoC, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    # plt.legend()
    plt.grid(axis='both')
    plt.title('Power flow and SoC of the hydrogen tank')
    # plt.gca().set_ylim(bottom=0)
    plt.xticks(np.arange(0, 25, step=1))
    plt.xlim(0, 23)
    plt.savefig('hydrogennormal.png', bbox_inches='tight')
    plt.close()

    powers = {'power_load': [0] * 24,
              'power_solar': [100] * 12 + [-100] * 12}
    b = power_battery(powers, N_EV=1, N_hydro=1)
    power_EV = b['power_EV']
    power_hydrogen = b['power_hydrogen']
    power_grid = b['power_grid']
    EV_SoC = b['EV_SoC']
    H_SoC = b['H_SoC']

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Time (hour)')
    ax1.set_ylabel('Power output (kW)', color=color)
    ax1.plot(time, power_hydrogen, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    plt.grid(axis='both')
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    plt.grid(axis='both')
    color = 'tab:blue'
    ax2.set_ylabel('SoC (%)', color=color)  # we already handled the x-label with ax1
    ax2.plot(time, H_SoC, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.grid(axis='both')
    plt.title('Power flow and SoC of the hydrogen tank')
    plt.xticks(np.arange(0, 25, step=1))
    plt.xlim(0, 23)
    plt.savefig('hydrogenextreme.png', bbox_inches='tight')
    plt.close()

    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('Time (hour)')
    ax1.set_ylabel('Power output (kW)', color=color)
    ax1.plot(time, power_EV, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    plt.grid(axis='both')
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    plt.grid(axis='both')
    color = 'tab:blue'
    ax2.set_ylabel('SoC (%)', color=color)  # we already handled the x-label with ax1
    ax2.plot(time, EV_SoC, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    plt.grid(axis='both')
    plt.title('Power flow and SoC of the EV')

    plt.xticks(np.arange(0, 25, step=1))
    plt.xlim(0, 23)
    plt.savefig('EVextreme.png', bbox_inches='tight')
    plt.close()

    plt.plot(time, power_grid)
    plt.ylabel('Power from the grid (kW)')
    plt.xlabel('Time (hour)')
    plt.grid(axis='both')
    plt.title('Power flow from the grid')

    plt.xticks(np.arange(0, 25, step=1))
    plt.xlim(0, 23)
    plt.savefig('gridextreme.png', bbox_inches='tight')

    plt.show()
    plt.close()
