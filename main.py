from flask import Flask
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from contents.dashboards.coviprev import coviprev_layout, update_target, targets

# Build App

server = Flask(__name__)

# app_coviprev = get_coviprev_dash(server)
# app_coviprev.server = server
stylesheets = [dbc.themes.BOOTSTRAP, 
              'https://codepen.io/chriddyp/pen/bWLwgP.css']
app_coviprev = dash.Dash(__name__,
                        server=server, 
                        external_stylesheets=stylesheets)
app_coviprev.layout = coviprev_layout

# Routes pages
@server.route("/coviprev")
def show_coviprev_dash():
    return app_coviprev.index()

@app_coviprev.callback(
    [Output(f'button-{i}', 'style') for i in range(len(targets))]
    + [Output(f'graph-{crit}', 'figure') 
                    for crit in ['region', 'fra', 'sexe', 'age']],
    [Input(f'button-{i}', 'n_clicks') for i in range(len(targets))])
def coviprev_update(*args):
    return update_target(*args)


if __name__ == '__main__':
    # Run app and display result inline in the notebook
    server.run()
