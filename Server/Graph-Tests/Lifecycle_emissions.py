import plotly.graph_objects as go
from plotly.subplots import make_subplots



data = {'pv':[1,4,1,2,4,2],
         'wind':[1,2,5,3,2,0],
        'net':[10,2,5,0,2,0]}
tot_net=  sum(data['net'])
tot_pv =  sum(data['pv'])+tot_net*0.05
tot_wind= sum(data['wind'])*0.08
tot_gas=tot_net*0.45
tot_coal=tot_net*0.32
tot_oil=tot_net*0.04
tot_nuclear=tot_net*0.03
tot_other=tot_net*0.03

tot_carbon=0.2*tot_net
tot_methane=0.1*tot_net
tot_nitrous=0.05*tot_net
tot_fluor=0.04*tot_net

labels1=['Fluorinated gases','Nitrous oxide','Methane','Carbon dioxide']
share1=[tot_fluor,tot_nitrous,tot_methane,tot_carbon]

labels2=['PV','Wind','Natural Gas','Coal','Oil','Nuclear','Other']
share2=[tot_pv,tot_wind,tot_gas,tot_coal,tot_oil,tot_nuclear,tot_other]

fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "bar"}]])


fig.add_trace(go.Bar(name='Greenhouse gases',
     x=labels1,y=share1,
),
     row=1, col=1)

fig.add_trace(go.Bar(name='Lifecycle emissions per source',
     x=labels2, y=share2,
),
    row=1, col=2)

fig.update_layout(
    title_text="Global Emissions 1990-2011")

fig.show()
