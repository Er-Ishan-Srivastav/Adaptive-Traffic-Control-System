import cv2
import time
import torch
import requests
import numpy as np
import flwr as fl
from ultralytics import YOLO

# ==========================================
# CONFIGURATION & HYPERPARAMETERS
# ==========================================
NODE_ID = "Intersection_A"
DOWNSTREAM_IP = "http://127.0.0.1:5000" # IP of Intersection B (Mocked for now)
VIDEO_SOURCE = "traffic_video.mp4" # Replace with 0 for live webcam
YOLO_MODEL_PATH = "yolo11n.pt" # Your trained model
EVALUATION_INTERVAL = 5 # Evaluate traffic light every 5 seconds

# Math Weights (alpha, beta) for Tg = aD + bW
ALPHA_DENSITY = 1.0
BETA_WAIT = 0.5

print(f"CUDA Available: {torch.cuda.is_available()}")

# ==========================================
# FEDERATED LEARNING CLIENT (FLOWCHART STEP 6 & 7)
# ==========================================
class TrafficEdgeClient(fl.client.NumPyClient):
    def __init__(self, model):
        self.model = model

    def get_parameters(self, config):
        return [val.cpu().numpy() for _, val in self.model.model.state_dict().items()]

    def set_parameters(self, parameters):
        params_dict = zip(self.model.model.state_dict().keys(), parameters)
        state_dict = {k: torch.tensor(v) for k, v in params_dict}
        self.model.model.load_state_dict(state_dict, strict=True)

    def fit(self, parameters, config):
        print("\n--- Starting Nightly Federated Sync ---")
        self.set_parameters(parameters)
        # In reality, this trains on the day's locally saved hard examples
        self.model.train(data='local_data.yaml', epochs=1, imgsz=640, batch=8, device=0)
        return self.get_parameters(config={}), 100, {}

# ==========================================
# CORE SYSTEM ENGINE
# ==========================================
def run_realtime_node():
    print(f"--- Initializing {NODE_ID} ---")
    
    # 1. Load Model (Flowchart Step 1 & 2)
    model = YOLO(YOLO_MODEL_PATH)
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    
    vehicle_wait_times = {}
    last_eval_time = time.time()
    current_light_state = "RED"
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video stream.")
            break

        # 2. YOLO Tracking (Flowchart Step 2)
        # Using BoT-SORT for stable ID tracking across frames
        results = model.track(frame, persist=True, tracker="botsort.yaml", verbose=False)
        
        current_density = 0
        max_wait_time = 0
        
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            classes = results[0].boxes.cls.int().cpu().tolist()
            
            # 3. Extract Density & Wait Time (Flowchart Step 3)
            current_density = len(track_ids)
            current_time = time.time()
            
            for box, track_id, cls in zip(boxes, track_ids, classes):
                # If new vehicle, record start time
                if track_id not in vehicle_wait_times:
                    vehicle_wait_times[track_id] = current_time
                
                # Calculate how long it has been on screen
                wait = current_time - vehicle_wait_times[track_id]
                if wait > max_wait_time:
                    max_wait_time = wait
                    
                # Highlight Emergency Vehicles (Assuming Class 2 is ambulance/fire)
                if cls == 2:
                    cv2.putText(frame, "EMERGENCY", (int(box[0]), int(box[1])-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                    max_wait_time += 100 # Artificial massive priority boost

        # 4. Logic & Coordination Layer (Flowchart Steps 4 & 5)
        # Evaluate every X seconds to avoid flickering lights
        if time.time() - last_eval_time > EVALUATION_INTERVAL:
            last_eval_time = time.time()
            
            # Spatio-Temporal Graph: Check Downstream Node B
            downstream_pressure = 0.0
            try:
                # Ask Node B how full it is
                response = requests.get(f"{DOWNSTREAM_IP}/status", timeout=1)
                downstream_pressure = response.json().get("pressure", 0.0)
            except:
                pass # If Node B is offline, assume it's clear
            
            # Decision Engine
            if downstream_pressure > 0.85:
                print(f"[{NODE_ID}] WARNING: Downstream Full! Forcing RED.")
                current_light_state = "RED"
            else:
                # Calculate Score: S = a*D + b*W
                local_score = (ALPHA_DENSITY * current_density) + (BETA_WAIT * max_wait_time)
                
                # Actuation Threshold (If score is high enough, turn green)
                if local_score > 15.0: 
                    current_light_state = "GREEN"
                    print(f"[{NODE_ID}] Score: {local_score:.1f} -> Light: GREEN")
                else:
                    current_light_state = "RED"
                    print(f"[{NODE_ID}] Score: {local_score:.1f} -> Light: RED")

        # Visual Display for the Demo
        annotated_frame = results[0].plot()
        
        # Draw the Traffic Light UI on the frame
        color = (0, 255, 0) if current_light_state == "GREEN" else (0, 0, 255)
        cv2.rectangle(annotated_frame, (10, 10), (350, 120), (0,0,0), -1)
        cv2.putText(annotated_frame, f"Density: {current_density}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
        cv2.putText(annotated_frame, f"Max Wait: {max_wait_time:.1f}s", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
        cv2.putText(annotated_frame, f"LIGHT: {current_light_state}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 3)
        
        cv2.imshow("CAMAF Edge Node Vision", annotated_frame)
        
        # Press 'q' to quit early
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    # After video ends (End of Day), trigger Federated Learning Sync
    print("\nInitiating Federated Learning Sync with Cloud Server...")
    fl.client.start_client(server_address="127.0.0.1:8080", client=TrafficEdgeClient(model))

if __name__ == "__main__":
    run_realtime_node()