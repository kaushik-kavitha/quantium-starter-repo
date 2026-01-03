import dash
from dash import dcc, html, callback, Input, Output
import plotly.express as px
import pandas as pd

# Load the processed data
df = pd.read_csv('formatted_pink_morsel_data.csv')

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Create the Dash app
app = dash.Dash(__name__)

# Define external CSS for additional styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {{
                fontFamily: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                minHeight: 100vh;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 20px;
                textAlign: center;
                boxShadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .container {{
                maxWidth: 1200px;
                margin: 0 auto;
                backgroundColor: white;
                borderRadius: 10px;
                boxShadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                margin: 30px auto;
                padding: 40px;
            }}
            .filter-section {{
                marginBottom: 30px;
                padding: 20px;
                backgroundColor: #f8f9fa;
                borderRadius: 8px;
                borderLeft: 5px solid #667eea;
            }}
            .filter-label {{
                fontSize: 18px;
                fontWeight: 600;
                color: #333;
                marginBottom: 15px;
                display: block;
            }}
            .radio-options {{
                display: flex;
                flexWrap: wrap;
                gap: 20px;
            }}
            h1 {{
                margin: 0;
                fontSize: 48px;
                fontWeight: 700;
                textShadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .subtitle {{
                fontSize: 16px;
                marginTop: 10px;
                opacity: 0.95;
            }}
            #sales-chart {{
                borderRadius: 8px;
                marginTop: 20px;
            }}
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Define the app layout
app.layout = html.Div([
    html.Div([
        html.H1("Pink Morsel Sales Analysis", style={'margin': 0}),
        html.Div("Analyzing regional sales trends before and after the January 15, 2021 price increase", 
                 className='subtitle')
    ], className='header'),
    
    html.Div([
        html.Div([
            html.Label('Filter by Region:', className='filter-label'),
            dcc.RadioItems(
                id='region-filter',
                options=[
                    {'label': ' All Regions', 'value': 'all'},
                    {'label': ' North', 'value': 'north'},
                    {'label': ' East', 'value': 'east'},
                    {'label': ' South', 'value': 'south'},
                    {'label': ' West', 'value': 'west'},
                ],
                value='all',
                className='radio-options',
                inline=False,
                style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px'}
            )
        ], className='filter-section'),
        
        dcc.Graph(id='sales-chart')
    ], className='container')
])

# Callback to update the chart based on selected region
@callback(
    Output('sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(selected_region):
    # Filter data based on selected region
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]
    
    # Group by date and sum sales
    daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()
    daily_sales = daily_sales.sort_values('date')
    
    # Create the figure
    fig = px.line(
        daily_sales,
        x='date',
        y='sales',
        title=f'Daily Sales of Pink Morsel - {selected_region.upper()} Region',
        labels={
            'date': 'Date',
            'sales': 'Sales ($)'
        },
        markers=True,
        line_shape='spline'
    )
    
    # Customize the figure
    fig.update_traces(
        line=dict(color='#667eea', width=3),
        marker=dict(size=6, color='#764ba2')
    )
    
    # Add vertical line for price increase
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
        yanchor='bottom',
        font=dict(color='red', size=12)
    )
    
    # Update layout for better appearance
    fig.update_layout(
        hovermode='x unified',
        template='plotly_white',
        font=dict(family='Segoe UI, sans-serif', size=12),
        title_font_size=20,
        xaxis_title_font_size=14,
        yaxis_title_font_size=14,
        height=500,
        margin=dict(l=80, r=40, t=80, b=60)
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)
