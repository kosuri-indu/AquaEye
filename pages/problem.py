import dash_html_components as html
import dash_core_components as dcc

layout = html.Div([
    html.H1("Problem"),
    html.P("This page explains the problem of underwater debris."),
    html.Div(
        [
            html.Img(src="/static/images/prob_i1.png", style={'width': '100%', 'height': '750px','padding-top': '0px'}),
            html.Button("Learn More", id="learn-more-button", style={
                'position': 'absolute', 'top': '70%', 'left': '50%', 'transform': 'translate(-50%, -50%)',
                'background-color': 'rgba(255, 255, 255, 0.7)', 'border': 'none', 'padding': '10px 20px',
                'font-size': '16px', 'cursor': 'pointer'
            })
        ],
        style={'position': 'relative', 'width': '100%', 'height': 'auto', 'text-align': 'center'}
    )
])