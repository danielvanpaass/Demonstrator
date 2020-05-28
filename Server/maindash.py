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
      'power_load': [1, 2, 3],}

labels=['PV','Wind','Natural Gas','Coal','Oil','Nuclear','Other']


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
    html.Div(id='output-pv'),
    dcc.Graph(id='pvpower'),
    dcc.Graph(id='loadpower'),
    dcc.Graph(id='piechart'),
    dcc.Graph(id='emissions')

])


def dash_update_solar(dict):
    global dh
    dh.update(dict)
    end = time.time()
    print(end - start)

#-------------------pv figure---------------------------------------------------------------
@app.callback(Output('pvpower', 'figure'),
              [Input('button', 'n_clicks')],
              state=[State('input', 'value'),
                     State('dropdown', 'value')
                     ])
def update_graph_live(n, z, k):
    time.sleep(1.3)#1.3 needed for the pi, (pi exe time is 1.1)
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

#-------------------load figure---------------------------------------------------------------
@app.callback(Output('loadpower', 'figure'),
              [Input('buttonload', 'n_clicks')],
              state=[State('input load', 'value'),
                     State('dropdownhousehold', 'value')
                     ])
def update_graph_live_load(n, z, k):
    time.sleep(0.6)
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


#-------------------pie chart---------------------------------------------------------------
@app.callback(Output('piechart', 'figure'),
              [Input('buttonload', 'n_clicks'), Input('button', 'n_clicks')])
def update_graph_live_pie(n, z,):
    time.sleep(0.6)
    dx=({'wind': [10000, 2, 5, 3, 2, 0],
    'net': [100000, 2, 5, 0, 2, 0]})
    tot_net = sum(dx['net'])
    tot_pv = sum(dh['power_solar']) + tot_net * 0.05
    tot_wind = sum(dx['wind']) * 0.08
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


#-------------------emissions figure---------------------------------------------------------------
@app.callback(Output('emissions', 'figure'),
              [Input('buttonload', 'n_clicks'), Input('button', 'n_clicks')])
def update_graph_live_emissions(n, z,):
    time.sleep(0.6)
    dx=({'wind': [10000, 2, 5, 3, 2, 0],
    'net': [100000, 2, 5, 0, 2, 0]})
    tot_net = sum(dx['net'])
    tot_pv = sum(dh['power_solar']) + tot_net * 0.05
    tot_wind = sum(dx['wind']) * 0.08
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
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "bar"}]])

    fig.add_trace(go.Bar(name='Greenhouse gases [kg]',
                         x=labels1, y=share1,
                         ),
                  row=1, col=1)
    fig.update_layout(
        title_text="Lifecycle Emission Analysis",
        xaxis_title=" ",
        yaxis_title="[kg]")
    fig.add_trace(go.Bar(name='Carbon dioxide [kg]',
                         x=labels2, y=share2,
                         ),
                  row=1, col=2,)
    return fig


#------------------------MQTT--------------------------------------------------------------------

def connect_and_run_dash(client):
    @app.callback(
        Output(component_id='output-pv', component_property='children'),
        [Input('button', 'n_clicks'), Input('buttonload', 'n_clicks')],
        state=[State('input', 'value'), State('dropdown', 'value'), State('input load', 'value'), State('dropdownhousehold', 'value')
               ], )
    def update_output(n_clicks,n_click, panelvalue, tiltvalue, loadvalue, loadtype):
        data.update({'N_solar': panelvalue})
        data.update({'tilt_panel': tiltvalue})
        data.update({'N_load': loadvalue})
        data.update({'load_type': loadtype})
        client.publish("to_clients", json.dumps(data))
        global start
        start = time.time()


    app.run_server(debug=False)


if __name__ == '__main__':
    app.run_server(debug=False)