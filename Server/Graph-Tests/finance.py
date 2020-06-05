import random
import numpy as np
import numpy_financial as npf
import pandas as pd
import plotly.graph_objects as go

tot_pv_yield=[10551]
N_solar=20
Watt_DC=N_solar*0.245

panel_cost_mono=164.46
panel_cost_poly=79,34
yearly_decay_mono=0.036
discount_rate=0.08

inverter_cost=N_solar * 0.2 *505,74
#inverter_cost_replacement=inverter_cost *(1+ discount_rate)^15

OM_year= Watt_DC*12.43
Initialcost_pv = (N_solar * panel_cost_mono + Watt_DC*0.30)/0.9


cashflows = [OM_year, OM_year, OM_year, OM_year, OM_year, OM_year, OM_year, OM_year, OM_year, OM_year, OM_year, OM_year, OM_year, OM_year, OM_year, OM_year, OM_year, OM_year, OM_year, OM_year, OM_year, OM_year, OM_year, OM_year, OM_year]
yearlyyield= [10551, 10551, 10551, 10551, 10551, 10551, 10551, 10551, 10551, 10551, 10551, 10551, 10551, 10551, 10551, 10551, 10551, 10551, 10551, 10551, 10551, 10551, 10551, 10551, 10551]
discountRate = 0.09; # Nine percent per annum
discountRate_decay=0.0936
netpresent = npf.npv(discountRate, cashflows)
totalyield = npf.npv(discountRate_decay, yearlyyield)

LCOE_pv=((Initialcost_pv+ netpresent)/totalyield).round(3)

print(LCOE_pv)