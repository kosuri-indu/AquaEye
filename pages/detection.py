# pages/detection.py

import cv2
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State
import os
import base64
from model import process_image, process_video
import plotly.graph_objs as go

# Define the layout for the detection page
layout = html.Div([
    html.H2("Debris Detection"),
    
    # File Upload Component with plus symbol
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                html.H3("+", style={'fontSize': '50px', 'marginBottom': '10px'}),
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
    html.Div(id='output-file-display', style={'marginTop': '20px', 'textAlign': 'center'}),
    
    # Spacer before dashboards
    html.Div(style={'height': '40px'}),

    # Container for all dashboards
    html.Div(
        id='dashboard-container',
        children=[
            # Individual object class count graph (conditionally displayed)
            html.H1("Dashboard", style={'fontSize': '50px', 'marginBottom': '20px'}),

            html.Div(
                id='individual-class-graph-container',
                children=[
                    dcc.Graph(id='individual-class-count-graph', style={'width': '100%', 'borderRadius': '12px', 'boxShadow': '0 6px 12px rgba(0, 0, 0, 0.2)', 'backgroundColor': '#f0f0f0', 'padding': '10px'})
                ],
                style={'width': '45%', 'margin': '20px', 'display': 'none', 'backgroundColor': '#d3d3d3', 'padding': '20px', 'borderRadius': '12px'}  # Initially hidden
            ),
            
            # Second Dashboard (Categorized graph) below the first one
            html.Div(
                id='categorized-class-graph-container',
                children=[
                    dcc.Graph(id='categorized-class-count-graph', style={'width': '100%', 'borderRadius': '12px', 'boxShadow': '0 6px 12px rgba(0, 0, 0, 0.2)', 'backgroundColor': '#f0f0f0', 'padding': '10px'})
                ],
                style={'width': '45%', 'margin': '20px', 'display': 'none', 'backgroundColor': '#d3d3d3', 'padding': '20px', 'borderRadius': '12px'}  # Initially hidden
            )
        ],
        style={'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap'}
    ),

    # Spacer after dashboards
    html.Div(style={'height': '40px'})
])

# Categories
animals = ['coral', 'crab', 'dolphin', 'fish', 'jellyfish', 'narwhal', 'octopus', 'sea-horse', 'sea-turtle', 'seal', 'shark', 'shrimp', 'star-fish', 'sting-ray', 'whale']
industrial_waste = ['can', 'cellphone', 'electronics', 'gbottle', 'glove', 'metal', 'misc', 'net', 'pbag', 'pbottle', 'plastic', 'rod', 'sunglasses', 'tire']
plastic = ['pbottle', 'plastic', 'pbag', 'gbottle']
medical_waste = ['glove', 'syringe', 'bandage', 'mask']  # New category for medical waste
miscellaneous = ['sunglasses', 'rod', 'rare_item']  # Rare or miscellaneous items

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
         Output('output-file-display', 'children'),
         Output('individual-class-count-graph', 'figure'),
         Output('categorized-class-count-graph', 'figure'),
         Output('individual-class-graph-container', 'style'),
         Output('categorized-class-graph-container', 'style')],
        [Input('upload-data', 'contents'),
         State('upload-data', 'filename')]
    )
    def detect_file_type(contents, filename):
        if not contents:
            return "No file uploaded yet.", "", go.Figure(), go.Figure(), {'display': 'none'}, {'display': 'none'}  # Hide both graph containers
        
        ext = os.path.splitext(filename)[1].lower()
        file_type = ""
        display_component = None
        
        if ext in ['.jpg', '.jpeg', '.png']:
            file_type = "Image"
            image, final_boxes = process_image(contents)
            # Convert the image to RGB format for Dash
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            _, buffer = cv2.imencode('.jpg', image_rgb)
            image_encoded = base64.b64encode(buffer).decode('utf-8')
            img_src = f'data:image/jpeg;base64,{image_encoded}'
            display_component = html.Img(src=img_src, style={'maxWidth': '100%', 'height': 'auto'})
        elif ext in ['.mp4']:
            file_type = "Video"
            try:
                processed_video_path = process_video(contents, skip_frames=5)  # Adjust skip_frames as needed
                with open(processed_video_path, 'rb') as f:
                    video_encoded = base64.b64encode(f.read()).decode('utf-8')
                video_src = f'data:video/mp4;base64,{video_encoded}'
                display_component = html.Video(src=video_src, controls=True, style={'maxWidth': '100%', 'height': 'auto'})
            except ValueError as e:
                return str(e), "", go.Figure(), go.Figure# pages/detection.py

import cv2
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State
import os
import base64
from model import process_image, process_video
import plotly.graph_objs as go

# Define the layout for the detection page
layout = html.Div([
    html.H2("Debris Detection"),
    
    # File Upload Component with plus symbol
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                html.H3("+", style={'fontSize': '50px', 'marginBottom': '10px'}),
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
    html.Div(id='output-file-display', style={'marginTop': '20px', 'textAlign': 'center'}),
    
    # Spacer before dashboards
    html.Div(style={'height': '40px'}),

    # Container for all dashboards
    html.Div(
        id='dashboard-container',
        children=[
            # Individual object class count graph (conditionally displayed)
            html.Div(
                id='individual-class-graph-container',
                children=[
                    dcc.Graph(id='individual-class-count-graph', style={'width': '100%', 'borderRadius': '12px', 'boxShadow': '0 6px 12px rgba(0, 0, 0, 0.2)', 'backgroundColor': '#f0f0f0', 'padding': '10px'})
                ],
                style={'width': '45%', 'margin': '20px', 'display': 'none', 'backgroundColor': '#d3d3d3', 'padding': '20px', 'borderRadius': '12px'}  # Initially hidden
            ),
            
            # Second Dashboard (Categorized graph) below the first one
            html.Div(
                id='categorized-class-graph-container',
                children=[
                    dcc.Graph(id='categorized-class-count-graph', style={'width': '100%', 'borderRadius': '12px', 'boxShadow': '0 6px 12px rgba(0, 0, 0, 0.2)', 'backgroundColor': '#f0f0f0', 'padding': '10px'})
                ],
                style={'width': '45%', 'margin': '20px', 'display': 'none', 'backgroundColor': '#d3d3d3', 'padding': '20px', 'borderRadius': '12px'}  # Initially hidden
            )
        ],
        style={'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap'}
    ),

    # Spacer after dashboards
    html.Div(style={'height': '40px'})
])

# Categories
animals = ['coral', 'crab', 'dolphin', 'fish', 'jellyfish', 'narwhal', 'octopus', 'sea-horse', 'sea-turtle', 'seal', 'shark', 'shrimp', 'star-fish', 'sting-ray', 'whale']
industrial_waste = ['can', 'cellphone', 'electronics', 'gbottle', 'glove', 'metal', 'misc', 'net', 'pbag', 'pbottle', 'plastic', 'rod', 'sunglasses', 'tire']
plastic = ['trash_plastic','pbottle', 'plastic', 'pbag', 'gbottle']
medical_waste = ['glove', 'syringe', 'bandage', 'mask']  # New category for medical waste
miscellaneous = ['sunglasses', 'rod', 'rare_item']  # Rare or miscellaneous items

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
         Output('output-file-display', 'children'),
         Output('individual-class-count-graph', 'figure'),
         Output('categorized-class-count-graph', 'figure'),
         Output('individual-class-graph-container', 'style'),
         Output('categorized-class-graph-container', 'style')],
        [Input('upload-data', 'contents'),
         State('upload-data', 'filename')]
    )
    def detect_file_type(contents, filename):
        if not contents:
            return "No file uploaded yet.", "", go.Figure(), go.Figure(), {'display': 'none'}, {'display': 'none'}  # Hide both graph containers
        
        ext = os.path.splitext(filename)[1].lower()
        file_type = ""
        display_component = None
        
        if ext in ['.jpg', '.jpeg', '.png']:
            file_type = "Image"
            image, final_boxes = process_image(contents)
            # Convert the image to RGB format for Dash
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            _, buffer = cv2.imencode('.jpg', image_rgb)
            image_encoded = base64.b64encode(buffer).decode('utf-8')
            img_src = f'data:image/jpeg;base64,{image_encoded}'
            display_component = html.Img(src=img_src, style={'maxWidth': '100%', 'height': 'auto'})
        elif ext in ['.mp4']:
            file_type = "Video"
            try:
                processed_video_path = process_video(contents, skip_frames=5)  # Adjust skip_frames as needed
                with open(processed_video_path, 'rb') as f:
                    video_encoded = base64.b64encode(f.read()).decode('utf-8')
                video_src = f'data:video/mp4;base64,{video_encoded}'
                display_component = html.Video(src=video_src, controls=True, style={'maxWidth': '100%', 'height': 'auto'})
            except ValueError as e:
                return str(e), "", go.Figure(), go.Figure(), {'display': 'none'}, {'display': 'none'}  # Hide both graph containers
        else:
            return "Unsupported file format.", "", go.Figure(), go.Figure(), {'display': 'none'}, {'display': 'none'}  # Hide both graph containers
        
        # Update individual class counts for the bar chart
        class_counts = {}
        for box in final_boxes:
            class_counts[box['class']] = class_counts.get(box['class'], 0) + 1

        # Categorize the counts into groups
        categorized_counts = {
            'Animals': 0,
            'Industrial Waste': 0,
            'Plastic Waste': 0,
            'Medical Waste': 0,
            'Miscellaneous': 0,
        }

        for label, count in class_counts.items():
            if label in animals:
                categorized_counts['Animals'] += count
            elif label in industrial_waste:
                categorized_counts['Industrial Waste'] += count
            if label in plastic:
                categorized_counts['Plastic Waste'] += count
            if label in medical_waste:
                categorized_counts['Medical Waste'] += count
            if label in miscellaneous:
                categorized_counts['Miscellaneous'] += count

        # Create the individual class count bar chart
        individual_data = [go.Bar(x=list(class_counts.keys()), y=list(class_counts.values()))]
        individual_figure = {'data': individual_data, 'layout': go.Layout(title='Object Class Counts')}

        # Create the categorized class count bar chart
        categorized_data = [go.Bar(x=list(categorized_counts.keys()), y=list(categorized_counts.values()))]
        categorized_figure = {'data': categorized_data, 'layout': go.Layout(title='Categorized Object Counts')}

        return html.Div([
            html.P(f"Uploaded {file_type}: {filename}", style={'fontSize': '18px', 'fontWeight': 'bold'}),
        ]), display_component, individual_figure, categorized_figure, {'display': 'block'}, {'display': 'block'}  # Show both graph containers

# Ensure to register the callbacks in app.py