import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from dataloader import plot_target, targets, labels, colors, get_values, ranges


# Build App
external_stylesheets = [dbc.themes.BOOTSTRAP,
                        'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, 
                external_stylesheets=external_stylesheets)

fig = plot_target(targets[0])

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
            figure=fig,
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
    app.run_server(host='0.0.0.0', port=14000)
