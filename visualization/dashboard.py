import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
import os

# Create a Dash app
app = Dash(__name__)

current_file_path = os.path.abspath(__file__)

files = os.listdir(os.getcwd()+'/visualization/data')
files = [file for file in files if file.endswith('.csv')]

data = pd.concat([pd.read_csv(f'visualization/data/{file}') for file in files])

# Define the layout
app.layout = html.Div([
    # Title Room rental market in Barcelona
    html.H1('Room rental market in Barcelona'),
    # Basic main data: number of cases, min price, max price, average price and median price
    html.Div([
        html.Div([
            html.H2('Number of cases'),
            html.H3(data.shape[0])
        ]),
        html.Div([
            html.H2('Min price'),
            html.H3(data['price'].min())
        ]),
        html.Div([
            html.H2('Max price'),
            html.H3(data['price'].max())
        ]),
        html.Div([
            html.H2('Average price'),
            html.H3(data['price'].mean())
        ]),
        html.Div([
            html.H2('Median price'),
            html.H3(data['price'].median())
        ]),
    ])

])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)