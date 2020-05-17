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
dh = {'power': [1, 2, 3]}
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
            html.Div('Number of PV panels'),
            dcc.Input(id='input', value=20, type='number'),
            html.Button('Refresh', id='button', n_clicks=0),
    dcc.Tab(label='Output', children=[
            html.Div(id='output-pv'),
            dcc.Graph(id='pvpower')
        ]),

        ]),
    ])
])


def dash_update_solar(dict):
    global dh
    dh.update(dict)

    print(dh)

@app.callback(Output('pvpower', 'figure'),
              [Input('button', 'n_clicks')],
                state=[State('input', 'value'),
               ],)
def update_graph_live(n, z):
    time.sleep(0.5)
    figure = {
        'data': [
            {'x': dh['time'], 'y': dh['power'], 'type': 'line', 'name': 'SF'}
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
        state=[State('input', 'value'),
               ],)
    def update_output(n_clicks, value):
        data.update({'N_solar': value})
        client.publish("to_clients", json.dumps(data))

    app.run_server(debug=False)


if __name__ == '__main__':
    app.run_server(debug=True)