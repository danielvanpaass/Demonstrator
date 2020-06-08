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
    'Mono residential': {'watt_peak': 245, 'price': 164.46, 'yearly_decay': 0.0939, 'bos': 0.30, 'OM': 12.43},
    'Mono commercial': {'watt_peak': 245, 'price': 164.46, 'yearly_decay': 0.0939, 'bos': 0.25, 'OM': 11.32},
    'Poly residential': {'watt_peak': 295, 'price': 89.45, 'yearly_decay': 0.0964, 'bos': 0.30, 'OM': 12.43},
    'Poly commercial': {'watt_peak': 295, 'price': 89.45, 'yearly_decay': 0.0964, 'bos': 0.25, 'OM': 11.32}
}



type_panel = 'HIT-N245SE10'
#type_panel = 'JAP60S01-290/SC'
type_turbine = 'Aeolos10'
discountRate = 0.09  # Nine percent per annum


def lcoe():
    if type_panel == 'HIT-N245SE10':
        output_pv= N_solar*245
        if output_pv < 10000:
            data= PV_FINANCE['Mono residential']
        elif output_pv >= 100000:
            data= PV_FINANCE['Mono commercial']
    elif type_panel == 'JAP60S01-290/SC':
        output_pv=N_solar*295
        if output_pv < 10000:
            data = PV_FINANCE['Poly residential']
        elif output_pv < 10000:
            data = PV_FINANCE['Poly commercial']
    inverter_cost = N_solar * 0.1 * 505.74
    Initialcost_pv = (N_solar * panel_cost + inverter_cost + inverter_cost_replacement + Watt_DC * bos) / 0.9
    cashflows = [OM_year] * 25
    yearlyyield = [10551] * 25
    netpresent = npf.npv(discountRate, cashflows)
    totalyield = npf.npv(discountrate_decay, yearlyyield)
    lcoe_pv = ((Initialcost_pv + netpresent) / totalyield).round(3)
    return lcoe_pv


# def lcoe_wind():
#     if type_turbine == 'Aeolos10':
#         turbine_cost= N_wind * (14338.54 + 2168.48 + 3097.83 + 3708.55)
#         discountrate_decay_wind = 0.112
#         OM_wind_year= 0.0015 * 28279 + 350
#         cashflowwind = [OM_wind_year] * 20
#         yearlyyieldwind = [28279] * 20
#         netpresentwind = npf.npv(discountRate, cashflowwind)
#         totalyieldwind = npf.npv(discountrate_decay_wind, yearlyyieldwind)
#         lcoe_w = ((turbine_cost + netpresentwind) / totalyieldwind).round(3)
#         return lcoe_w
#
# fig = go.Figure([go.Bar(x=['PV','Wind'], y=[lcoe(), lcoe_wind()])])
# fig.show()
#
# def paybacktime():
#     total_investment= N_wind * WIND_FINANCE['Aeolos10']['investment_cost'] + N_solar*PV_FINANCE['HIT-N245SE10']['price'] + N_solar * 0.2 * 505.74
#     yearly_savings= (28279 + 10551)*0.22
#     payback= total_investment/yearly_savings
#     print(payback)
# paybacktime()