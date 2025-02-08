import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from pages import detection, education, problem, video  # Import problem module

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
                dbc.NavItem(dbc.NavLink("The Problem", href="/")),  # Fixed href
                dbc.NavItem(dbc.NavLink("Image Detection", href="/detection")),
                dbc.NavItem(dbc.NavLink("Video Detection", href="/video")),
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
    html.Div(id='page-content', style={"margin-top": "80px"}),  # Added margin to avoid overlap with navbar
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/detection':
        return detection.layout
    elif pathname == '/':
        return problem.layout  # Fixed problem page navigation
    elif pathname == '/education':
        return education.layout
    elif pathname == '/video':
        return video.layout
    else:
        return html.Div([
            html.H1("Home"),
            html.P("Welcome to AquaEye.")
        ])

detection.register_callbacks(app)
video.register_callbacks(app)  # Register video callbacks

if __name__ == '__main__':
    app.run_server(debug=True)