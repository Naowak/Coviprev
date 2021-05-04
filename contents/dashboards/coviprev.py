import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import textwrap

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
legends = ['' for _ in range(len(targets))]

sentence1 = 'Part de la population {} en %'
sentence2 = 'Part de la population {} par {} en %'

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
def get_values(criterion, cible):
    columns = [cible, 'date']
    df = data[criterion][columns].groupby('date')[cible].apply(list)
    return df.values


def plot_region(cible):
    fig_region = px.choropleth_mapbox(
        data['reg'], 
        geojson=france, 
        locations='region', 
        color=cible,
        featureidkey='properties.nom',
        mapbox_style="carto-positron",
        animation_frame='date',
        color_continuous_scale='Reds',
        range_color=region_range[cible],
        opacity=0.5,
        zoom=4.5, 
        center={"lat": 46.71109, "lon": 1.7191036},
        labels=dict(zip(targets, legends)))

    fig_region.update_traces(
        hovertemplate="<b>%{location}:</b> %{z}<extra></extra>")

    for frame in fig_region.frames:
        frame['data'][0]['hovertemplate'] = \
            "<b>%{location}:</b> %{z}<extra></extra>"
    
    fig_region.update_geos(fitbounds="geojson", visible=False)

    fig_region.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        title=age_title[cible],
        height=700,
        width=900)


    return fig_region


def update_region(cible):
    # Update figure values : 0.006s againt more than 1s to create new fig
    values = get_values('reg', cible)
    fig_region.__dict__['_data_objs'][0]['z'] = values[0]
    for i, val in enumerate(values):
        fig_region.__dict__['_frame_objs'][i]['data'][0]['z'] = val

    crange = region_range[cible]
    fig_region.update_layout(
        coloraxis={'cmin': crange[0], 'cmax': crange[1]},
        title=region_title[cible])

    return fig_region


def plot_age(cible):
    fig_age = px.bar(data['age'], x='date', y=cible, 
                                    color='age', barmode='group')
    fig_age.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        title=age_title[cible],
        legend={'title': ''},
        xaxis={'title': ''},
        yaxis={'title': ''},
        height=300,
        width=900)

    return fig_age


def plot_sexe(cible):
    fig_sexe = px.bar(data['sexe'], x='date', y=cible, 
                                    color='sexe', barmode='group')

    fig_sexe.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        title=sexe_title[cible],
        legend={'title': ''},
        xaxis={'title': ''},
        yaxis={'title': ''},
        height=300,
        width=900)

    return fig_sexe



def plot_fra(cible):
    fig_fra = px.bar(data['fra'], x='date', y=cible)

    fig_fra.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        title=fra_title[cible],
        xaxis={'title': ''},
        yaxis={'title': ''},
        height=300,
        width=900)

    return fig_fra





# Layout
fig_region = plot_region(targets[0])
fig_age = plot_age(targets[0])
fig_sexe = plot_sexe(targets[0])
fig_fra = plot_fra(targets[0])


coviprev_layout = html.Div([

    # Navbar
    html.Div([
        dbc.Navbar(
            [
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='assets/logo.png', height="50px")),
                        dbc.Col(dbc.NavbarBrand(
                            "Naowak  |  Visualisation des données Coviprev", 
                            className="navbar-domain")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
            ],
            color=colors['dark'],
            dark=True,
        )
    ]),
    
    # Graphs
    html.Div(
        [   
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
                    ),

                    html.Div(
                        [
                            dcc.Graph(
                                id='graph-region', 
                                figure=fig_region,
                                config={'displayModeBar': False, 'scrollZoom': False},
                                className='map')
                        ], className='row'
                    )

                ], className='col'),

            html.Div(
                [
                    dcc.Graph(
                        id='graph-fra', 
                        figure=fig_fra,
                        config={'displayModeBar': False, 'scrollZoom': False},
                        className='barchart'),

                    dcc.Graph(
                        id='graph-sexe',
                        figure=fig_sexe,
                        config={'displayModeBar': False, 'scrollZoom': False},
                        className='barchart'),

                    dcc.Graph(
                        id='graph-age',
                        figure=fig_age,
                        config={'displayModeBar': False, 'scrollZoom': False},
                        className='barchart')

                ], className='col')

        ], className='row'
    )

])



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

    # Update figures
    cible = targets[index]

    returns += [update_region(cible)]
    returns += [plot_fra(cible)]
    returns += [plot_sexe(cible)]
    returns += [plot_age(cible)]

    return returns
