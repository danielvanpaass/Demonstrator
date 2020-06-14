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
from collections import OrderedDict
from plotly.subplots import make_subplots
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
        children='Energy System Integrator Demonstrator',
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
    dcc.Graph(id='emission', animate=True),
    html.Div(id='Paybacktime'),
    html.Div(id='table')
    ],id='output-all'),

    dcc.Interval(
        id='interval-component',
        interval=2*1000,#in miliseconds
        n_intervals=0
    ),
    # empty dummy div
    html.Div(id='hidden-div', style={'display':'none'})

])


def dash_update_solar(dict):
    global dh
    dh.update(dict)
    print("received")


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
            ],
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
                {'x': dh['time'], 'y': dh['power_load'], 'type': 'line', 'name': 'load'}
            ],
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
            ],
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
            ],
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
    global wind_cache

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
              [Input('interval-component', 'n_intervals')])
def update_graph_live_emission(n):
    global em_cache

    tot_net = sumPositiveInts(dh['power_grid'])
    tot_pv = sum(dh['power_solar']) + tot_net * 0.05
    pv_carbon = tot_pv*0.0000527
    tot_wind = sum(dh['power_wind']) + tot_net* 0.08
    wind_carbon = tot_wind * 0.0000175
    tot_gas = tot_net * 0.45
    tot_coal = tot_net * 0.32
    tot_oil = tot_net * 0.04
    tot_nuclear = tot_net * 0.03
    tot_other = tot_net * 0.03
    sources = ['Solar', 'Wind', 'Battery']

    fig = go.Figure(data=[
        go.Bar(name='GHG', x=sources, y=[pv_carbon, wind_carbon, 2])
    ])
    fig.update_layout(
        title="Life cycle emission",
        xaxis_title="Generation source",
        yaxis_title="Tonne CO2 equivalent",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )
    global em_cache
    if em_cache != fig:
        em_cache = fig
    else:
        raise PreventUpdate
    return fig



#-------------------Payback---------------------------------------------------------------
pay_cache = 0

@app.callback(Output('Paybacktime', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live_pay(n):
    global pay_cache
    if pay_cache != dh['power_grid']:
        pay_cache = dh['power_grid']

        WIND_FINANCE = {
            'Aeolos10': {'P_rated': 10000, 'investment_cost': 23313.40, 'OM per KWh': 0.02},
            'Vestas V90 2MW': {'P_rated': 2000000, 'investment_cost': 2456000, 'OM per KWh': 0.02}
        }
        PV_FINANCE = {
            'Mono residential': {'watt_peak': 245, 'price': 164.46, 'yearly_decay': 0.0939, 'bos': 0.30, 'OM': 12.43},
            'Mono commercial': {'watt_peak': 245, 'price': 164.46, 'yearly_decay': 0.0939, 'bos': 0.25, 'OM': 11.32},
            'Poly residential': {'watt_peak': 295, 'price': 89.45, 'yearly_decay': 0.0964, 'bos': 0.30, 'OM': 12.43},
            'Poly commercial': {'watt_peak': 295, 'price': 89.45, 'yearly_decay': 0.0964, 'bos': 0.25, 'OM': 11.32}
        }
        N_wind=1
        N_solar=200
        total_investment = 1000
        yearly_savings = 200
        payback = total_investment / yearly_savings
        #print(payback)
    else:
        raise PreventUpdate
    return payback



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
        ('With', [(sum(g_o[:744])*0.22), sum(g_o[745:1416])*0.22, sum(g_o[1417:2161])*0.22, sum(g_o[2161:2881])*0.22,
                sum(g_o[2881:3625])*0.22, sum(g_o[3625:4345])*0.22, sum(g_o[4345:5089])*0.22, sum(g_o[5089:5833])*0.22,
                sum(g_o[5833:6553])*0.22, sum(g_o[6553:7297])*0.22, sum(g_o[7297:8017])*0.22, sum(g_o[8017:8761])*0.22,
                sum(g_o)*0.22]),
    ]))
    table = dash_table.DataTable(
        id='typing_formatting_1',
        data=df_typing_formatting.to_dict('rows'),
        columns=[{
            'id': 'Month',
            'name': 'City',
            'type': 'text'
        }, {
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
            'name': 'Energy cost Without (€)',
            'type': 'numeric',
            'format': Format(
                precision=2,
                scheme=Scheme.fixed,
                symbol=Symbol.yes,
                symbol_suffix=u'€'
            ),
        }, {
            'id': 'With',
            'name': 'Energy cost With (€)',
            'type': 'numeric',
            'format': Format(
                precision=2,
                scheme=Scheme.fixed,
                symbol=Symbol.yes,
                symbol_suffix=u'€'
            )
        },
        ],
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
        global load
        if load != [loadvalue,loadtype]:
            load = [loadvalue,loadtype]
            data = {'N_load': loadvalue}
            data.update({'load_type': loadtype})
            client.publish("load", json.dumps(data))
            print( 'load request')
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
        global PV
        if PV != [paneltype, panelvalue, tiltvalue]:
            PV = [paneltype, panelvalue, tiltvalue]
            data = ({'pv_type': paneltype})
            data.update({'N_solar': panelvalue})
            data.update({'tilt_panel': tiltvalue})
            client.publish("solar", json.dumps(data))
            print('solar request')
        return 0


    @app.callback(
        Output('hidden-div', 'Turbine'),
        [Input('button', 'n_clicks')],
        [State('dropdownwind', 'value'), State('inputwind', 'value')],  # add amount of windmills
    )
    def update_output_wind(n_clicks, turbinetype, windvalue):
        global wind
        if wind != [turbinetype,windvalue]:
            wind = [turbinetype,windvalue]
            data = ({'turbine_type': turbinetype})
            data.update({'N_wind': windvalue})
            client.publish("wind", json.dumps(data))
            print('wind request')
        return 0


    @app.callback(
       Output('hidden-div','battery'),
       [Input('button_bat', 'n_clicks')],
       [State('input EV', 'value'), State('input H', 'value')],
    )
    def update_output_bat(n_clicks,evvalue, hydrogen):
       print('bat request')
       #hydrogen = 1 or hydrogen = 0
       number_bat.setValue(evvalue, hydrogen)
       return 0

    app.run_server(debug=False)


if __name__ == '__main__':
    app.run_server(debug=False)