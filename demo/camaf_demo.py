import os
import sys
import traci
import time

# 1. Locate SUMO
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Error: Please set the 'SUMO_HOME' environment variable.")

def get_lane_metrics(lane_id):
    """Simulates YOLO detecting cars and measuring wait time."""
    vehicle_count = traci.lane.getLastStepVehicleNumber(lane_id)
    wait_time = traci.lane.getWaitingTime(lane_id)
    return vehicle_count, wait_time

def run_camaf_logic():
    step = 0
    tls_id = "Intersection_A"
    
    # In SUMO, adding "_0" targets the first lane of an edge
    north_lane = "edge_north_to_A_0"
    west_lane = "edge_west_to_A_0"
    downstream_lane = "edge_A_to_B_0" 
    
    print("--- Starting CAMAF Simulation ---")
    
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        
        # Run our logic every 5 simulation steps
        if step % 5 == 0:
            n_count, n_wait = get_lane_metrics(north_lane)
            w_count, w_wait = get_lane_metrics(west_lane)
            downstream_count, _ = get_lane_metrics(downstream_lane)
            
            # Calculate Downstream Pressure (Assuming edge holds ~10 cars)
            downstream_pressure = downstream_count / 10.0 
            
            # SPATIO-TEMPORAL LOGIC: 
            # If the road to B is full, DO NOT let more cars go West-to-East
            if downstream_pressure > 0.80:
                print(f"Step {step} | WARNING: Gridlock risk at B! Force North-South Green.")
                traci.trafficlight.setPhase(tls_id, 0) # Phase 0: North-South Green
                
            else:
                # NORMAL YOLO LOGIC: Weight density and wait time
                north_score = (n_count * 1.0) + (n_wait * 0.5)
                west_score = (w_count * 1.0) + (w_wait * 0.5)
                
                if north_score > west_score:
                    print(f"Step {step} | Flow: North-South (Score: {north_score:.1f} vs {west_score:.1f})")
                    traci.trafficlight.setPhase(tls_id, 0) 
                else:
                    print(f"Step {step} | Flow: West-East   (Score: {west_score:.1f} vs {north_score:.1f})")
                    traci.trafficlight.setPhase(tls_id, 2) # Phase 2: West-East Green
        
        step += 1
        time.sleep(0.1)
        
    traci.close()
    print("Simulation Complete.")

if __name__ == "__main__":
    # Launch the visual GUI
    sumo_cmd = ["sumo-gui", "-c", "demo.sumocfg", "--start"]
    traci.start(sumo_cmd)
    run_camaf_logic()