import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State
import os
import base64

# Define the layout for the detection page
layout = html.Div([
    html.H2("Debris Detection"),
    
    # File Upload Component with plus symbol
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                html.H1("+", style={'fontSize': '50px', 'marginBottom': '10px'}),
            ], style={
                'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100%'
            }),
            style={
                'width': '95.5%', 'height': '20rem', 'lineHeight': '60px',
                'borderWidth': '2px', 'borderStyle': 'dashed', 'borderRadius': '10px',  
                'textAlign': 'center', 'margin': '7rem 2rem 2rem 2rem', 'padding': '20px', 
                'backgroundColor': '#f8f9fa'
            },
            multiple=False  # Allow only one file at a time
        ),
    ], style={'textAlign': 'center'}),
    
    # Hidden div to store filename state
    dcc.Store(id='stored-filename'),
    
    # Output section
    html.Div(id='output-file-info', style={'marginTop': '20px', 'fontWeight': 'bold', 'textAlign': 'center'}),
    
    # Display uploaded image or video
    html.Div(id='output-file-display', style={'marginTop': '20px', 'textAlign': 'center'})
])

# Callback to detect file type and display the file
def register_callbacks(app):
    @app.callback(
        Output('stored-filename', 'data'),
        Input('upload-data', 'filename')
    )
    def store_filename(filename):
        return filename if filename else ""
    
    @app.callback(
        [Output('output-file-info', 'children'),
         Output('output-file-display', 'children')],
        [Input('upload-data', 'contents'),
         State('upload-data', 'filename')]
    )
    def detect_file_type(contents, filename):
        if not contents:
            return "No file uploaded yet.", ""
        
        ext = os.path.splitext(filename)[1].lower()
        file_type = ""
        display_component = None
        
        if ext in ['.jpg', '.png']:
            file_type = "Image"
            display_component = html.Img(src=contents, style={'maxWidth': '100%', 'height': 'auto'})
        elif ext in ['.mp4']:
            file_type = "Video."
            content_type, content_string = contents.split(',')
            display_component = html.Video(src=f"data:video/mp4;base64,{content_string}", controls=True, style={'maxWidth': '100%', 'height': 'auto'})
        else:
            return "Unsupported file format.", ""
        
        return html.Div([
            html.P(f"Uploaded {file_type}: {filename}", style={'fontSize': '18px', 'fontWeight': 'bold'}),
        ]), display_component

# Ensure to register the callbacks in app.py