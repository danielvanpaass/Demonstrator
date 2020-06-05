import base64
import json
import time

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots
start = 0.0
end = 0.0
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
    dcc.Input(id='input', value=20, type='number'),
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
            {'label': 'WES5', 'value': 'WES5'},
        ],
        value='Aeolos10'
    ),
    html.H3('Load Parameters',
            style={'color': colors['text']}),
    html.Div('Number of houses in the neighbourhood'),
    dcc.Dropdown(
        id='dropdownhousehold',
        options=[
            {'label': 'Energy saving households', 'value': 'saving'},
            {'label': 'Average households', 'value': 'average'},
        ],
        value='average'
    ),
    dcc.Input(id='input load', value=160, type='number'),
    html.Button('Refresh', id='buttonload', n_clicks=0),

    html.H3('Battery Parameters',
            style={'color': colors['text']}),
    html.Div('Number of EV'),
    dcc.Input(id='input EV', value=80, type='number'),
    html.Button('Refresh', id='buttonev', n_clicks=0),

    html.Div(id='output-pv'),
    dcc.Graph(id='pvpower', animate=True),
    dcc.Graph(id='windpower', animate=True),
    dcc.Graph(id='loadpower', animate=True),
    dcc.Graph(id='EVpower', animate=True),
    dcc.Graph(id='Hydrogen', animate=True),
    dcc.Graph(id='gridpower', animate=True),
    dcc.Graph(id='piechart', animate=True),
    dcc.Graph(id='piechartshare', animate=True),
    #dcc.Graph(id='emissions', animate=True),
    dcc.Interval(
        id='interval-component',
        interval=2*1000,
        n_intervals=0
    )

])


def dash_update_solar(dict):
    global dh
    dh.update(dict)
    end = time.time()
    print(end - start)

#-------------------pv figure---------------------------------------------------------------
@app.callback(Output('pvpower', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_solar(n):
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
    return figure

#-------------------Wind figure---------------------------------------------------------------
@app.callback(Output('windpower', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_wind(n):
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
    return figure


#-------------------load figure---------------------------------------------------------------
@app.callback(Output('loadpower', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live_load(n):
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
    return figure

#-------------------Battery---------------------------------------------------------------
@app.callback(Output('EVpower', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_ev(n):
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
    return figure


#-------------------Battery---------------------------------------------------------------
@app.callback(Output('Hydrogen', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_hydrogen(n):
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
    return figure


#-------------------grid---------------------------------------------------------------
@app.callback(Output('gridpower', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live_load(n):
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
    return figure


#-------------------pie chart---------------------------------------------------------------
@app.callback(Output('piechart', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live_pie(n):
    tot_net = sumPositiveInts(dh['power_grid'])
    tot_pv = sum(dh['power_solar']) + tot_net * 0.05
    tot_wind = sum(dh['power_wind']) + tot_net* 0.08
    tot_gas = tot_net * 0.45
    tot_coal = tot_net * 0.32
    tot_oil = tot_net * 0.04
    tot_nuclear = tot_net * 0.03
    tot_other = tot_net * 0.03
    share = [tot_pv, tot_wind, tot_gas, tot_coal, tot_oil, tot_nuclear, tot_other]
    figure = go.Figure(data=[go.Pie(labels=labels, values=share)])
    figure.update_layout(
        title_text="Share of Total Energy Consumption")
    return figure


@app.callback(Output('piechartshare', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live_pie(n):
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
    share = [green, grey, other]
    figure = go.Figure(data=[go.Pie(labels=labels_2, values=share)])
    figure.update_layout(
        title_text="Green and grey ratio neigbourhood use")
    return figure

#-------------------emissions figure---------------------------------------------------------------
@app.callback(Output('emissions', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live_emissions(n):
    tot_net = sumPositiveInts(dh['power_grid'])
    tot_pv = sum(dh['power_solar']) + tot_net * 0.05
    tot_wind = sum(dh['power_wind']) + tot_net * 0.08
    tot_gas = tot_net * 0.45
    tot_coal = tot_net * 0.32
    tot_oil = tot_net * 0.04
    tot_nuclear = tot_net * 0.03
    tot_other = tot_net * 0.03
    tot_carbon = 0.2 * tot_net
    tot_methane = 0.1 * tot_net
    tot_nitrous = 0.05 * tot_net
    tot_fluor = 0.04 * tot_net

    labels1 = ['Carbon dioxide','Methane', 'Nitrous oxide','Fluorinated gases']
    share1 = [tot_carbon,tot_methane,tot_nitrous,tot_fluor,]

    labels2 = ['PV', 'Wind', 'Natural Gas', 'Coal', 'Oil', 'Nuclear', 'Other']
    share2 = [tot_pv, tot_wind, tot_gas, tot_coal, tot_oil, tot_nuclear, tot_other]


#------------------------MQTT--------------------------------------------------------------------

def connect_and_run_dash(client, N_EV):
    @app.callback(
        Output(component_id='output-pv', component_property='children'),
        [Input('button', 'n_clicks'), Input('buttonload', 'n_clicks'), Input('buttonev', 'n_clicks')],
        state=[State('dropdownpvtype', 'value'),State('input', 'value'), State('dropdown', 'value'),
               State('dropdownwind', 'value'),
               State('input load', 'value'), State('dropdownhousehold', 'value'),
               State('input EV', 'value')
               ], )
    def update_output(n_clicks, n_click, n_clickbat, paneltype ,panelvalue, tiltvalue, turbinetype, loadvalue, loadtype, evvalue):
        data.update({'pv_type': paneltype})
        data.update({'N_solar': panelvalue})
        data.update({'tilt_panel': tiltvalue})
        data.update({'turbine_type': turbinetype})
        data.update({'N_load': loadvalue})
        data.update({'load_type': loadtype})
        data.update({'N_EV': evvalue})
        client.publish("to_clients", json.dumps(data))
        global start
        start = time.time()
        N_EV.setValue(loadvalue)


    app.run_server(debug=False)


if __name__ == '__main__':
    app.run_server(debug=False)