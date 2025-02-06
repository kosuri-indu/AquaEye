import base64
import pathlib
import cv2
import torch
from PIL import Image
import numpy as np
from inference_sdk import InferenceHTTPClient, InferenceConfiguration
import os
import dotenv

# Load the environment variables
dotenv.load_dotenv()
CLIENT1_API_KEY = os.getenv('CLIENT1_API_KEY')
CLIENT2_API_KEY = os.getenv('CLIENT2_API_KEY')

# Configuration for the HTTP clients
custom_configuration = InferenceConfiguration(confidence_threshold=0.5, iou_threshold=0.4)
CLIENT1 = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=CLIENT1_API_KEY,
)

CLIENT2 = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=CLIENT2_API_KEY,
)

# Temporarily change pathlib for Windows compatibility
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# Load the YOLO model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best_250_with_yolov5s.pt', force_reload=True)
print("YOLO model loaded successfully.")

# Define colors for different sources
colors = {
    'yolo': (255, 0, 0),  # Blue
    'seascanner': (0, 0, 255),  # Red
    'neuralocean': (0, 0, 0)  # Black
}

# IoU calculation function
def iou(box1, box2):
    x1, y1, x2, y2 = box1
    x1_, y1_, x2_, y2_ = box2
    xi1, yi1 = max(x1, x1_), max(y1, y1_)
    xi2, yi2 = min(x2, x2_), min(y2, y2_)
    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (x2_ - x1_) * (y2_ - y1_)
    union_area = box1_area + box2_area - inter_area
    return inter_area / union_area if union_area > 0 else 0

# Combine results from multiple models
def combine_results(yolo_results, seascanner_results, neuralocean_results):
    combined_boxes = []

    # Process YOLO results
    for yolo_box in yolo_results.xyxy[0]:
        confidence = yolo_box[4].item()
        if confidence > 0.5:  # Filter by confidence threshold
            combined_boxes.append({
                'box': yolo_box[:4].tolist(),
                'conf': confidence,
                'class': model.names[int(yolo_box[5].item())],
                'source': 'yolo'
            })

    # Process SeaScanner results
    for seascanner_box in seascanner_results['predictions']:
        combined_boxes.append({
            'box': [seascanner_box['x'] - seascanner_box['width'] / 2, seascanner_box['y'] - seascanner_box['height'] / 2,
                    seascanner_box['x'] + seascanner_box['width'] / 2, seascanner_box['y'] + seascanner_box['height'] / 2],
            'conf': seascanner_box['confidence'],
            'class': seascanner_box['class'],
            'source': 'seascanner'
        })

    # Process NeuralOcean results with class mapping
    class_mapping = {"0": "trash_plastics", "1": "living_beings"}
    for workflow_id, result in neuralocean_results.items():
        if 'predictions' in result and 'predictions' in result['predictions']:
            for box in result['predictions']['predictions']:
                class_label = class_mapping.get(str(box['class']), box['class'])
                if box['confidence'] > 0.5:
                    combined_boxes.append({
                        'box': [box['x'] - box['width'] / 2, box['y'] - box['height'] / 2,
                                box['x'] + box['width'] / 2, box['y'] + box['height'] / 2],
                        'conf': box['confidence'],
                        'class': class_label,
                        'source': workflow_id
                    })

    # Sort by confidence and filter overlapping boxes
    combined_boxes.sort(key=lambda x: x['conf'], reverse=True)
    final_boxes = []
    for box in combined_boxes:
        if not any([iou(box['box'], existing_box['box']) > 0.4 for existing_box in final_boxes]):
            final_boxes.append(box)

    return final_boxes

def process_image(contents):
    # Decode the image
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    image = cv2.imdecode(np.frombuffer(decoded, np.uint8), cv2.IMREAD_COLOR)

    # Save the image to a temporary file
    temp_image_path = 'temp_image.jpg'
    cv2.imwrite(temp_image_path, image)

    # Convert the frame for YOLO inference
    frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(frame_rgb)

    # Run YOLO inference
    yolo_results = model(pil_img)

    # Run HTTP inference for SeaScanner model
    with CLIENT1.use_configuration(custom_configuration):
        seascanner_results = CLIENT1.infer(temp_image_path, model_id="seascanner/4")

    # Run inference for NeuralOcean model
    results = {}
    for workflow_id in ["neuralocean"]:
        response = CLIENT2.run_workflow(
            workspace_name="trashdetection-eihzd",
            workflow_id=workflow_id,
            images={"image": temp_image_path},
            use_cache=True
        )
        if isinstance(response, list) and len(response) > 0:
            results[workflow_id] = response[0]  # Take the first element if it's a list
        else:
            results[workflow_id] = response  # Otherwise, store as-is

    # Combine the results from all models
    final_boxes = combine_results(yolo_results, seascanner_results, results)

    return image, final_boxes

# Restore pathlib
pathlib.PosixPath = temp
print("Processing complete.")