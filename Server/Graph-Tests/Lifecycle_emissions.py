import plotly.graph_objects as go

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
fig1 = go.Figure(go.Bar(
            x=share1,
            y=labels1,
            orientation='h'))

#fig2 = go.Figure([go.Bar(x=labels2, y=share2)])
fig2 = go.Figure(data=[
    go.Bar(name='Carbon dioxide', x=labels2, y=share2),
    go.Bar(name='Methane', x=labels2, y=share2),
    go.Bar(name='Nitrous oxide', x=labels2, y=share2),
    go.Bar(name='Fluorinated gases', x=labels2, y=share2),

])
# Change the bar mode
fig2.update_layout(barmode='stack')
#fig.show()
#fig2.show()
fig1.show()
