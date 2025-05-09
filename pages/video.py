import pathlib
import torch
import cv2
from PIL import Image
import numpy as np
import dash
import dash_bootstrap_components as dbc

from dash import dcc, html
from dash.dependencies import Output, Input, State
import plotly.graph_objs as go
import base64
# import os
import tempfile
import platform
import concurrent.futures

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

# Temporary fix for pathlib issue
if platform.system() == 'Windows':
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath

# Load YOLOv5 model
try:
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best_250_with_yolov5s.pt', force_reload=True)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# Define the layout for the video page
layout = html.Div([
    html.H2("Underwater Debris Video Detection", style={'textAlign': 'center', 'marginTop': '10rem', 'marginBottom': '3rem', 'fontWeight':'bold'}),
    
    html.Div(dcc.Upload(
        id='upload-video',
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
            multiple=False 
    ), style={'marginBottom': '20px'}),

    html.Div(id='video-info', style={'textAlign': 'center', 'margin': '10px', 'fontSize': '16px'}),

    html.Div(html.Img(id='video-frame', style={
        'width': '60%', 'margin': '20px auto', 'display': 'block',
        'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.2)', 'borderRadius': '10px'
    })),

    dcc.Graph(id='class-count-graph'),

    # Container for all dashboards
    html.Div(
        id='dashboard-container',
        children=[
            # # Row 1
            #         html.H2("Insights Dashboard", style={'textAlign': 'center', 'width': '100%', 'marginBottom': '20px', 'color': '#ffffff', 'fontWeight': 'bold'}),  # New header for the dashboard
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
                                     html.H5("Safe Cleanup Suggestions", className="card-title"),
    html.P("1. Wear protective gloves and masks while handling debris."),
    html.P("2. Use a grabber tool to pick up lightweight trash like paper and plastic."),
    html.P("3. Participate in organized cleanup events with proper supervision."),
    html.P("4. Separate waste into recyclables and non-recyclables."),
    html.P("5. Educate others on waste disposal and environmental conservation."),

    html.H5("Medium Risk Cleanup Suggestions", className="card-title"),
    html.P("1. Use thicker gloves and sturdy shoes to avoid cuts and punctures."),
    html.P("2. Handle small amounts of broken glass or metal carefully using tools."),
    html.P("3. Avoid wading into water without proper gear."),
    html.P("4. Ensure that you are working in a well-lit and stable area."),
    html.P("5. Carry a first aid kit in case of minor injuries."),

    html.H5("Unsafe Cleanup Suggestions (Requires Caution)", className="card-title"),
    html.P("1. Do not attempt to remove large or deeply embedded debris alone."),
    html.P("2. Avoid handling sharp, rusted, or unknown metal objects directly."),
    html.P("3. Stay clear of unstable structures or heavily polluted areas."),
    html.P("4. Be cautious of wildlife that may be hiding under debris."),
    html.P("5. Work in pairs when dealing with heavier or bulkier waste items."),

    html.H5("Hazardous Cleanup Suggestions (Requires Authorities)", className="card-title"),
    html.P("1. Do not touch hazardous materials such as oil spills, chemicals, or medical waste."),
    html.P("2. Report large debris or biohazards (e.g., syringes, contaminated waste) to local authorities."),
    html.P("3. Avoid areas with strong odors, discoloration, or toxic fumes."),
    html.P("4. If a cleanup involves industrial waste, seek guidance from professionals."),
    html.P("5. Wear full protective gear (respirator, coveralls, gloves) if required by emergency teams.")
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

    dcc.Interval(id='interval-component', interval=500, n_intervals=0, disabled=True)  # Faster refresh rate
])

# Video Processing Optimizations
frame_skip = 3  # Skip frames for speed
batch_size = 4  # Process 4 frames in parallel
class_counts = {}
cap = None
executor = concurrent.futures.ThreadPoolExecutor(max_workers=batch_size)

def process_frames_parallel(frames):
    """ Process multiple frames in parallel using YOLOv5 """
    results = []
    futures = []

    for frame in frames:
        futures.append(executor.submit(run_model, frame))

    for future in concurrent.futures.as_completed(futures):
        results.append(future.result())

    return results

def run_model(frame):
    """ Runs the model on a single frame """
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(frame_rgb)
    results = model(pil_img)

    detected_objects = {}
    for result in results.xyxy[0]:
        class_id = int(result[5])
        class_name = model.names[class_id]
        detected_objects[class_name] = detected_objects.get(class_name, 0) + 1

    annotated_frame = np.squeeze(results.render())
    _, buffer = cv2.imencode('.jpg', cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR))
    return base64.b64encode(buffer).decode('utf-8'), detected_objects

def process_video():
    global cap, class_counts
    if not cap or not cap.isOpened():
        return None, None

    frames_to_process = []
    for _ in range(batch_size):
        ret, frame = cap.read()
        if not ret:
            break
        frames_to_process.append(frame)

    if not frames_to_process:
        return None, None

    results = process_frames_parallel(frames_to_process)

    final_counts = {}
    last_encoded_frame = None

    for encoded_frame, frame_counts in results:
        last_encoded_frame = encoded_frame  # Use the last valid frame for display
        for key, value in frame_counts.items():
            final_counts[key] = final_counts.get(key, 0) + value

    return last_encoded_frame, final_counts

def register_callbacks(app):
    @app.callback(
        [Output('video-info', 'children'), Output('interval-component', 'disabled')],
        [Input('upload-video', 'contents')],
        [State('upload-video', 'filename')]
    )
    def upload_video(contents, filename):
        global cap, class_counts
        if contents is None:
            return "No video uploaded.", True

        # Save uploaded video to a temporary file
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=filename)
        with open(temp_file.name, 'wb') as f:
            f.write(decoded)

        # Initialize video capture
        cap = cv2.VideoCapture(temp_file.name)
        if not cap.isOpened():
            return "Error: Unable to open the uploaded video.", True

        class_counts = {}
        return f"Processing video: {filename}", False

    @app.callback(
        [Output('class-count-graph', 'figure'), Output('video-frame', 'src')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_output(n):
        frame_encoded, class_counts = process_video()
        if frame_encoded is None:
            return dash.no_update, dash.no_update

        # Update bar chart
        data = [go.Bar(x=list(class_counts.keys()), y=list(class_counts.values()))]
        figure = {'data': data, 'layout': go.Layout(title='Object Class Counts')}

        # Update video frame
        img_src = f'data:image/jpeg;base64,{frame_encoded}'
        return figure, img_src

# Restore pathlib
if platform.system() == 'Windows':
    pathlib.PosixPath = temp