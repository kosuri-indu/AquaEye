from dash import html, dcc

layout = html.Div([
    # Video container with text overlay and gradient
    html.Div(
        [
            # Video with reduced height
            html.Video(
                src="https://assets.theoceancleanup.com/videos/home-header-720p-v3.webm",
                poster="https://assets.theoceancleanup.com/videos/home-header-poster-v2.jpg",
                autoPlay=True,
                loop=True,
                muted=True,
                style={
                    'width': '100%',
                    'height': '550px',
                    'object-fit': 'cover',
                    'display': 'block'
                }
            ),

            # Transparent overlay for text
            html.Div(
                [
                    html.H2("AQUAEYE",
                            style={
                                'font-size': '75px',
                                'font-family': 'Georgia, serif',
                                'color': 'white',
                                'position': 'absolute',
                                'top': '30%',
                                'left': '5%',
                                'padding': '10px',
                                'border-radius': '5px'
                            }),

                    html.H3("Every piece of plastic removed is a piece less in nature.",
                            style={
                                'font-size': '30px',
                                'font-family': 'Arial, sans-serif',
                                'color': 'white',
                                'position': 'absolute',
                                'top': '50%',
                                'left': '5%',
                                'padding': '10px',
                                'border-radius': '5px'
                            })
                ],
                style={
                    'position': 'absolute',
                    'top': '0',
                    'left': '0',
                    'width': '100%',
                    'height': '100%',
                    'zIndex': '2'
                }
            ),

            # Overlapping gradient using #003755
            html.Div(style={
                'position': 'absolute',
                'bottom': '0',
                'left': '0',
                'width': '100%',
                'height': '40%',
                'background': 'linear-gradient(to bottom, rgba(0, 55, 85, 0), #003755)',
                'zIndex': '3'
            })
        ],
        style={'position': 'relative', 'textAlign': 'left'}
    ),

    # Feature Section (Equal-sized Cards)
    html.Div(
        [
            html.Div([
                html.Img(src="static/images/highdetect.png", className="feature-img"),
                html.Div("High Precision Detection", className="feature-text")
            ], className="feature-card"),

            html.Div([
                html.Img(src="static/images/visuvalise.png", className="feature-img"),
                html.Div("Data Visualization", className="feature-text")
            ], className="feature-card"),

            html.Div([
                html.Img(src="static/images/realtime.png", className="feature-img"),
                html.Div("Real-time Processing", className="feature-text")
            ], className="feature-card"),
        ],
        style={
            'display': 'flex',
            'justifyContent': 'space-evenly',  # Distribute cards equally
            'alignItems': 'center',
            'gap': '15px',
            'padding': '30px 0'
        }
    )
], style={'backgroundColor': '#003755', 'minHeight': '100vh'})  # Set full background color

# CSS for feature cards (Equal sizes)
feature_card_style = {
    'width': '300px',  # Ensure equal width
    'height': '400px',
    'borderRadius': '10px',
    'overflow': 'hidden',
    'position': 'relative',
    'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.2)',
    'display': 'flex',
    'flexDirection': 'column',
    'alignItems': 'center'
}

feature_img_style = {
    'width': '100%',
    'height': '80%',  # Adjust image height
    'objectFit': 'cover',
    'position': 'relative'
}

feature_text_style = {
    'width': '100%',
    'height': '20%',  # Text at bottom
    'padding': '15px',
    'background': 'linear-gradient(to top, black, rgba(0, 0, 0, 0.6))',
    'color': 'white',
    'textAlign': 'center',
    'fontSize': '18px',
    'fontFamily': 'Arial, sans-serif',
    'display': 'flex',
    'alignItems': 'center',
    'justifyContent': 'center'
}

# Apply styles dynamically
for feature in layout.children[1].children:
    feature.style = feature_card_style
    feature.children[0].style = feature_img_style
    feature.children[1].style = feature_text_style
