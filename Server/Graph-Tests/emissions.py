import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html

Sources=['Solar', 'Wind', 'Battery']

fig = go.Figure(data=[
    go.Bar(name='GHG', x=Sources, y=[52.7, 17.5, 69])
#    go.Bar(name='', x=animals, y=[12, 18, 29])
])
# Change the bar mode
fig.update_layout(barmode='stack')
fig.show()

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False) 


