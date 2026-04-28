import flwr as fl
from ultralytics import YOLO
import torch

# Define a Flower Client (represents ONE intersection)
class TrafficEdgeClient(fl.client.NumPyClient):
    def __init__(self):
        self.model = YOLO('yolo11n.pt') # Load local model

    def get_parameters(self, config):
        # Extract weights from PyTorch model to send to server
        return [val.cpu().numpy() for _, val in self.model.model.state_dict().items()]

    def set_parameters(self, parameters):
        # Receive averaged weights from server and update local model
        params_dict = zip(self.model.model.state_dict().keys(), parameters)
        state_dict = {k: torch.tensor(v) for k, v in params_dict}
        self.model.model.load_state_dict(state_dict, strict=True)

    def fit(self, parameters, config):
        self.set_parameters(parameters)
        # Train locally on THIS intersection's data
        self.model.train(data='local_intersection_data.yaml', epochs=1, batch=8, device=0)
        return self.get_parameters(config=config), 100, {} # 100 is number of examples

# Start the client (In a real setup, run multiple of these on different machines/terminals)
if __name__ == "__main__":
    fl.client.start_client(server_address="127.0.0.1:8080", client=TrafficEdgeClient())