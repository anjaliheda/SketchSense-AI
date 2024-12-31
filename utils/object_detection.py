from ultralytics import YOLO
import cv2

# Load the YOLO model
model = YOLO('yolov8n.pt')

def detect_objects(input_path, output_path):
    # Perform object detection
    results = model(input_path)
    annotated_image = results[0].plot()  # Annotate the image
    cv2.imwrite(output_path, annotated_image)
