import requests
import pandas as pd
import json
"""get API access to Irradiance and Temp of 2019, with input: location"""

lat, lon = 51.998, 4.373#Delft
weather = {}
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
start_year = 24 - 1 #because of time zone
data_solar = data[start_year:start_year+8760]
global_ir = data.to_numpy()[:, 2] + data.to_numpy()[:, 3]
weather.update({'irradiance_direct':data['irradiance_direct'].tolist()})
weather.update({'irradiance_direct':data['irradiance_direct'].tolist()})
weather.update({'irradiance_diffuse':data['irradiance_diffuse'].tolist()})
weather.update({'temp':data['temperature'].tolist()})
# temp = data.to_numpy()[:, 4]



api_base = 'https://www.renewables.ninja/api/'
s = requests.session()
s.headers = {'Authorization': 'Token 39046b41231860f99468167ba101617bcb782f05'}
url = api_base + 'data/wind'
args = {
    'local_time': 'true',
    'raw': 'true',
    'lat': lat,
    'lon': lon,
    'date_from': '2018-12-31',
    'date_to': '2019-12-31',
    'dataset': 'merra2',
    'capacity': 1.0,
    'height': 100,
    'turbine': 'Vestas V80 2000',
    'format': 'json'
}
r = s.get(url, params=args)
parsed_response = json.loads(r.text)
data = pd.read_json(json.dumps(parsed_response['data']), orient='index')
# trim this to year data of Ir and Temp
start_year = 24 - 1 #because of time zone
data_wind = data[start_year:start_year+8760]
weather.update({'wind':data['wind_speed'].tolist()})
with open('weather.txt', 'w') as outfile:
    json.dump(weather, outfile)