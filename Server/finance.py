import random
import numpy as np
import numpy_financial as npf
import pandas as pd
import plotly.graph_objects as go
import math

# tot_pv_yield=[105510]
# tot_wind_yield=[28279]



WIND_FINANCE = {
    'Aeolos10': {'P_rated': 10000, 'investment_cost': 23313.40, 'OM per KWh': 0.02 },
    'Vestas V90 2MW': {'P_rated': 2000000, 'investment_cost':  2456000, 'OM per KWh': 0.02 }
}
PV_FINANCE = {
    'Mono residential': {'watt_peak': 245, 'price': 164.46, 'yearly_decay': 0.0939, 'bos': 0.30, 'OM': 12.43},
    'Mono commercial': {'watt_peak': 245, 'price': 164.46, 'yearly_decay': 0.0939, 'bos': 0.25, 'OM': 11.32},
    'Poly residential': {'watt_peak': 295, 'price': 89.45, 'yearly_decay': 0.0964, 'bos': 0.30, 'OM': 12.43},
    'Poly commercial': {'watt_peak': 295, 'price': 89.45, 'yearly_decay': 0.0964, 'bos': 0.25, 'OM': 11.32}
}

def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

N_solar = 20
N_wind = 1

type_panel = 'HIT-N245SE10'
#type_panel = 'JAP60S01-290/SC'

type_turbine = 'Aeolos10'
discountRate = 0.09  # Nine percent per annum


def lcoe():
    if type_panel == 'HIT-N245SE10':
        output_pv= N_solar*245
        if output_pv < 10000:
            dpv= PV_FINANCE['Mono residential']
        else:
            dpv= PV_FINANCE['Mono commercial']
    elif type_panel == 'JAP60S01-290/SC':
        output_pv=N_solar*295
        if output_pv < 10000:
            dpv = PV_FINANCE['Poly residential']
        else:
            dpv = PV_FINANCE['Poly commercial']
    inverter_cost = roundup(N_solar) * 0.1 * 505.74
    Initialcost_pv = (N_solar * dpv['price'] + inverter_cost + dpv['watt_peak'] * dpv['bos']) / 0.9
    cashflows = [dpv['OM']] * 14
    cashflows.extend([dpv['OM']+inverter_cost])
    cashflows.extend([dpv['OM'], dpv['OM'], dpv['OM'], dpv['OM'], dpv['OM'], dpv['OM'], dpv['OM'], dpv['OM'], dpv['OM'], dpv['OM']])
    yearlyyield = [10551] * 25
    netpresent = npf.npv(discountRate, cashflows)
    totalyield = npf.npv(dpv['yearly_decay'], yearlyyield)
    lcoe_pv = ((Initialcost_pv + netpresent) / totalyield).round(3)
    print(lcoe_pv)
    return dpv, lcoe_pv


def lcoe_wind():
    if type_turbine == 'Aeolos10':
        dw= WIND_FINANCE['Aeolos10']
    elif type_turbine == 'Vestas V90 2MW':
        dw = WIND_FINANCE['Vestas V90 2MW']
    turbine_cost= N_wind * dw['investment_cost']
    discountrate_decay_wind = 0.112
    cashflowwind = [dw['OM per KWh'] * 28279] * 20
    yearlyyieldwind = [28279] * 20
    netpresentwind = npf.npv(discountRate, cashflowwind)
    totalyieldwind = npf.npv(discountrate_decay_wind, yearlyyieldwind)
    lcoe_w = ((turbine_cost + netpresentwind) / totalyieldwind).round(3)
    print(lcoe_w)
    return dw, lcoe_w


D_PV, LCOEPV = lcoe()
D_W, LCOEW = lcoe_wind()

# fig = go.Figure([go.Bar(x=['PV','Wind'], y=[LCOEPV, LCOEW])])
# fig.show()

def paybacktime():
    total_investment= N_wind * D_W['investment_cost'] + N_solar*D_PV['price'] + N_solar * 0.2 * 505.74
    yearly_savings= (28279 + 10551)*(0.22-0.02)-0.001*D_PV['OM']*N_solar*D_PV['watt_peak']
    payback= total_investment/yearly_savings
    print(payback)

paybacktime()

dh = {'power_solar': [1, 2, 3],
      'power_load': [1, 2, 3],
      'power_wind': [1, 2, 3],
      'power_grid': [1, 2, 3],
      'EV_SoC': [1, 2, 3],
      'H_SoC': [1, 2, 3],
      }
pv_output = dh['power_solar']
w_output = dh['power_wind']

headerColor = '#00A6D6'
rowEvenColor = 'lightgrey'
rowOddColor = 'white'
fig = go.Figure(data=[go.Table(
  header=dict(
    values=['<b>Sort</b>','<b>Jan</b>','<b>Feb</b>','<b>Mar</b>','<b>April</b>','<b>May</b>','<b>Jun</b>','<b>Jul</b>','<b>Aug</b>','<b>sep</b>','<b>Oct</b>','<b>Nov</b>','<b>Dec</b>'],
    line_color='darkslategray',
    fill_color=headerColor,
    align=['left','center'],
    font=dict(color='white', size=12)
  ),
  cells=dict(
    values=[
      ['PV_yield_day', 'Wind_yield_day', 'Net_grid_day', 'Energy_saved', 'Bill_without', 'Bill_with'],
      [sum(pv_output[:3])/3, sum(w_output[:3])/3, 80000, 2000, 12120000, 10000],
      [1300000, 20000, 70000, 2000, 130902000, 10000],
      [1300000, 20000, 120000, 2000, 131222000, 10000],
      [1400000, 20000, 90000, 2000, 14102000, 10000],
      [1200000, 20000, 80000, 2000, 12120000, 10000],
      [1300000, 20000, 70000, 2000, 130902000, 10000],
      [1300000, 20000, 120000, 2000, 131222000, 10000],
      [1400000, 20000, 90000, 2000, 14102000, 10000],
      [1200000, 20000, 80000, 2000, 12120000, 10000],
      [1300000, 20000, 70000, 2000, 130902000, 10000],
      [1300000, 20000, 120000, 2000, 131222000, 10000],
      [1400000, 20000, 90000, 2000, 14102000, 10000]],

    line_color='darkslategray',
    # 2-D list of colors for alternating rows
    fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*5],
    align = ['left', 'center'],
    font = dict(color = 'darkslategray', size = 11)
    ))
])


fig.show()