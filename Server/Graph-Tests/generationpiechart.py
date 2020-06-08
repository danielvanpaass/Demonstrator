import plotly.graph_objects as go
from plotly.subplots import make_subplots
data = {'pv':[1,4,1,2,4,2],
         'wind':[1,2,5,3,2,0],
        'net':[10,2,-5,0,2,0]}
tot_net=  sum(data['net'])
tot_pv =  sum(data['pv'])+tot_net*0.05
tot_wind= sum(data['wind'])*0.08
tot_gas=tot_net*0.45
tot_coal=tot_net*0.32
tot_oil=tot_net*0.04
tot_nuclear=tot_net*0.03
tot_other=tot_net*0.03


labels=['PV','Wind','Natural Gas','Coal','Oil','Nuclear','Other']
share=[tot_pv,tot_wind,tot_gas,tot_coal,tot_oil,tot_nuclear,tot_other]

# fig = go.Figure(data=[go.Pie(labels=labels, values=share)])
# fig.show()

fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]])


fig.add_trace(go.Pie(
     values=share,
     labels=labels,
     domain=dict(x=[0, 0.5]),
     name="Share of Energy source"),
     row=1, col=1)

fig.add_trace(go.Pie(
     values=[27, 11, 4],
     labels=["Green", "Grey", "Unknown",
             ],
     domain=dict(x=[0.5, 1.0]),
     name="Green vs grey"),
    row=1, col=2)

fig.show()