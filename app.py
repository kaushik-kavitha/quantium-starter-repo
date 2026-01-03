import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Load the processed data
df = pd.read_csv('formatted_pink_morsel_data.csv')

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Sort by date
df = df.sort_values('date')

# Group by date and sum sales
daily_sales = df.groupby('date')['sales'].sum().reset_index()

# Create the Dash app
app = dash.Dash(__name__)

# Create the figure
fig = px.line(
    daily_sales,
    x='date',
    y='sales',
    title='Daily Sales of Pink Morsel Over Time',
    labels={
        'date': 'Date',
        'sales': 'Sales ($)'
    },
    markers=True
)

# Add vertical line for price increase using shapes
fig.add_shape(
    type='line',
    x0='2021-01-15',
    y0=0,
    x1='2021-01-15',
    y1=1,
    xref='x',
    yref='paper',
    line=dict(color='red', width=2, dash='dash')
)

fig.add_annotation(
    x='2021-01-15',
    y=1,
    yref='paper',
    text='Price Increase (Jan 15, 2021)',
    showarrow=False,
    yanchor='bottom'
)

# Define the app layout
app.layout = html.Div([
    html.H1("Pink Morsel Sales Analysis", style={'textAlign': 'center', 'marginBottom': 30, 'marginTop': 20}),
    
    html.Div([
        dcc.Graph(
            id='sales-chart',
            figure=fig
        )
    ], style={'padding': '20px'})
])

if __name__ == '__main__':
    app.run(debug=True)
