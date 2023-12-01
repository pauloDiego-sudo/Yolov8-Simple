import cv2
from ultralytics import YOLO
from ultralytics.nn.tasks import Ensemble

# # Load the YOLOv8 model
model = YOLO('yolov8n-face.pt')
model2 = YOLO('yolov8n.pt')

# Open the video file
video_path = "samples/video2.mp4"
cap = cv2.VideoCapture(video_path)

# Get the video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_path = 'output.mp4'
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# Class names (modify as needed)
class_names = ['face','person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

total_people = []
total_faces = []
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame,classes=0, conf=0.5)
        results2 = model2(frame, classes=0, conf=0.5)
        # Set to store unique faces for the current frame
        faces = set()
        # Set for people
        people = set()

        # Process the YOLOv8 results
        for result in results:
            boxes = result.boxes  # Boxes object for bbox outputs
            cls = boxes.cls.tolist()  # Convert tensor to list

            for idx, class_index in enumerate(cls):
                class_name = class_names[int(class_index)]

                # Extract bounding box coordinates
                x1, y1, x2, y2 = int(boxes.xyxy[idx][0]), int(boxes.xyxy[idx][1]), \
                                 int(boxes.xyxy[idx][2]), int(boxes.xyxy[idx][3])

                # Extract region of interest (ROI) inside the bounding box
                roi = frame[y1:y2, x1:x2]
                blurred_roi = cv2.blur(roi, (15, 15))  # Apply blur effect (adjust kernel size as needed)

                # Replace the region inside the bounding box with the blurred image
                frame[y1:y2, x1:x2] = blurred_roi

                # Draw bounding box and label on the frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, f'{class_name}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                faces.add((x1, y1, x2, y2))

        for result2 in results2:
            boxes2 = result2.boxes
            cls2 = boxes2.cls.tolist()

            for idx2, class_index2 in enumerate(cls2):
                class_name2 = class_names[int(class_index2)]
                # Extract bounding box coordinates
                x1, y1, x2, y2 = int(boxes2.xyxy[idx2][0]), int(boxes2.xyxy[idx2][1]), \
                                 int(boxes2.xyxy[idx2][2]), int(boxes2.xyxy[idx2][3])
                # Draw bounding box and label on the frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'Person', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                people.add((x1, y1, x2, y2))       
        
        total_faces.append(len(faces))
        cv2.putText(frame, f'Total Number of tracked faces: {max(total_faces)}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        # Get the total amount of tracked people and show just the max
        total_people.append(len(people))
        cv2.putText(frame, f'Total Number of tracked people: {max(total_people)}', (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Write the frame to the output video file
        out.write(frame)
        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
