import pandas as pd
import plotly.express as px

# Load geojson file
with open('data/regions.geojson', 'r') as f:
    france = eval(f.read())

# Load data
coviprev = pd.read_csv('data/coviprevs_formatted.csv')
targets = coviprev.drop(['region', 'date'], axis=1).columns
coviprev[targets] = coviprev[targets]*100

targets = ['anxiete_target', 'depression_target', 'pbsommeil_target', 
                                    'hyg4mes_target', 'portmasque_target']
labels = ['Anxiété', 'Dépression', 'Problèmes de sommeil', 
                                'Distanciation sociale', 'Port du masque']

ranges = {'anxiete_target': [0, 35],
            'depression_target': [0, 35],
            'pbsommeil_target': [45, 85],
            'hyg4mes_target': [15, 65],
            'portmasque_target': [0, 90]}

colors = {'background': '#F9F9F9', 
            'light': '#669DE6',
            'dark': '#293241',
            'show': '#E66666'}

titles = {'anxiete_target': 'Part de la population étant anxieuse par date et région',
            'depression_target': 'Part de la population étant dépressive par date et région',
            'pbsommeil_target': 'Part de la population ayant des problèmes de sommeil par date et région',
            'hyg4mes_target': 'Part de la population respectant les règles d\'hygiène par date et région',
            'portmasque_target': 'Part de la population respectant le port du masque par date et région'}


# Plot functions
def plot_target(cible):
    fig = px.choropleth(coviprev,
                geojson=france, 
                featureidkey='properties.nom',
                locations='region', 
                color=cible,
                animation_frame='date',
                title=titles[cible],
                labels=dict(zip(targets, [l + ' (%)' for l in labels])),
                color_continuous_scale=['#FFFFFF', colors['show']], 
                range_color=ranges[cible])

    fig.update_traces(hovertemplate="<b>%{location}:</b> %{z}<extra></extra>")

    for frame in fig.frames:
        frame['data'][0]['hovertemplate'] = \
            "<b>%{location}:</b> %{z}<extra></extra>"
    
    fig.update_geos(fitbounds="geojson", visible=False)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    geo=dict(bgcolor='rgba(0,0,0,0)'),
                    height=700,
                    width=1200)
    fig["layout"].pop("updatemenus")

    return fig