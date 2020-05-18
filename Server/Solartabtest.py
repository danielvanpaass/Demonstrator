import json

import plotly.express as px
import pandas as pd
import time



import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import base64
data_change = False
data = {}
dh = {'power_solar': [1, 2, 3]}
dh.update({'time': pd.date_range(start='2019-01-01 00:00', freq='1h', periods=8760)})
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
colors = {
    'background': '#111111',
    'text': '#00A6D6'
}
test_png = 'TUD.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

app.layout = html.Div([
    html.H1(
        children='Energy System Integrator Demonstrator',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ), html.Img(src='data:image/png;base64,{}'.format(test_base64)),
    dcc.Tabs([
        dcc.Tab(label='Input Parameters', children=[
            html.Button('Refresh', id='button', n_clicks=0),
            html.Div('PV Parameters'),
            dcc.Input(id='input', value=20, type='number'),
            dcc.Dropdown(
                    id='dropdown',
                    options=[
                        {'label': '30 degrees tilt', 'value': 30},
                        {'label': '35 degrees tilt', 'value': 35},
                        {'label': '40 degrees tilt', 'value': 40}
                    ],
                    value=30
    ),      html.Div('Load Parameters'),
            dcc.Input(id='input load', value=160, type='number'),
    dcc.Tab(label='Output', children=[
            html.Div(id='output-pv'),
            dcc.Graph(id='pvpower'),
            dcc.Graph(id='loadpower')
        ]),

        ]),
    ])
])


def dash_update_solar(dict):
    global dh, data_change
    dh.update(dict)
    data_change = True

@app.callback(Output('pvpower', 'figure'),
              [Input('button', 'n_clicks')],
                state=[State('input', 'value'),
                       State('dropdown','value')
               ],
              )
def update_graph_live(n, z, k):
    global data_change
    while(data_change == False):
        pass
    data_change = False
    figure = {
        'data': [
            {'x': dh['time'], 'y': dh['power_solar'], 'type': 'line', 'name': 'SF'}
        ],
        'layout': {
            'title': ' Power output'
        }
    }
    return figure

@app.callback(Output('loadpower', 'figure'),
              [Input('button', 'n_clicks')],
                state=[State('input load', 'value')
               ],
              )
def update_graph_live_load(n, z,):
    global data_change
    while(data_change == False):
        pass
    data_change = False
    figure = {
        'data': [
            {'x': dh['time'], 'y': dh['power_load'], 'type': 'line', 'name': 'load'}
        ],
        'layout': {
            'title': ' Power output'
        }
    }
    return figure


def connect_and_run_dash(client):
    @app.callback(
        Output(component_id='output-pv', component_property='children'),
        [Input('button', 'n_clicks')],
        state=[State('input', 'value'), State('dropdown','value'), State('input load','value')
               ],)
    def update_output(n_clicks, panelvalue, tiltvalue, loadvalue):
        data.update({'N_solar': panelvalue})
        data.update({'tilt_panel': tiltvalue})
        data.update({'N_load': loadvalue})
        client.publish("to_clients", json.dumps(data))

    app.run_server(debug=False)



if __name__ == '__main__':
    app.run_server(debug=False)