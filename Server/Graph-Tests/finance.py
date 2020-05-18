import pandas as pd
import plotly.graph_objects as go
import random

l = [random.randint(-2,10) for i in range(365)]

df = {'weekly profit':l}
df.update({'time': pd.date_range(start='2019-01-01', freq='1d', periods=365)})


fig = go.Figure(go.Bar(
            x=df['time'],
            y=df['weekly profit']
            ))
fig.show()
#print(df)
