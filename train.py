from ultralytics import YOLO
import torch

# Verify CUDA is available (Crucial for 6GB VRAM)
print("CUDA Available: ", torch.cuda.is_available())

def train():
    # Load the YOLOv11 nano model
    model = YOLO('yolo11n.pt') 

    # Train the model
    # batch=8 ensures you don't run out of your 6GB VRAM
    # imgsz=416 or 640 depending on memory. Let's use 640.
    results = model.train(
        data='./dataset/data.yaml', 
        epochs=50, 
        imgsz=640, 
        batch=8, 
        device=0, # 0 targets your Nvidia GPU
        name='traffic_edge_model'
    )

     # Validation
    metrics = model.val()
    print(f"mAP50-95: {metrics.box.map}")

    # Export
    model.export(format='onnx')

if __name__ == '__main__':
    train()