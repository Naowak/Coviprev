from flask import Flask
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from dataloader import plot_target, targets, labels, colors, get_values, ranges


# Build App
external_stylesheets = [dbc.themes.BOOTSTRAP,
                        'https://codepen.io/chriddyp/pen/bWLwgP.css']

server = Flask(__name__)

app = dash.Dash(__name__, 
                server=server,
                external_stylesheets=external_stylesheets)

fig = plot_target(targets[0])



# Build Layout
off_button_style = {'background-color': colors['dark'],
                      'color': 'white',
                      'height': '50px'}

on_button_style = {'background-color': colors['light'],
                    'color': 'white',
                    'height': '50px'}

app.layout = html.Div([

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
                figure=fig,
                config={'displayModeBar': False, 'scrollZoom': False},
                className='map')
        ], className='row'
    )

])


# Define callback to update the target
@app.callback([Output(f'button-{i}', 'style') for i in range(len(targets))]
            + [Output('graph', 'figure')],
            [Input(f'button-{i}', 'n_clicks') for i in range(len(targets))])
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
    values = get_values(targets[index])
    fig.__dict__['_data_objs'][0]['z'] = values[0]
    for i, val in enumerate(values):
        fig.__dict__['_frame_objs'][i]['data'][0]['z'] = val

    crange = ranges[targets[index]]
    fig.update_layout(coloraxis={'cmin': crange[0], 'cmax': crange[1]})

    returns += [fig]

    return returns


if __name__ == '__main__':
    # Run app and display result inline in the notebook
    server.run()
