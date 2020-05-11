import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# from timezonefinder import TimezoneFinder

"""get API access to Irradiance and Temp of 2019, with input: location"""


def gather_ir(lat, lon):
    api_base = 'https://www.renewables.ninja/api/'
    s = requests.session()
    s.headers = {'Authorization': 'Token 39046b41231860f99468167ba101617bcb782f05'}
    url = api_base + 'data/pv'
    args = {
        'local_time': 'true',
        'raw': 'true',
        'lat': lat,
        'lon': lon,
        'date_from': '2018-12-31',
        'date_to': '2019-12-31',
        'dataset': 'merra2',
        'capacity': 1.0,
        'system_loss': 0.1,
        'tracking': 0,
        'tilt': 35,
        'azim': 180,
        'format': 'json'
    }
    r = s.get(url, params=args)
    parsed_response = json.loads(r.text)
    data = pd.read_json(json.dumps(parsed_response['data']), orient='index')
    # trim this to year data of Ir and Temp
    timezone = 1  # should be calculated from localtime in data
    start_year = 24 - timezone
    data = data[start_year:data.size - timezone]
    global_ir = data.to_numpy()[:, 2] + data.to_numpy()[:, 3]
    temp = data.to_numpy()[:, 4]
    return global_ir, temp


# An implementation of a solar energy model in Netherlands
# size, angle(panel), irradiance, efficiency, temperature reliance
# import time
# import math
# import datetime


"""Power calculation solar panel with ambient temp as operating temp"""


def power_calc(length, width, efficiency, coefficient, irradiance, temperature):
    p_nom = length * width * efficiency * irradiance
    p_out = (((coefficient * (temperature - 25)) / 100) * p_nom) + p_nom
    return p_out


# lat and lon as input, global_ir and Temp array as output of 2019
global_ir, temp = gather_ir(51.998, 4.373)

# Datasheet imported values
length, width, efficiency, coefficient = 1.956, 0.992, 0.186, -0.39

# calculate power per solar panel
power = power_calc(length, width, efficiency, coefficient, global_ir, temp)
# timehour = np.arange(0, temp.size)

"""Main function to be called in this file, for total power out in a year per hour"""


def power_out_solar(N_panels):
    data = {}  # empty dictionary
    tot_power = power * N_panels
    tot_power = np.around(tot_power.astype(np.float), 3)  # rounding for reducing the message size
    data.update({'power': tot_power.tolist()})

    return json.dumps(data)

    # m_in=json.loads(m_decode) #decode json data
    # plt.plot(timehour[0:24], power[0:24])
    # plt.xlabel("Time (hr)")
    # plt.ylabel("Power (W)")
    # plt.show()
    #
