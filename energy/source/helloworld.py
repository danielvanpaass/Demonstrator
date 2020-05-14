import pandas as pd
import matplotlib.pyplot as plt

naive_times = pd.date_range(start='2018', end='2019', freq='1h')

# very approximate
# latitude, longitude, name, altitude, timezone
coordinates = [(52.0, 4.3, 'Delft', 0, 'Etc/GMT+2')]

import pvlib

# get the module and inverter specifications from SAM
sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')

sapm_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')

module = sandia_modules['Canadian_Solar_CS5P_220M___2009_']

inverter = sapm_inverters['ABB__MICRO_0_25_I_OUTD_US_208__208V_']

temperature_model_parameters = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

# specify constant ambient air temp and wind for simplicity
temp_air = 20
wind_speed = 0

system = {'module': module, 'inverter': inverter, 'surface_azimuth': 180}

energies = {}

for latitude, longitude, name, altitude, timezone in coordinates:
    times = naive_times.tz_localize(timezone)
    system['surface_tilt'] = latitude
    solpos = pvlib.solarposition.get_solarposition(times, latitude, longitude)
    dni_extra = pvlib.irradiance.get_extra_radiation(times)
    aoi = pvlib.irradiance.aoi(system['surface_tilt'], system['surface_azimuth'],
                               solpos['apparent_zenith'], solpos['azimuth'])
    #total_irrad = pvlib.irradiance.get_total_irradiance(system['surface_tilt'],
                                                        #system['surface_azimuth'],
                                                        #solpos['apparent_zenith'],
                                                        #solpos['azimuth'],
                                                        #dni_extra=dni_extra,
                                                        #model='haydavies')
    tcell = pvlib.temperature.sapm_cell(total_irrad['poa_global'], temp_air, wind_speed, **temperature_model_parameters)
    dc = pvlib.pvsystem.sapm(total_irrad['poa_direct'], tcell, module)
    ac = pvlib.pvsystem.snlinverter(dc['v_mp'], dc['p_mp'], inverter)
    #annual_energy = ac.sum()
    #energies[name] = annual_energy
    energies = ac

energies = pd.Series(energies)

# based on the parameters specified above, these are in W*hrs
print(energies.round(0))

plt.plot(times, solpos)
# plt.ylabel('Yearly energy yield (W hr)')
# Text(0, 0.5, 'Yearly energy yield (W hr)')
