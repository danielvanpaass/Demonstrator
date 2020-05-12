import plotly.express as px
import pandas as pd

#import PV and convert to prefered form (JSON)
dg = pd.read_csv ('Time-Load-PV-Wind.csv')                       #read values from csv file
dg.to_json ('Time-Load-PV-Wind.json')                            #convert values to json file

#Generation Graphs
PV    = px.line(dg, x = 'Date', y = 'PV Power [KW]', title='Generated PV Power in 2019')
Wind  = px.line(dg, x = 'Date', y = 'Wind Power [KW]', title='Generated Wind in 2019')
Load  = px.line(dg, x = 'Date', y = 'Load [KW]', title='Residential Load in 2019')

import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)

app.layout = html.Div([
        dcc.Tabs([
            dcc.Tab(label='Input Parameters', children=[
                html.Div('Number of PV panels'),
                dcc.Input(id='input', value='20', type='number'),
                html.Button('Refresh',id='button', n_clicks=0),
            
            
        ]),
            dcc.Tab(label='Output', children=[
            html.Div(id='output-pv'),
                dcc.Graph(figure=PV),
                dcc.Graph(figure=Wind),
                dcc.Graph(figure=Load),
           
            
        ]),
        
    ])
])

@app.callback(
    Output(component_id='output-pv', component_property='children'),
    [Input('button', 'n_clicks')],
    state=[State('input', 'value'),
           ])

def update_output(n_clicks, value):
    return 'Data for neighbourhood when using {} PV panels'.format(value)
    

    

if __name__ == '__main__':
    app.run_server(debug=True)