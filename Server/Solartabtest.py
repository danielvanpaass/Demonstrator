import json
import plotly.express as px
import pandas as pd
import time

import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import base64

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
    dcc.Input(id='input load', value=160, type='number'),
    html.Button('Refresh', id='buttonload', n_clicks=0),
    html.Div(id='output-pv'),
    dcc.Graph(id='pvpower'),
    dcc.Graph(id='loadpower')
])


def dash_update_solar(dict):
    global dh
    dh.update(dict)


@app.callback(Output('pvpower', 'figure'),
              [Input('button', 'n_clicks')],
              state=[State('input', 'value'),
                     State('dropdown', 'value')
                     ])
def update_graph_live(n, z, k):
    time.sleep(0.5)
    figure = {
        'data': [
            {'x': dh['time'], 'y': dh['power_solar'], 'type': 'line', 'name': 'PV'}
        ],
        'layout': {
            'title': ' Power output'
        }
    }
    return figure


@app.callback(Output('loadpower', 'figure'),
              [Input('buttonload', 'n_clicks')],
              state=[State('input load', 'value')
                     ])
def update_graph_live_load(n, z, ):
    time.sleep(0.5)
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
        [Input('button', 'n_clicks'), Input('buttonload', 'n_clicks')],
        state=[State('input', 'value'), State('dropdown', 'value'), State('input load', 'value')
               ], )
    def update_output(n_clicks,n_click, panelvalue, tiltvalue, loadvalue):
        data.update({'N_solar': panelvalue})
        data.update({'tilt_panel': tiltvalue})
        data.update({'N_load': loadvalue})
        client.publish("to_clients", json.dumps(data))

    app.run_server(debug=False)


if __name__ == '__main__':
    app.run_server(debug=False)