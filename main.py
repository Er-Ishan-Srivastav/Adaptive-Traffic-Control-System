from ultralytics import YOLO
import cv2
import time

model = YOLO('runs/detect/traffic_edge_model/weights/best.pt')
video_path = "test_traffic.mp4"
cap = cv2.VideoCapture(video_path)

# Dictionary to store how long a car has been in the frame
vehicle_wait_times = {}
density_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv11 tracking
    results = model.track(frame, persist=True, tracker="botsort.yaml", verbose=False)
    
    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        classes = results[0].boxes.cls.int().cpu().tolist()
        
        density_count = len(track_ids) # Current lane density
        
        for box, track_id, cls in zip(boxes, track_ids, classes):
            # If we haven't seen this car, record its start time
            if track_id not in vehicle_wait_times:
                vehicle_wait_times[track_id] = time.time()
            
            # Calculate wait time
            wait_time = time.time() - vehicle_wait_times[track_id]
            
            # Highlight emergency vehicles (Class 2 might be ambulance depending on your dataset)
            if cls == 2: 
                print("EMERGENCY VEHICLE DETECTED - TRIGGER PRIORITY")
                
    # Display the frame
    annotated_frame = results[0].plot()
    cv2.imshow("YOLOv11 Traffic Tracking", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()