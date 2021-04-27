import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from dataloader import plot_target, targets, labels, colors


# Build App
app = dash.Dash(__name__, 
        external_stylesheets=[dbc.themes.BOOTSTRAP,
                            'https://codepen.io/chriddyp/pen/bWLwgP.css'])


# Build Layout
app.layout = html.Div([

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

    html.Div([
        html.H2(children='Visualisation des données Coviprev', className='title')
    ]),
        
    html.Div([
        dbc.ListGroup(
            [dbc.ListGroupItem(
                children=v,
                id='item-' + str(i), 
                n_clicks=0,
                color=colors['light'] if i == 0 else colors['dark']) 
            for i, v in enumerate(labels)], 
            horizontal=True,
            className='targets'
        )
    ], className='row'),

    html.Div([
        dcc.Graph(
            id='graph', 
            figure=plot_target(targets[0]),
            config={'displayModeBar': False, 'scrollZoom': False},
            className='map')
    ], className='row')

])


# Define callback to update the target
@app.callback([Output(f'item-{i}', 'color') for i in range(len(targets))]
                + [Output('graph', 'figure')],
            [Input(f'item-{i}', 'n_clicks') for i in range(len(targets))])
def update_target(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        index = 0
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        index = int(button_id[-1])

    returns = []
    for i in range(len(targets)):
        if index == i:
            returns += [colors['light']]
        else:
            returns += [colors['dark']]

    returns += [plot_target(targets[index])]

    return returns 


# Run app and display result inline in the notebook
app.run_server()
