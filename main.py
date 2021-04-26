
import pandas as pd
from plotly import graph_objects as go
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# Load geojson file
with open('data/regions.geojson', 'r') as f:
    france = eval(f.read())


# Load data
df = pd.read_csv('data/coviprevs_formatted.csv')
df = df.replace('Grand-Est', 'Grand Est').dropna()
targets = df.drop(['region', 'date'], axis=1).columns
df[targets] = df[targets]*100

translation = {'anxiete_target': 'Anxiété',
                'depression_target': 'Dépression',
                'pbsommeil_target': 'Problèmes de sommeil',
                'hyg4mes_target': 'Distanciation sociale',
                'portmasque_target': 'Port du masque'}
cibles = [{'label': l, 'value': v} for v, l in translation.items()]

ranges = {'anxiete_target': [0, 35],
            'depression_target': [0, 35],
            'pbsommeil_target': [45, 85],
            'hyg4mes_target': [15, 65],
            'portmasque_target': [0, 90]}


# Plot functions
def plot_map(cible):
    fig = go.Figure(data=go.Choropleth(
        locations=df['region'],
        z=df[cible],
        locationmode='geojson-id',
        geojson=france,
        featureidkey='properties.nom',
        hovertemplate="%{text}" "%{z}<extra></extra>",
        text=["<b>"+x+f"</b><br>{translation[cible]}:   " for x in df['region']],
        colorscale='Reds',
        colorbar_title=translation[cible],
    ))
    fig.update_geos(fitbounds="geojson", visible=False)
    return fig


# Build App
app = Dash(__name__)


# Build Layout
app.layout = html.Div([
    html.H1('CoviPrev par région'),
    html.Label([
        'Cible',
        dcc.Dropdown(
            id='cible-dropdown', clearable=False,
            value=cibles[0]['value'], options=cibles)
    ]),
    dcc.Graph(
        id='graph', 
        figure=plot_map(cibles[0]['value']),
        config={'displayModeBar': False, 'scrollZoom': False}),
])


# Define callback to update graph
@app.callback(Output('graph', 'figure'), 
                [Input('cible-dropdown', 'value')])
def update_figure(cible):
    return plot_map(cible)


# Run app and display result inline in the notebook
app.run_server()
