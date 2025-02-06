import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

from pages import detection, education, problem  # Import the problem module

# Initialize the app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Define the navbar
navbar = dbc.Navbar(
    dbc.Container([
        # Logo on the left
        html.A(
            html.Img(src="/static/images/logo.png", height="60px"),
            href="/",
            className="navbar-brand",
        ),
        
        # Navigation links on the right
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("The Problem", href="/problem")),
                dbc.NavItem(dbc.NavLink("Debris Detection", href="/detection")),
                dbc.NavItem(dbc.NavLink("Education", href="/education")),
            ],
            className="ms-auto",  # Pushes items to the right
            navbar=True,
        ),
    ]),
    color="dark",
    dark=True,
    fixed="top",
)

# Define the layout with a placeholder content area
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/detection':
        return detection.layout
    elif pathname == '/problem':
        return problem.layout  # Use the layout defined in problem.py
    elif pathname == '/education':
        return education.layout  # Use the layout defined in education.py
    else:
        return html.Div([html.H1("Home"), html.P("Welcome to AquaEye.")])

detection.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)