# model.py

import time
import base64
import pathlib
import cv2
import torch
from PIL import Image
import numpy as np
from inference_sdk import InferenceHTTPClient, InferenceConfiguration
import os
import dotenv
from ratelimit import limits, sleep_and_retry

# Load the environment variables
dotenv.load_dotenv()
CLIENT1_API_KEY = os.getenv('CLIENT1_API_KEY')
CLIENT2_API_KEY = os.getenv('CLIENT2_API_KEY')

# Configuration for the HTTP clients
custom_configuration = InferenceConfiguration(confidence_threshold=0.4, iou_threshold=0.4)
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
model = torch.hub.load('./yolov5', 'custom', path='best_250_with_yolov5s.pt', source='local')
print("YOLO model loaded successfully.")

# Define colors for different sources
colors = {
    'yolo': (255, 0, 0),  # Red
    'seascanner': (0, 100, 0),  # Dark Green
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
def combine_results(yolo_results, marinespecies_results, seascanner_results, neuralocean_results):
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
        if seascanner_box['confidence'] > 0.41:
            combined_boxes.append({
                'box': [seascanner_box['x'] - seascanner_box['width'] / 2, seascanner_box['y'] - seascanner_box['height'] / 2,
                        seascanner_box['x'] + seascanner_box['width'] / 2, seascanner_box['y'] + seascanner_box['height'] / 2],
                'conf': seascanner_box['confidence'],
                'class': seascanner_box['class'],
                'source': 'seascanner'
            })

    for marine_box in marinespecies_results['predictions']:
        if marine_box['confidence'] > 0.75:
            combined_boxes.append({
                'box': [marine_box['x'] - marine_box['width'] / 2, marine_box['y'] - marine_box['height'] / 2,
                        marine_box['x'] + marine_box['width'] / 2, marine_box['y'] + marine_box['height'] / 2],
                'conf': marine_box['confidence'],
                'class': marine_box['class'],
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

    # Convert the frame for YOLO inference
    frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(frame_rgb)

    # Run YOLO inference
    yolo_results = model(pil_img)

    # Save the image to a temporary file
    temp_image_path = 'temp_image.jpg'
    cv2.imwrite(temp_image_path, image)

    # Run HTTP inference for SeaScanner model
    try:
        with CLIENT1.use_configuration(custom_configuration):
            seascanner_results = CLIENT1.infer(temp_image_path, model_id="seascanner/3")
            marinespecies_results = CLIENT1.infer(temp_image_path, model_id="underwater-marine-species/6")

    except Exception as e:
        print(f"Error calling SeaScanner API: {e}")
        seascanner_results = {'predictions': []}

    # Run inference for NeuralOcean model
    results = {}
    for workflow_id in ["neuralocean"]:
        try:
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
        except Exception as e:
            print(f"Error calling NeuralOcean API: {e}")
            results[workflow_id] = {'predictions': []}

    # Combine the results from all models
    final_boxes = combine_results(yolo_results, marinespecies_results, seascanner_results, results)

    # Draw the combined results on the image
    for box in final_boxes:
        x1, y1, x2, y2 = map(int, box['box'])
        label = f"{box['class']} {box['conf']:.2f}"
        color = colors[box['source']]
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        
        # Calculate text size
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
        
        # Draw filled rectangle behind the label
        cv2.rectangle(image, (x1, y1 - h - 5), (x1 + w, y1), color, -1)
        
        # Draw the label text
        cv2.putText(image, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    # Convert the image back to RGB format
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image_rgb, final_boxes

def process_video(contents, skip_frames=5):
    # Decode the video
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    video_path = 'temp_video.mp4'
    with open(video_path, 'wb') as f:
        f.write(decoded)

    # Process the video frame by frame
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Skip frames
        if frame_count % skip_frames != 0:
            frame_count += 1
            continue

        try:
            # Convert the frame for YOLO inference
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(frame_rgb)

            # Run YOLO inference
            yolo_results = model(pil_img)

            # Run HTTP inference for SeaScanner model
            try:
                with CLIENT1.use_configuration(custom_configuration):
                    seascanner_results = CLIENT1.infer(frame, model_id="seascanner/3")
                    marinespecies_results = CLIENT1.infer(frame, model_id="underwater-marine-species/6")
            except Exception as e:
                print(f"Error calling SeaScanner API: {e}")
                seascanner_results = {'predictions': []}

            # Run inference for NeuralOcean model
            results = {}
            for workflow_id in ["neuralocean"]:
                try:
                    response = CLIENT2.run_workflow(
                        workspace_name="trashdetection-eihzd",
                        workflow_id=workflow_id,
                        images={"image": frame},
                        use_cache=True
                    )
                    if isinstance(response, list) and len(response) > 0:
                        results[workflow_id] = response[0]  # Take the first element if it's a list
                    else:
                        results[workflow_id] = response  # Otherwise, store as-is
                except Exception as e:
                    print(f"Error calling NeuralOcean API: {e}")
                    results[workflow_id] = {'predictions': []}

            # Combine the results from all models
            final_boxes = combine_results(yolo_results, seascanner_results, results)

            # Draw the combined results on the frame
            for box in final_boxes:
                x1, y1, x2, y2 = map(int, box['box'])
                label = f"{box['class']} {box['conf']:.2f}"
                color = colors[box['source']]
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
                # Calculate text size
                (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
                
                # Draw filled rectangle behind the label
                cv2.rectangle(frame, (x1, y1 - h - 5), (x1 + w, y1), color, -1)
                
                # Draw the label text
                cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

            # Display the frame with detections
            cv2.imshow('Detections', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Convert the frame back to RGB format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame_rgb)
        except Exception as e:
            print(f"Error processing frame {frame_count}: {e}")

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

    # Ensure there are frames to process
    if not frames:
        raise ValueError("No frames were processed from the video.")

    # Save the processed video
    processed_video_path = 'processed_video.mp4'
    out = cv2.VideoWriter(processed_video_path, cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (frames[0].shape[1], frames[0].shape[0]))
    for frame in frames:
        # Convert the frame back to BGR format before writing to the video file
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)
    out.release()

    return processed_video_path, frames

# Restore pathlib
pathlib.PosixPath = temp
print("Processing complete.")