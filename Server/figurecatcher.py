import json
import numpy as np
import matplotlib.pyplot as plt
with open('powers.txt', 'r') as outfile:
    powers = json.load(outfile)


power_EV = np.array(powers['power_EV']).reshape([-1,24]).sum(axis=1)/24
power_hydrogen = np.array(powers['power_hydrogen']).reshape([-1,24]).sum(axis=1)/24
power_grid = np.array(powers['power_grid']).reshape([-1,24]).sum(axis=1)/24
EV_SoC = np.array(powers['EV_SoC']).reshape([-1,24]).sum(axis=1)/24*100
power_load = np.array(powers['power_load']).reshape([-1,24]).sum(axis=1)/24
power_solar = np.array(powers['power_solar']).reshape([-1,24]).sum(axis=1)/24
power_wind = np.array(powers['power_wind']).reshape([-1,24]).sum(axis=1)/24
excess_power = np.array(powers['excess_power']).reshape([-1,24]).sum(axis=1)/24
H_SoC = np.array(powers['H_SoC']).reshape([-1,24]).sum(axis=1)/24*100


time = np.arange(0, 365)

plt.plot(time, EV_SoC)
plt.ylabel('SoC (%)')
plt.xlabel('Time (day)')
plt.title('SoC of the EVs')
plt.gca().set_ylim(bottom=0)
plt.xlim(0, 365)
plt.savefig('systemEV.png', bbox_inches='tight')
plt.close()

plt.plot(time, H_SoC)
plt.ylabel('SoC (%)')
plt.xlabel('Time (day)')
plt.title('SoC of the hydrogen tank')
plt.gca().set_ylim(bottom=0)
plt.xlim(0, 365)
plt.savefig('systemhydro.png', bbox_inches='tight')
plt.close()

plt.plot(time, power_solar)
plt.ylabel('Power output (kW)')
plt.xlabel('Time (day)')
plt.title('Power output of the solar panels')
plt.gca().set_ylim(bottom=0)
plt.xlim(0, 365)
plt.savefig('systemsolar.png', bbox_inches='tight')
plt.close()

plt.plot(time, power_load)
plt.ylabel('Power (kW)')
plt.xlabel('Time (day)')
plt.title('Power demand of the residential homes')
# plt.gca().set_ylim(bottom=0)
plt.xlim(0, 365)
plt.savefig('systemload.png', bbox_inches='tight')
plt.close()

plt.plot(time, power_wind)
plt.ylabel('Power output (kW)')
plt.xlabel('Time (day)')
plt.title('Power output of the wind turbines')
plt.gca().set_ylim(bottom=0)
plt.xlim(0, 365)
plt.savefig('systemwind.png', bbox_inches='tight')
plt.close()

plt.plot(time, power_grid)
plt.ylabel('Power (kW)')
plt.xlabel('Time (day)')
plt.title('Power from the national grid')
# plt.gca().set_ylim(bottom=0)
plt.xlim(0, 365)
plt.savefig('systemgrid.png', bbox_inches='tight')
plt.close()

plt.plot(time, excess_power)
plt.ylabel('Power (kW)')
plt.xlabel('Time (day)')
plt.title('Total power excess from the subtraction of\n loads (including cars) from sources')
# plt.gca().set_ylim(bottom=0)
plt.xlim(0, 365)
plt.savefig('systemexcess.png', bbox_inches='tight')
plt.close()


