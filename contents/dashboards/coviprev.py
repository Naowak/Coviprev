import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from contents.utils import colors, on_button_style, off_button_style



# Load data
data = pd.read_excel('data/coviprev22.xlsx', 
                            engine='openpyxl', 
                            sheet_name=None)

with open('data/france-regions.geojson', 'r') as f:
    france = eval(f.read())




# Prepare variables
targets = ['anxiete', 'depression', 'pbsommeil']
labels = ['Anxiété', 'Dépression', 'Problèmes de sommeil']
sentence1 = 'Part de la population {}'
sentence2 = 'Part de la population {} par {}'

# For regions
region_range = {target: [data['reg'][target].min(), data['reg'][target].max()] 
                                                        for target in targets}
region_title = {
    'anxiete': sentence2.format('étant anxieuse', 'région'),
    'depression': sentence2.format('étant dépressive', 'région'),
    'pbsommeil': sentence2.format('ayant des problèmes de sommeil', 'région')
}

# For age
age_title = {
    'anxiete': sentence2.format('étant anxieuse', 'tranche d\'âge'),
    'depression': sentence2.format('étant dépressive', 'tranche d\'âge'),
    'pbsommeil': sentence2.format('ayant des problèmes de sommeil', 'tranche d\'âge')  # noqa: E501
}


# For sexe
sexe_title = {
    'anxiete': sentence2.format('étant anxieuse', 'sexe'),
    'depression': sentence2.format('étant dépressive', 'sexe'),
    'pbsommeil': sentence2.format('ayant des problèmes de sommeil', 'sexe') 
}

# For france
fra_title = {
    'anxiete': sentence1.format('étant anxieuse'),
    'depression': sentence1.format('étant dépressive'),
    'pbsommeil': sentence1.format('ayant des problèmes de sommeil') 
}





# Functions
def plot_region(cible):
    fig = px.choropleth_mapbox(
        data['reg'], 
        geojson=france, 
        locations='region', 
        color='anxiete',
        featureidkey='properties.nom',
        mapbox_style="carto-positron",
        animation_frame='date',
        color_continuous_scale='Reds',
        range_color=region_range['anxiete'],
        opacity=0.5,
        zoom=4.5, 
        center={"lat": 46.71109, "lon": 1.7191036},
        title=region_title[cible],
        labels=dict(zip(targets, [label + ' (%)' for label in labels])))

    fig.update_traces(hovertemplate="<b>%{location}:</b> %{z}<extra></extra>")

    for frame in fig.frames:
        frame['data'][0]['hovertemplate'] = \
            "<b>%{location}:</b> %{z}<extra></extra>"
    
    fig.update_geos(fitbounds="geojson", visible=False)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        coloraxis=dict(zip(['cmin', 'cmax'], region_range['anxiete'])),
        height=700,
        width=1200)
    fig["layout"].pop("updatemenus")

    return fig


def plot_age(cible):
    return px.bar(data['age'], x='date', y=cible, 
                                    color='age', barmode='group')


def plot_sexe(cible):
    return px.bar(data['sexe'], x='date', y=cible, 
                                    color='sexe', barmode='group')


def plot_fra(cible):
    return px.bar(data['fra'], x='date', y=cible)





# Layout
coviprev_layout = html.Div([

    # Navbar
    html.Div([
        dbc.Navbar(
            [
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='assets/logo.png', height="50px")),
                        dbc.Col(dbc.NavbarBrand("Naowak", className="navbar-domain")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
            ],
            color=colors['dark'],
            dark=True,
        )
    ]),

    # Titre
    html.Div([
        html.H2(children='Visualisation des données Coviprev', className='title')
    ]),
    
    # Targets
    html.Div(
        [
            html.Div(
                [
                    html.Button(
                        children=v,
                        id='button-' + str(i), 
                        n_clicks=0,
                        style=on_button_style if i == 0 else off_button_style)
                    for i, v in enumerate(labels)
                ], className='targets'
            )
        ], className='row'
    ),

    # Map
    html.Div(
        [
            dcc.Graph(
                id='graph', 
                figure=plot_region(targets[0]),
                config={'displayModeBar': False, 'scrollZoom': False},
                className='map')
        ], className='row'
    )

])



# Dashboard


# def get_coviprev_dash(server):
#     app_coviprev.server = server
#     return app_coviprev




# # Callbacks
# @app_coviprev.callback(
#     [Output(f'button-{i}', 'style') for i in range(len(targets))]
#     + [Output('graph', 'figure')],
#     [Input(f'button-{i}', 'n_clicks') for i in range(len(targets))])
def update_target(*args):
    # Catch the target
    ctx = dash.callback_context
    if not ctx.triggered:
        index = 0
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        index = int(button_id[-1])

    # Indicate colors of buttons
    returns = []
    for i in range(len(targets)):
        if index == i:
            returns += [on_button_style]
        else:
            returns += [off_button_style]

    # Update figure values : 0.006s againt more than 1s to create new fig
    # values = get_values(targets[index])
    # fig.__dict__['_data_objs'][0]['z'] = values[0]
    # for i, val in enumerate(values):
    #     fig.__dict__['_frame_objs'][i]['data'][0]['z'] = val

    # crange = ranges[targets[index]]
    # fig.update_layout(coloraxis={'cmin': crange[0], 'cmax': crange[1]})

    # returns += [fig]
    returns += [plot_region(targets[index])]

    return returns
