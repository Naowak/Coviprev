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

ranges = {'anxiete_target': [8, 28],
            'depression_target': [5, 28],
            'pbsommeil_target': [52, 78],
            'hyg4mes_target': [23, 57],
            'portmasque_target': [9, 84]}

colors = {'background': '#F9F9F9', 
            'light': '#669DE6',
            'dark': '#293241',
            'show': '#E66666'}

titles = {'anxiete_target': 'Part de la population étant anxieuse par date et région',
            'depression_target': 'Part de la population étant dépressive par date et région',
            'pbsommeil_target': 'Part de la population ayant des problèmes de sommeil par date et région',
            'hyg4mes_target': 'Part de la population respectant les règles d\'hygiène par date et région',
            'portmasque_target': 'Part de la population respectant le port du masque par date et région'}


def get_values(cible):
    columns = [cible, 'date']
    df = coviprev[columns].groupby('date')[cible].apply(list)
    return df.values


# Plot functions
def plot_target(cible):
    # fig = px.choropleth(coviprev,
    #             geojson=france, 
    #             featureidkey='properties.nom',
    #             locations='region', 
    #             color=cible,
    #             animation_frame='date',
    #             title=titles[cible],
    #             labels=dict(zip(targets, [l + ' (%)' for l in labels])),
    #             color_continuous_scale=['#FFFFFF', colors['show']])
    fig = px.choropleth_mapbox(coviprev, geojson=france, locations='region', color='depression_target',
                            featureidkey='properties.nom',
                           color_continuous_scale='Reds',
                           range_color=(0, 0.5),
                           mapbox_style="carto-positron",
                           animation_frame='date',
                           zoom=4.5, center = {"lat": 46.71109, "lon": 1.7191036},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'})

    fig.update_traces(hovertemplate="<b>%{location}:</b> %{z}<extra></extra>")

    for frame in fig.frames:
        frame['data'][0]['hovertemplate'] = \
            "<b>%{location}:</b> %{z}<extra></extra>"
    
    fig.update_geos(fitbounds="geojson", visible=False)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    geo=dict(bgcolor='rgba(0,0,0,0)'),
                    coloraxis=dict(zip(['cmin', 'cmax'], ranges['anxiete_target'])),
                    height=700,
                    width=1200)
    fig["layout"].pop("updatemenus")

    return fig
