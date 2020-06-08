import random
import numpy as np
import numpy_financial as npf
import pandas as pd
import plotly.graph_objects as go

tot_pv_yield=[10551]
tot_wind_yield=[28279]
#inputs
N_solar = 20
N_wind = 1

WIND_FINANCE = {
    'Aeolos10': {'P_rated': 10000, 'investment_cost': 23313.40, }
}
PV_FINANCE = {
    'HIT-N245SE10': {'watt_peak': 245, 'price': 164.46, 'yearly_decay': 0.0939}
}
PV_SIZE = {
    'Residential': {'bos': 0.30, 'OM': 12.43},
    'Commercial': {'bos': 0.25, 'OM': 11.32}
}


type_panel = 'HIT-N245SE10'
#type_panel = 'JAP60S01-290/SC'
type_turbine = 'Aeolos10'
discountRate = 0.09  # Nine percent per annum


def lcoe():
    if type_panel == 'HIT-N245SE10':
        Watt_DC=N_solar*245
        panel_cost=164.46
        discountrate_decay = 0.0936
    elif type_panel == 'JAP60S01-290/SC':
        Watt_DC=N_solar*295
        panel_cost = 164.46
        discountrate_decay = 0.0964
    if Watt_DC < 10000:
        bos = 0.3
        OM_year = 0.001*Watt_DC * 12.43
    elif Watt_DC >= 10000:
        bos = 0.25
        OM_year = 0.001*Watt_DC * 11.32
    inverter_cost = N_solar * 0.1 * 505.74
    inverter_cost_replacement = inverter_cost * (1.00 + discountRate) ** 15
    Initialcost_pv = (N_solar * panel_cost + inverter_cost + inverter_cost_replacement + Watt_DC * bos) / 0.9
    cashflows = [OM_year] * 25
    yearlyyield = [10551] * 25
    netpresent = npf.npv(discountRate, cashflows)
    totalyield = npf.npv(discountrate_decay, yearlyyield)
    lcoe_pv = ((Initialcost_pv + netpresent) / totalyield).round(3)
    return lcoe_pv


def lcoe_wind():
    if type_turbine == 'Aeolos10':
        turbine_cost= N_wind * (14338.54 + 2168.48 + 3097.83 + 3708.55)
        discountrate_decay_wind = 0.112
        OM_wind_year= 0.0015 * 28279 + 350
        cashflowwind = [OM_wind_year] * 20
        yearlyyieldwind = [28279] * 20
        netpresentwind = npf.npv(discountRate, cashflowwind)
        totalyieldwind = npf.npv(discountrate_decay_wind, yearlyyieldwind)
        lcoe_w = ((turbine_cost + netpresentwind) / totalyieldwind).round(3)
        return lcoe_w

fig = go.Figure([go.Bar(x=['PV','Wind'], y=[lcoe(), lcoe_wind()])])
fig.show()

def paybacktime():
    total_investment= N_wind * WIND_FINANCE['Aeolos10']['investment_cost'] + N_solar*PV_FINANCE['HIT-N245SE10']['price'] + N_solar * 0.2 * 505.74
    yearly_savings= (28279 + 10551)*0.22
    payback= total_investment/yearly_savings
    print(payback)
paybacktime()