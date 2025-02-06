import dash_html_components as html

layout = html.Div([
    html.H1("Education"),
    html.Img(src="/static/images/education_banner.png", style={'width': '100%', 'height': '500px'}),
    html.Div(
        [
            html.P(
                html.B("How does plastic enter the ocean?"),
                style={'font-size': '45px', 'font-family': 'Open Sans', 'text-align': 'center'}
            ),
            html.P(
                [
                    "Plastic usage and waste management infrastructures differ all over the world. Only ",
                    html.Span("9%", style={'font-size': '24px', 'font-weight': 'bold', 'color': 'darkred'}),
                    " gets recycled, and about ",
                    html.Span("22%", style={'font-size': '24px', 'font-weight': 'bold', 'color': 'darkred'}),
                    " of plastic waste worldwide is either not collected, improperly disposed of, or ends up as litter. People in high income countries consume the most plastic, but the waste management systems there are usually effective – meaning that even though there’s a lot of plastic around, it is mostly kept out of the natural environment. Meanwhile, lower income countries often consume less plastic, meaning emissions from these countries remain low even if the local waste management infrastructure is lacking."
                ],
                style={'font-size': '20px', 'font-family': 'Open Sans', 'text-align': 'center', 'padding-top': '20px', 'padding-left': '160px', 'padding-right': '160px', 'padding-bottom': '25px'}
            ),
            html.Img(src="/static/images/plastic_journey.png", style={'width': '80%', 'height': '2000px', 'display': 'block', 'margin': '0 auto', 'margin-top': '0'}),
            html.Img(src="/static/images/edu_footer.png", style={'width': '100%', 'height': '2000px', 'display': 'block', 'margin': '0 auto', 'margin-top': '0'})
        ],
        style={'width': '100%', 'height': '500px', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'padding-top': '25px'}
    )
])