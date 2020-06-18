import base64
import json
import time

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import dash_table
from dash_table.Format import Format, Scheme, Sign, Symbol
import pandas as pd
import math
from collections import OrderedDict
from plotly.subplots import make_subplots
import numpy_financial as npf

data = {}
dh = {'power_solar': [1, 2, 3],
      'power_load': [1, 2, 3],
      'power_wind': [1, 2, 3],
      'power_grid': [1, 2, 3],
      'EV_SoC': [1, 2, 3],
      'H_SoC': [1, 2, 3],
      }

labels=['PV','Wind','Natural Gas','Coal','Oil','Nuclear','Other']
labels_2=['Green', 'Grey', 'Unknown']

def sumNegativeInts(listInt):
    m = 0
    for x in listInt:
        if x < 0:
            m+= x
    return (int(m))

def sumPositiveInts(listInt):
    m = 0
    for x in listInt:
        if x > 0:
            m += x
    return(int(m))

def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

start = time.time()

dh.update({'time': pd.date_range(start='2019-01-01 00:00', freq='1h', periods=8760)})
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

colors = {
    'background': '#111111',
    'text': '#00A6D6'
}
test_png = 'TUD.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

#-------------------dash layout---------------------------------------------------------------

app.layout = html.Div(children=[
    html.H1(
        children='Energy System Integration Demonstrator',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Img(src='data:image/png;base64,{}'.format(test_base64)),
    html.H3('PV Parameters',
            style={'color': colors['text']}),
    html.Div('PV module type'),
    dcc.Dropdown(
        id='dropdownpvtype',
        options=[
            {'label': 'HIT-N245SE10 Monocrystalline', 'value': 'HIT-N245SE10'},
            {'label': 'JAP60S01-290/SC Polycrystalline', 'value': 'JAP60S01-290/SC'},
        ],
        value='HIT-N245SE10'
    ),
    html.Div('Number of PV panels'),
    dcc.Input(id='input', value=200, type='number'),
    html.Button('Refresh', id='button', n_clicks=0),
    html.Div('Tilt of the PV panels'),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': '30 degrees', 'value': 30},
            {'label': '35 degrees', 'value': 35},
            {'label': '40 degrees', 'value': 40}
        ],
        value=30
    ),
    html.H3('Wind Parameters',
            style={'color': colors['text']}),
    html.Div('Wind turbine model'),
    dcc.Dropdown(
        id='dropdownwind',
        options=[
            {'label': 'Aeolos10', 'value': 'Aeolos10'},
            {'label': 'Hummer60', 'value': 'Hummer60'},
            {'label': 'Vestas V90 2MW', 'value': 'V90-2MW'},
        ],
        value='Aeolos10'
    ),
    html.Div('Number of Wind turbines'),
    dcc.Input(id='inputwind', value=2, type='number'),
    html.H3('Load Parameters',
            style={'color': colors['text']}),
    html.Div('Type of Energy users'),
    dcc.Dropdown(
        id='dropdownhousehold',
        options=[
            {'label': 'Energy saving households', 'value': 'saving'},
            {'label': 'Average households', 'value': 'average'},
        ],
        value='average'
    ),
    html.Div('Number of houses in the neighbourhood'),
    dcc.Input(id='input load', value=40, type='number'),
    html.H3('Battery Parameters',
            style={'color': colors['text']}),
    html.Div('Number of Hydrogen Tanks'),
    dcc.Input(id='input H', value=1, type='number'),
    html.Div('Number of EV'),
    dcc.Input(id='input EV', value=10, type='number'),
    html.Button('Refresh battery', id='button_bat', n_clicks=0),



    html.Div(children = [
    dcc.Graph(id='pvpower', ),
    dcc.Graph(id='windpower',),
    dcc.Graph(id='loadpower', ),
    dcc.Graph(id='EVpower', ),
    dcc.Graph(id='Hydrogen', ),
    dcc.Graph(id='gridpower', ),
    dcc.Graph(id='piechart', ),
    #dcc.Graph(id='piechartshare', animate=False,)
    dcc.Graph(id='emission',),
    dcc.Graph(id='lcoe',),
    html.H3('payback time [years]',
            style={'color': colors['text']}),
    html.Div(id='pay'),
    html.Div(id='table')
    ],id='output-all'),

    dcc.Interval(
        id='interval-component',
        interval=4*1000,#in miliseconds
        n_intervals=0
    ),
    # empty dummy div
    html.Div(id='hidden-div', style={'display':'none'})

])


def dash_update_solar(dict):
    global dh,start
    dh.update(dict)
    print("received at" +str(time.time()-start))
    start = time.time()


# @app.callback([
#     Output('pvpower', 'animate'),
#     Output('windpower', 'animate'),
#     Output('loadpower', 'animate'),
#     Output('EVpower', 'animate'),
#     Output('Hydrogen', 'animate'),
#     Output('gridpower', 'animate'),
#     ],
#     [Input('interval-component', 'n_intervals')])
# def update_graph(n):
#     print(n)
#
#     animate = True
#
#     animate = [animate]*6 #8 because 8 outputs are required
#     return animate




#-------------------pv figure---------------------------------------------------------------
PV_cache = 0

@app.callback(Output('pvpower', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_solar(n):
    global PV_cache
    if PV_cache != dh['power_solar']:
        PV_cache = dh['power_solar']
        
        figure = {
            'data': [
                {'x': dh['time'], 'y': dh['power_solar'], 'type': 'line', 'name': 'PV'}
            ],'marker' : { 'color' :'#00A6D6' },
            'layout': {
                'title': 'PV power output',
                'xaxis': {
                    'title': 'Time'
                },
                'yaxis': {
                    'title': 'Power [kW]'
                }
            }
        }
    else:
        raise PreventUpdate
    return figure

#-------------------Wind figure---------------------------------------------------------------
wind_cache = 0

@app.callback(Output('windpower', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_wind(n):
    global wind_cache
    if wind_cache != dh['power_wind']:
        wind_cache = dh['power_wind']
        figure = {
            'data': [
                {'x': dh['time'], 'y': dh['power_wind'], 'type': 'line', 'name': 'Wind'}
            ],
            'layout': {
                'title': 'Wind power output',
                'xaxis': {
                    'title': 'Time'
                },
                'yaxis': {
                    'title': 'Power [kW]'
                }
            }
        }
    else:
        raise PreventUpdate
    return figure


#-------------------load figure---------------------------------------------------------------
load_cache = 0

@app.callback(Output('loadpower', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live_load(n):
    global load_cache
    if load_cache != dh['power_load']:
        load_cache = dh['power_load']
        figure = {
            'data': [
                {'x': dh['time'], 'y': dh['power_load'], 'type': 'line', 'name': 'load',}
            ],'marker' : { 'color' :'#00A6D6' },
            'layout': {
                'title': 'Residential load consumption',
                'xaxis': {
                    'title': 'Time'
                },
                'yaxis': {
                    'title': 'Power [kW]'
                }
            }
        }
    else:
        raise PreventUpdate
    return figure

#-------------------Battery---------------------------------------------------------------
EV_cache = 0

@app.callback(Output('EVpower', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_ev(n):
    global EV_cache
    if EV_cache != dh['EV_SoC']:
        EV_cache = dh['EV_SoC']
        figure = {
            'data': [
                {'x': dh['time'], 'y': dh['EV_SoC'], 'type': 'line', 'name': 'Battery'}
            ],'marker' : { 'color' :'#00A6D6' },
            'layout': {
                'title': 'Electric vehicle battery soc',
                'xaxis': {
                    'title': 'Time'
                },
                'yaxis': {
                    'title': 'SoC [%]'
                }
            }
        }
    else:
        raise PreventUpdate
    return figure


#-------------------Battery---------------------------------------------------------------
hydro_cache = 0

@app.callback(Output('Hydrogen', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_hydrogen(n):
    global hydro_cache
    if hydro_cache != dh['H_SoC']:
        hydro_cache = dh['H_SoC']
        figure = {
            'data': [
                {'x': dh['time'], 'y': dh['H_SoC'], 'type': 'line', 'name': 'Hydrotank'}
            ],'marker' : { 'color' :'#00A6D6' },
            'layout': {
                'title': 'Hydrogen battery soc',
                'xaxis': {
                    'title': 'Time'
                },
                'yaxis': {
                    'title': 'SoC [%]'
                }
            }
        }
    else:
        raise PreventUpdate
    return figure


#-------------------grid---------------------------------------------------------------
grid_cache = 0

@app.callback(Output('gridpower', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live_load(n):
    global grid_cache
    if grid_cache != dh['power_grid']:
        grid_cache = dh['power_grid']
        figure = {
            'data': [
                {'x': dh['time'], 'y': dh['power_grid'], 'type': 'line', 'name': 'grid'}
            ],
            'layout': {
                'title': 'Grid Power flow',
                'xaxis': {
                    'title': 'Time'
                },
                'yaxis': {
                    'title': 'Power [kW]'
                }
            }
        }
    else:
        raise PreventUpdate
    return figure



#-------------------pie chart---------------------------------------------------------------
pie_cache = 0

@app.callback(Output('piechart', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live_pie(n):

    global pie_cache

    tot_net = sumPositiveInts(dh['power_grid'])
    tot_pv = sum(dh['power_solar']) + tot_net * 0.05
    tot_wind = sum(dh['power_wind']) + tot_net* 0.08
    tot_gas = tot_net * 0.45
    tot_coal = tot_net * 0.32
    tot_oil = tot_net * 0.04
    tot_nuclear = tot_net * 0.03
    tot_other = tot_net * 0.03
    green = tot_pv + tot_wind
    grey = tot_gas + tot_oil + tot_coal
    other = tot_nuclear + tot_other
    share = [tot_pv, tot_wind, tot_gas, tot_coal, tot_oil, tot_nuclear, tot_other]
    share_2 = [green, grey, other]

    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]])

    fig.add_trace(go.Pie(
        values=share,
        labels=labels,
        domain=dict(x=[0, 0.5]),
        name="Share of Energy source"),
        row=1, col=1)

    fig.add_trace(go.Pie(
        values=share_2,
        labels=["Green", "Grey", "Unknown",
                ],
        domain=dict(x=[0.5, 1.0]),
        name="Green vs grey"),
        row=1, col=2)
    global pie_cache
    if pie_cache != fig:
        pie_cache = fig
    else:
        raise PreventUpdate
    return fig

#-------------------emissions figure---------------------------------------------------------------
em_cache = 0

@app.callback(Output('emission', 'figure'),
              [Input('interval-component', 'n_intervals')],state=[State('dropdownpvtype', 'value'),
                                                                   State('input', 'value'),
                                                                   State('dropdownwind', 'value'),
                                                                   State('inputwind', 'value'),
                                                                   State('input H', 'value'),
                                                                   State('input EV', 'value'),
                                                                  ],)
def update_graph_live_emission(n,type,number,typewind,numberwind,H,EV):
    global em_cache

    WIND_EMISSIONS = {
        'Aeolos10': {'P_rated': 10000, 'GHG': 0.000047,},
        'Hummer60': {'P_rated': 60000, 'GHG': 0.000047,},
        'Vestas V90 2MW': {'P_rated': 2000000, 'GHG': 0.0000093,}
    }
    PV_EMISSIONS = {
        'Mono': {'watt_peak': 245, 'GHG': 0.00004702,},
        'Poly': {'watt_peak': 295, 'GHG': 0.00005155,}
    }
    if type == 'HIT-N245SE10':
        dpv = PV_EMISSIONS['Mono']
    else:
        dpv = PV_EMISSIONS['Poly']
    if typewind == 'Aeolos10':
        dwe= WIND_EMISSIONS['Aeolos10']
    elif typewind == 'V90-2MW':
        dwe = WIND_EMISSIONS['Vestas V90 2MW']
    elif typewind == 'Hummer60':
        dwe = WIND_EMISSIONS['Hummer60']

    ghgwind=dwe['GHG']
    ghgpv = dpv['GHG']
    tot_net = sumPositiveInts(dh['power_grid'])
    tot_pv = sum(dh['power_solar']) + tot_net * 0.05
    pv_carbon = round(tot_pv*ghgpv,4)
    tot_wind = sum(dh['power_wind']) + tot_net* 0.08
    wind_carbon = round(tot_wind * ghgwind,4)
    tot_h=H*0.007485
    tot_ev=EV*0.327
    tot_gas = (tot_net * 0.45)*0.000499
    tot_coal = (tot_net * 0.32)*0.000888
    tot_oil = (tot_net * 0.04)*0.000733
    tot_nuclear = (tot_net * 0.03)*0.00029
    tot_other = tot_net * 0.03
    sources = ['Solar', 'Wind', ' Hydrogen Battery', 'EV Battery','Natural Gas', 'Coal', 'Oil', 'Nuclear']

    fig = go.Figure(data=[
        go.Bar(name='CO2', x=sources, y=[pv_carbon*0.836, wind_carbon*0.941, tot_h*0.81, tot_ev*0.81, tot_gas*0.9375, tot_coal*0.81, tot_oil*0.81, tot_nuclear*0.651], ),
        go.Bar(name='Methane', x=sources, y=[pv_carbon*0.112, wind_carbon*0.002, tot_h*0.1, tot_ev*0.1, tot_gas*0.0023, tot_coal*0.1, tot_oil*0.1, tot_nuclear*0.0007], ),
        go.Bar(name='Nitrous Oxide', x=sources, y=[pv_carbon * 0.0495, wind_carbon * 0.005, tot_h * 0.07, tot_ev * 0.07, tot_gas * 0.001125, tot_coal * 0.07, tot_oil * 0.07, tot_nuclear * 0.0007], ),
        go.Bar(name='Fluorinated Gases & rest', x=sources, y=[pv_carbon * 0.0025, wind_carbon * 0.0583, tot_h * 0.03, tot_ev * 0.03, tot_gas * 0.0591, tot_coal * 0.03, tot_oil * 0.03, tot_nuclear * 0.0346], )
    ])
    fig.update_layout(
        title="Life cycle emission",
        xaxis_title="Generation source",
        yaxis_title="Tonne CO2 equivalent",
        height=1000, barmode='stack'
    )
    global em_cache
    if em_cache != fig:
        em_cache = fig
    else:
        raise PreventUpdate
    return fig



#-------------------lcoe---------------------------------------------------------------
lcoe_cache = 0

@app.callback(Output('lcoe', 'figure'),
              [Input('interval-component', 'n_intervals',)],state=[State('dropdownpvtype', 'value'),
                                                                   State('input', 'value'),
                                                                   State('dropdownwind', 'value'),
                                                                   State('inputwind', 'value'),
                                                                   State('input H', 'value'),
                                                                   State('input EV', 'value'),],)
def update_graph_live_lcoe(n,type,number,typewind,numberwind,H,EV):
    global lcoe_cache
    WIND_FINANCE = {
        'Aeolos10': {'P_rated': 10000, 'investment_cost': 23313.40, 'OM per year': 466.27},
        'Hummer60': {'P_rated': 60000, 'investment_cost': 106860.00, 'OM per year': 2137.20},
        'Vestas V90 2MW': {'P_rated': 2000000, 'investment_cost': 2456000, 'OM per year': 49120}
    }
    PV_FINANCE = {
        'Mono residential': {'watt_peak': 245, 'price': 164.46, 'yearly_decay': 0.0939, 'bos': 1.65, 'OM': 12.43},
        'Mono commercial': {'watt_peak': 245, 'price': 164.46, 'yearly_decay': 0.0939, 'bos': 0.35, 'OM': 11.32},
        'Poly residential': {'watt_peak': 295, 'price': 89.45, 'yearly_decay': 0.0964, 'bos': 1.65, 'OM': 12.43},
        'Poly commercial': {'watt_peak': 295, 'price': 89.45, 'yearly_decay': 0.0964, 'bos': 0.35, 'OM': 11.32}
    }
    discountRate = 0.09  # Nine percent per annum
    total_solar_power = dh['power_solar']
    if type == 'HIT-N245SE10':
        output_pv = number* 245
        if output_pv < 10000:
            dpv = PV_FINANCE['Mono residential']
        else:
            dpv = PV_FINANCE['Mono commercial']
    elif type == 'JAP60S01-290/SC':
        output_pv = number * 295
        if output_pv < 10000:
            dpv = PV_FINANCE['Poly residential']
        else:
            dpv = PV_FINANCE['Poly commercial']
    inverter_cost = roundup(number) * 0.1 * 505.74
    Initialcost_pv = (number * dpv['price'] + (inverter_cost + dpv['watt_peak'] * dpv['bos'])/0.9)
    cashflows = [dpv['OM']] * 14
    cashflows.extend([dpv['OM'] + inverter_cost])
    cashflows.extend(
        [dpv['OM'], dpv['OM'], dpv['OM'], dpv['OM'], dpv['OM'], dpv['OM'], dpv['OM'], dpv['OM'], dpv['OM'],
         dpv['OM']])
    yearlyyield = [sum(dh['power_solar'])]*25
    netpresent = npf.npv(discountRate, cashflows)
    totalyield = npf.npv(dpv['yearly_decay'], yearlyyield)
    lcoe_pv = ((Initialcost_pv + netpresent) / totalyield).round(3)

    if typewind == 'Aeolos10':
        dw= WIND_FINANCE['Aeolos10']
    elif typewind == 'V90-2MW':
        dw = WIND_FINANCE['Vestas V90 2MW']
    elif typewind == 'Hummer60':
        dw = WIND_FINANCE['Hummer60']
    turbine_cost= numberwind * dw['investment_cost']
    discountrate_decay_wind = 0.112
    cashflowwind = [dw['OM per year']] * 20
    yearlyyieldwind = [sum(dh['power_wind'])]*20
    netpresentwind = npf.npv(discountRate, cashflowwind)
    totalyieldwind = npf.npv(discountrate_decay_wind, yearlyyieldwind)
    lcoe_w = ((turbine_cost + netpresentwind) / totalyieldwind).round(3)
    bat_cost = EV * (57 + 3000)
    bat_cap = EV*56*308
    bat_cost_h = H * (78048 + 48000)
    bat_cap_h = H * 396 * 5000
    lcoe_sev = round(((bat_cost) / bat_cap),2)
    lcoe_seh = round(((bat_cost_h) / bat_cap_h), 2)
    fig = go.Figure(data=[
        go.Bar(name='LCOE', x=['pv', 'wind', 'Lithium Ion', 'Hydrogen'], y=[lcoe_pv, lcoe_w, lcoe_sev, lcoe_seh], marker_color='#00A6D6', )
    ])
    fig.update_layout(
        title="LCOE for renewable generation and storage",
        height=600,
        xaxis_title="Generation source",
        yaxis_title="€ / kWh",
    )

    # fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "bar"}]])
    # fig.add_trace(go.Bar(
    #     y=[lcoe_pv,lcoe_w],
    #     x=['pv','wind',],
    #     domain=dict(x=[0, 0.5]),
    #     name="LCOE energy"),
    #     row=1, col=1)
    #
    # fig.add_trace(go.Bar(
    #     y=[lcoe_s],
    #     x=['storage'],
    #     domain=dict(x=[0.5, 1.0]),
    #     name="LCOE storage"),
    #     row=1, col=2)
    # fig.update_layout(
    #     title="Levelized cost of energy",
    #     xaxis_title="Generation source",
    #     yaxis_title="€/kWh",
    # )

    global lcoe_cache
    if lcoe_cache != fig:
        lcoe_cache = fig
    else:
        raise PreventUpdate
    return fig


#-------------------paybacktime---------------------------------------------------------------
pay_cache = 0

@app.callback(Output('pay', 'children'),
              [Input('interval-component', 'n_intervals',)],state=[State('dropdownpvtype', 'value'),
                                                                   State('input', 'value'),
                                                                   State('dropdownwind', 'value'),
                                                                   State('inputwind', 'value'),
                                                                   State('input H', 'value'),
                                                                   State('input EV', 'value'),
                                                                   ],)
def update_graph_live_pay(n,type,number,typewind,numberwind,H,EV):
    global pay_cache
    WIND_FINANCE = {
        'Aeolos10': {'P_rated': 10000, 'investment_cost': 23313.40, 'OM per year': 466.27},
        'Hummer60': {'P_rated': 60000, 'investment_cost': 106860.00, 'OM per year': 2137.20},
        'Vestas V90 2MW': {'P_rated': 2000000, 'investment_cost': 2456000, 'OM per year': 49120}
    }
    PV_FINANCE = {
        'Mono residential': {'watt_peak': 245, 'price': 164.46, 'yearly_decay': 0.0939, 'bos': 1.65, 'OM': 12.43},
        'Mono commercial': {'watt_peak': 245, 'price': 164.46, 'yearly_decay': 0.0939, 'bos': 0.35, 'OM': 11.32},
        'Poly residential': {'watt_peak': 295, 'price': 89.45, 'yearly_decay': 0.0964, 'bos': 1.65, 'OM': 12.43},
        'Poly commercial': {'watt_peak': 295, 'price': 89.45, 'yearly_decay': 0.0964, 'bos': 0.35, 'OM': 11.32}
    }
    discountRate = 0.09  # Nine percent per annum
    if type == 'HIT-N245SE10':
        output_pv = number* 245
        if output_pv < 10000:
            dpv = PV_FINANCE['Mono residential']
        else:
            dpv = PV_FINANCE['Mono commercial']
    elif type == 'JAP60S01-290/SC':
        output_pv = number * 295
        if output_pv < 10000:
            dpv = PV_FINANCE['Poly residential']
        else:
            dpv = PV_FINANCE['Poly commercial']
    if typewind == 'Aeolos10':
        dw= WIND_FINANCE['Aeolos10']
    elif typewind == 'V90-2MW':
        dw = WIND_FINANCE['Vestas V90 2MW']
    elif typewind == 'Hummer60':
        dw = WIND_FINANCE['Hummer60']
    inverter_cost = roundup(number) * 0.2 * 505.74
    Initialcost_pv = (number * dpv['price'] + (inverter_cost + dpv['watt_peak'] * dpv['bos'])/0.9)
    Initialcost_wind= (numberwind * dw['investment_cost'])
    bat_cost_h = H * (78048 + 48000)
    bat_cost = EV * (57 + 3000)
    total_investment= Initialcost_wind + Initialcost_pv +bat_cost_h + bat_cost
    pos_net = sumPositiveInts(dh['power_grid'])
    neg_net = sumNegativeInts(dh['power_grid'])
    yearly_savings = (sum(dh['power_load'])*0.22 - pos_net*0.22 + neg_net*0.06)
    paytime= total_investment/(0.1+yearly_savings)
    if paytime > 0:
        paytimes=round(paytime,2)
    else:
        paytimes= '(not reached)'
    total_investments=round(total_investment,2)
    global pay_cache
    if pay_cache != paytime:
        pay_cache = paytime
    else:
        raise PreventUpdate
    return 'The payback time is expected to be {} years with a total investment cost of €{} '.format(paytimes,total_investments)
#-------------------Table---------------------------------------------------------------
table_cache = 0

@app.callback(Output('table', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live_table(n):
    global wind_cache
    pv_o = dh['power_solar']
    w_o = dh['power_wind']
    g_o = dh['power_grid']
    l_o = dh['power_load']

    df_typing_formatting = pd.DataFrame(OrderedDict([
        ('Month', ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Total 2019']),
        ('PV', [sum(pv_o[:744]) / 31, sum(pv_o[745:1416]) / 31, sum(pv_o[1417:2161]) / 31, sum(pv_o[2161:2881]) / 31,
                sum(pv_o[2881:3625]) / 31, sum(pv_o[3625:4345]) / 31, sum(pv_o[4345:5089]) / 31, sum(pv_o[5089:5833]) / 31,
                sum(pv_o[5833:6553]) / 31, sum(pv_o[6553:7297]) / 31, sum(pv_o[7297:8017]) / 31, sum(pv_o[8017:8761]) / 31,
                sum(pv_o) / 31]),
        ('Wind', [sum(w_o[:744]) / 31, sum(w_o[745:1416]) / 31, sum(w_o[1417:2161]) / 31, sum(w_o[2161:2881]) / 31,
                sum(w_o[2881:3625]) / 31, sum(w_o[3625:4345]) / 31, sum(w_o[4345:5089]) / 31, sum(w_o[5089:5833]) / 31,
                sum(w_o[5833:6553]) / 31, sum(w_o[6553:7297]) / 31, sum(w_o[7297:8017]) / 31, sum(w_o[8017:8761]) / 31,
                sum(w_o) / 31]),
        ('Grid', [sum(g_o[:744]) / 31, sum(g_o[745:1416]) / 31, sum(g_o[1417:2161]) / 31, sum(g_o[2161:2881]) / 31,
                sum(g_o[2881:3625]) / 31, sum(g_o[3625:4345]) / 31, sum(g_o[4345:5089]) / 31, sum(g_o[5089:5833]) / 31,
                sum(g_o[5833:6553]) / 31, sum(g_o[6553:7297]) / 31, sum(g_o[7297:8017]) / 31, sum(g_o[8017:8761]) / 31,
                sum(g_o) / 31]),
        ('Electricity Saved', [(sum(w_o[:744]) + sum(pv_o[:744])) / 31, (sum(w_o[745:1416]) + sum(pv_o[745:1416])) / 31,
                               (sum(w_o[1417:2161]) + sum(pv_o[1417:2161])) / 31, (sum(w_o[2161:2881]) + sum(pv_o[2161:2881])) / 31,
                               (sum(w_o[2881:3625]) + sum(pv_o[2881:3625])) / 31, (sum(w_o[3625:4345]) + sum(pv_o[3625:4345])) / 31,
                               (sum(w_o[4345:5089]) + sum(pv_o[4345:5089])) / 31, (sum(w_o[5089:5833]) + sum(pv_o[5089:5833])) / 31,
                               (sum(w_o[5833:6553]) + sum(pv_o[5833:6553])) / 31, (sum(w_o[6553:7297]) + sum(pv_o[6553:7297])) / 31,
                               (sum(w_o[7297:8017]) + sum(pv_o[7297:8017])) / 31, (sum(w_o[8017:8761]) + sum(pv_o[8017:8761])) / 31,
                               (sum(w_o) + sum(pv_o)) / 31]),
        ('Without', [sum(l_o[:744])*0.22, sum(l_o[745:1416])*0.22, sum(l_o[1417:2161])*0.22, sum(l_o[2161:2881])*0.22,
                sum(l_o[2881:3625])*0.22, sum(l_o[3625:4345])*0.22, sum(l_o[4345:5089])*0.22, sum(l_o[5089:5833])*0.22,
                sum(l_o[5833:6553])*0.22, sum(l_o[6553:7297])*0.22, sum(l_o[7297:8017])*0.22, sum(l_o[8017:8761])*0.22,
                sum(l_o)*0.22]),
        ('With',
         [(sum(g_o[:744]) * 0.22), sum(g_o[745:1416]) * 0.22, sum(g_o[1417:2161]) * 0.22, sum(g_o[2161:2881]) * 0.22,
          sum(g_o[2881:3625]) * 0.22, sum(g_o[3625:4345]) * 0.22, sum(g_o[4345:5089]) * 0.22,
          sum(g_o[5089:5833]) * 0.22,
          sum(g_o[5833:6553]) * 0.22, sum(g_o[6553:7297]) * 0.22, sum(g_o[7297:8017]) * 0.22,
          sum(g_o[8017:8761]) * 0.22,
          sum(g_o) * 0.22]),
    ]))
    table = dash_table.DataTable(
        id='typing_formatting_1',
        data=df_typing_formatting.to_dict('rows'),
        columns=[{
            'id': 'Month',
            'name': 'Month',
            'type': 'text'
        },

            {
            'id': 'PV',
            'name': 'PV output (KWh) / day',
            'type': 'numeric',
            'format': Format(
                precision=1,
                scheme=Scheme.fixed,
                symbol=Symbol.yes,
                symbol_suffix=u'KWh')
        }, {
            'id': 'Wind',
            'name': 'Wind output (KWh) / day',
            'type': 'numeric',
            'format': Format(
                precision=1,
                scheme=Scheme.fixed,
                symbol=Symbol.yes,
                symbol_suffix=u'KWh')
        }, {
            'id': 'Grid',
            'name': 'Grid output (KWh) / day',
            'type': 'numeric',
            'format': Format(
                precision=1,
                scheme=Scheme.fixed,
                symbol=Symbol.yes,
                symbol_suffix=u'KWh')

        }, {
            'id': 'Electricity Saved',
            'name': 'Electricity Saved (KWh) / day',
            'type': 'numeric',
            'format': Format(
                precision=1,
                scheme=Scheme.fixed,
                symbol=Symbol.yes,
                symbol_suffix=u'KWh')

        }, {
            'id': 'Without',
            'name': 'Electricity bill old (€)',
            'type': 'numeric',
            'format': Format(
                precision=2,
                scheme=Scheme.fixed,
                symbol=Symbol.yes,
                symbol_suffix=u'€'
            ),
        }, {
            'id': 'With',
            'name': 'Electricity bill new (€)',
            'type': 'numeric',
            'format': Format(
                precision=2,
                scheme=Scheme.fixed,
                symbol=Symbol.yes,
                symbol_suffix=u'€'
            )
        },
        ],style_header={'backgroundColor': '#00A6D6'},
        editable=True
    )



    global table_cache
    if table_cache !=table:
        table_cache = table
    else:
        raise PreventUpdate
    return table



#------------------------MQTT--------------------------------------------------------------------
wind = 0
load = 0
PV = 0
def connect_and_run_dash(client, number_bat):

    @app.callback(
        Output('hidden-div','load'),
        [Input('button', 'n_clicks')],
        state=[State('input load', 'value'), State('dropdownhousehold', 'value')],
    )
    def update_output_load(n_clicks,loadvalue, loadtype):
        global load,start
        if load != [loadvalue,loadtype]:
            load = [loadvalue,loadtype]
            data = {'N_load': loadvalue}
            data.update({'load_type': loadtype})
            client.publish("load", json.dumps(data))
            print( 'load request at'  +str(time.time()-start))
            start = time.time()
        return 0

    # @app.callback([
    #     Output('pvpower', 'animate'),
    #     Output('windpower', 'animate'),
    #     Output('loadpower', 'animate'),
    #     Output('EVpower', 'animate'),
    #     Output('Hydrogen', 'animate'),
    #     Output('gridpower', 'animate'),
    # ],
    #     [Input('interval-component', 'n_intervals')])
    # def update_graph(n):
    #     print(n)
    #     if n % 20 == 10:
    #         animate = False
    #     else:
    #         animate = True
    #     animate = [animate] * 6  # 8 because 8 outputs are required
    #     return animate

    @app.callback(
        Output('hidden-div','PV'),
        [Input('button', 'n_clicks')],
        state=[State('dropdownpvtype', 'value'), State('input', 'value'), State('dropdown', 'value'),],
    )
    def update_output_solar(n_clicks, paneltype, panelvalue, tiltvalue):
        global PV,start
        if PV != [paneltype, panelvalue, tiltvalue]:
            PV = [paneltype, panelvalue, tiltvalue]
            data = ({'pv_type': paneltype})
            data.update({'N_solar': panelvalue})
            data.update({'tilt_panel': tiltvalue})
            client.publish("solar", json.dumps(data))
            print('solar request at' +str(time.time()-start))
            start = time.time()
        return 0


    @app.callback(
        Output('hidden-div', 'Turbine'),
        [Input('button', 'n_clicks')],
        [State('dropdownwind', 'value'), State('inputwind', 'value')],  # add amount of windmills
    )
    def update_output_wind(n_clicks, turbinetype, windvalue):
        global wind,start
        if wind != [turbinetype,windvalue]:
            wind = [turbinetype,windvalue]
            data = ({'turbine_type': turbinetype})
            data.update({'N_wind': windvalue})
            client.publish("wind", json.dumps(data))
            print('wind request at'  +str(time.time()-start))
            start = time.time()
        return 0


    @app.callback(
       Output('hidden-div','battery'),
       [Input('button_bat', 'n_clicks')],
       [State('input EV', 'value'), State('input H', 'value')],
    )
    def update_output_bat(n_clicks,evvalue, hydrogen):
       global start
       print('bat request at' +str(time.time()-start))
       start = time.time()
       #hydrogen = 1 or hydrogen = 0
       number_bat.setValue(evvalue, hydrogen)
       return 0

    app.run_server(debug=False)


if __name__ == '__main__':
    app.run_server(debug=False)