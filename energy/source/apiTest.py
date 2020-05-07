import json
import requests
import pandas as pd
from timezonefinder import TimezoneFinder


def gatherIr(lat,lon):
    #getting API access to Irradiance and Temp
    api_base = 'https://www.renewables.ninja/api/'
    s = requests.session()
    s.headers = {'Authorization': 'Token 39046b41231860f99468167ba101617bcb782f05'}
    url = api_base + 'data/pv'
    args = {
        'local_time':'true',
        'raw':'true',
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
    #trim this to year data of Ir and Temp
    timezone = 1#should be calculated from localtime in data
    startYear = 24-timezone
    data = data[startYear:data.size-timezone]
    globalIr = data.to_numpy()[:,2]+data.to_numpy()[:,3]
    temp = data.to_numpy()[:,4]
    return globalIr,temp

#lat and lon as input, GlobalIr and Temp array as output of 2019
gatherIr(51.998,4.373)