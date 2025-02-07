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
    html.H2("Underwater Debris Detection", style={'textAlign': 'center', 'marginTop': '8rem', 'marginBottom': '3rem', 'fontWeight':'bold'}),
    
    # File Upload Component with plus symbol
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                html.H3("+", style={'fontSize': '50px','marginBottom': '10px'}),
            ], style={
                'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100%'
            }),
            style={
                'width': '60%', 'height': '15rem', 'lineHeight': '60px',
                'borderWidth': '2px', 'borderStyle': 'dashed', 'borderRadius': '10px',  
                'textAlign': 'center', 'margin': '0 auto', 'padding': '20px', 
                'backgroundColor': '#ffffff', 
            },
            multiple=False  # Allow only one file at a time
        ),
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),
    
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
            # Row 1
                    html.H2("Insights Dashboard", style={'textAlign': 'center', 'width': '100%', 'marginBottom': '20px', 'color': '#ffffff', 'fontWeight': 'bold'}),  # New header for the dashboard
            html.Div(
                children=[
                    # Individual object class count graph (conditionally displayed)
                    html.Div(
                        id='individual-class-graph-container',
                        children=[
                            dcc.Graph(id='individual-class-count-graph', style={'width': '100%', 'borderRadius': '12px', 'boxShadow': '0 6px 12px rgba(0, 0, 0, 0.2)', 'backgroundColor': '#444444', 'padding': '10px','border': '2px solid #333333'})  
                        ],
                        style={'width': '45%', 'margin': '20px', 'display': 'none', 'backgroundColor': '#444444', 'padding': '20px', 'borderRadius': '12px'}  # Initially hidden
                    ),
                    
                    # Categorized object class count graph
                    html.Div(
                        id='categorized-class-graph-container',
                        children=[
                            dcc.Graph(id='categorized-class-count-graph', style={'width': '100%', 'borderRadius': '12px', 'boxShadow': '0 6px 12px rgba(0, 0, 0, 0.2)', 'backgroundColor': '#444444', 'padding': '10px', 'border': '2px solid #333333'})
                        ],
                        style={'width': '45%', 'margin': '20px', 'display': 'none', 'backgroundColor': '#444444', 'padding': '20px', 'borderRadius': '12px'}  # Initially hidden
                    )
                ],
                style={'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap'}
            ),
            
            # Row 2
            html.Div(
                children=[
                    # Safety Gauge
                    html.Div(
                        id='gauge-container',
                        children=[
                            dcc.Graph(id='safety-gauge', style={'width': '100%', 'borderRadius': '12px', 'boxShadow': '0 6px 12px rgba(0, 0, 0, 0.2)', 'backgroundColor': '#444444', 'padding': '10px', 'border': '2px solid #333333'})
                        ],
                        style={'width': '45%', 'margin': '20px', 'display': 'none', 'backgroundColor': '#444444', 'padding': '20px', 'borderRadius': '12px'}  # Initially hidden
                    ),
                    
                    # Degradation Time Graph
                    html.Div(
                        id='degradation-time-graph-container',
                        children=[
                            dcc.Graph(id='degradation-time-graph', style={'width': '100%', 'borderRadius': '12px', 'boxShadow': '0 6px 12px rgba(0, 0, 0, 0.2)', 'backgroundColor': '#444444', 'padding': '10px', 'border': '2px solid #333333'})
                        ],
                        style={'width': '45%', 'margin': '20px', 'display': 'none', 'backgroundColor': '#444444', 'padding': '20px', 'borderRadius': '12px'}  # Initially hidden
                    )
                ],
                style={'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap'}
            ),

            # Row 3
            html.Div(
                children=[
                    # Suggestions Button
                    html.Div(
                        children=[
                            dbc.Button("Show Cleanup Suggestions", id="suggestions-button", color="primary", className="mr-2"),
                        ],
                        style={'width': '100%', 'textAlign': 'center', 'margin': '20px'}
                    ),
                    
                    # Toggle Container for Cleanup Suggestions
                    html.Div(
                        id='suggestions-container',
                        children=[
                            dbc.Collapse(
                                dbc.Card(dbc.CardBody([
                                    html.H5("Basic Cleanup Suggestions", className="card-title"),
                                    html.P("1. Always wear protective gloves and masks while handling debris."),
                                    html.P("2. Use a grabber tool to pick up sharp or hazardous objects."),
                                    html.P("3. Separate waste into categories: plastics, metals, and organic materials."),
                                    html.P("4. Dispose of medical waste like gloves and masks in designated bins."),
                                    html.P("5. Report large or hazardous debris to local authorities."),
                                    html.P("6. Participate in community cleanup events."),
                                    html.P("7. Educate others about the importance of keeping our waters clean.")
                                ])),
                                id="suggestions-collapse",
                            )
                        ],
                        style={'width': '100%',  'margin': '20px'}
                    )
                ],
                style={'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap'}
            )
        ],
        style={'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap', 'backgroundColor': '#333333', 'padding': '20px', 'borderRadius': '12px'}
    ),

    # Spacer after dashboards
    html.Div(style={'height': '40px'})
], style={'backgroundColor': 'white', 'padding': '20px'})

# Categories
animals = ['coral', 'crab', 'dolphin', 'fish', 'jellyfish', 'narwhal', 'octopus', 'sea-horse', 'sea-turtle', 'seal', 'shark', 'shrimp', 'star-fish', 'sting-ray', 'whale']
industrial_waste = ['can', 'cellphone', 'electronics', 'gbottle', 'glove', 'metal', 'misc', 'net', 'rod', 'sunglasses', 'tire']
plastic = ['pbottle', 'plastic', 'pbag', 'trash_plastic']
medical_waste = ['glove', 'syringe', 'bandage', 'mask']  # New category for medical waste
miscellaneous = ['sunglasses', 'rod', 'rare_item']  # Rare or miscellaneous items

degradation_times = {
    'mask': 450, 'can': 200, 'cellphone': 1000, 'electronics': 1000, 'gbottle': 10000,
    'glove': 50, 'metal': 500, 'misc': 100, 'net': 600, 'pbag': 20,
    'pbottle': 450, 'plastic': 450, 'rod': 500, 'sunglasses': 1000, 'tire': 2000, 'trash_plastic': 450
}

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
         Output('categorized-class-graph-container', 'style'),
         Output('safety-gauge', 'figure'),  # New output for gauge meter
         Output('gauge-container', 'style'),
         Output('degradation-time-graph', 'figure'),
         Output('degradation-time-graph-container', 'style')],
        [Input('upload-data', 'contents'),
         State('upload-data', 'filename')]
    )
    def detect_file_type(contents, filename):
        if not contents:
            return ("No file uploaded yet.", "", go.Figure(), go.Figure(), {'display': 'none'}, {'display': 'none'}, go.Figure(), {'display': 'none'}, go.Figure(), {'display': 'none'})  # Hide all containers
        
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
            display_component = html.Img(src=img_src, style={'maxWidth': '100%', 'height': 'auto', 'maxHeight': '500px'})
        elif ext in ['.mp4']:
            file_type = "Video"
            try:
                processed_video_path = process_video(contents, skip_frames=5)  # Adjust skip_frames as needed
                with open(processed_video_path, 'rb') as f:
                    video_encoded = base64.b64encode(f.read()).decode('utf-8')
                video_src = f'data:video/mp4;base64,{video_encoded}'
                display_component = html.Video(src=video_src, controls=True, style={'maxWidth': '100%', 'height': 'auto', 'maxHeight': '500px'})
            except ValueError as e:
                return str(e), "", go.Figure(), go.Figure(), {'display': 'none'}, {'display': 'none'}, go.Figure(), {'display': 'none'}, go.Figure(), {'display': 'none'}  # Hide all containers
        else:
            return "Unsupported file format.", "", go.Figure(), go.Figure(), {'display': 'none'}, {'display': 'none'}, go.Figure(), {'display': 'none'}, go.Figure(), {'display': 'none'}  # Hide all containers
        
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

        total_detections = len(final_boxes)
        # Create the individual class count bar chart
        individual_data = [go.Bar(x=list(class_counts.keys()), y=list(class_counts.values()))]
        individual_figure = {'data': individual_data, 'layout': go.Layout(title='Object Class Counts', paper_bgcolor='#444444', plot_bgcolor='#444444', font=dict(color='#ffffff'))}

        # Create the categorized class count bar chart
        categorized_data = [go.Bar(x=list(categorized_counts.keys()), y=list(categorized_counts.values()))]
        categorized_figure = {'data': categorized_data, 'layout': go.Layout(title='Categorized Object Counts', paper_bgcolor='#444444', plot_bgcolor='#444444', font=dict(color='#ffffff'))}

        # Update image info to include total detections
        image_info = f"Processing image: {filename}\n"
        # Calculate debris percentage
        debris_count = sum(count for item, count in class_counts.items() if item not in animals)

        max_percentage = 100 # or some other maximum value

        debris_percentage = (debris_count / max_percentage) * 1000
        # Determine safety level
        if debris_percentage <= 30:
            safety_status = "Safe"
            gauge_color = "green"
        elif debris_percentage <= 60:
            safety_status = "Moderate"
            gauge_color = "yellow"
        elif debris_percentage <= 90:
            safety_status = "Unsafe"
            gauge_color = "orange"
        else:
            safety_status = "Hazardous"
            gauge_color = "red"

        # Create gauge meter figure
        gauge_figure = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=debris_percentage,
                title={"text": f"Safety Level: {safety_status}"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": gauge_color},
                    "steps": [
                        {"range": [0, 30], "color": "green"},
                        {"range": [30, 60], "color": "yellow"},
                        {"range": [60, 90], "color": "orange"},
                        {"range": [90, 100], "color": "red"}
                    ]
                }
            )
        )
        gauge_figure.update_layout(paper_bgcolor='#444444', font=dict(color='#ffffff'))

        # Create degradation time bar chart
        degradation_data = []
        for item, count in class_counts.items():
            if item not in degradation_times:
                continue
            degradation_time = degradation_times.get(item, 0)
            degradation_data.append(go.Bar(x=[item], y=[degradation_time]))
        degradation_figure = {'data': degradation_data, 'layout': go.Layout(title='Degradation Time of Detected Items', paper_bgcolor='#444444', plot_bgcolor='#444444', font=dict(color='#ffffff'))}

        return image_info, display_component, individual_figure, categorized_figure, {'display': 'block'}, {'display': 'block'}, gauge_figure, {'display': 'block'}, degradation_figure, {'display': 'block'}  # Show all containers

    @app.callback(
        Output("suggestions-collapse", "is_open"),
        [Input("suggestions-button", "n_clicks")],
        [State("suggestions-collapse", "is_open")],
    )
    def toggle_suggestions(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open
# Ensure to register the callbacks in app.py