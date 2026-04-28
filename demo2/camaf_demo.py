import os
import sys
import traci

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Error: Please set the 'SUMO_HOME' environment variable.")

def get_approach_metrics(edge_id, num_lanes):
    """
    Simulates YOLO aggregating data across multiple lanes.
    Calculates Total Density and the Maximum Wait Time for the approach.
    """
    total_vehicles = 0
    max_wait = 0
    
    # Loop through lanes _0, _1, _2
    for i in range(num_lanes):
        lane_id = f"{edge_id}_{i}"
        total_vehicles += traci.lane.getLastStepVehicleNumber(lane_id)
        
        # We care about the longest waiting car on the approach
        wait = traci.lane.getWaitingTime(lane_id)
        if wait > max_wait:
            max_wait = wait
            
    return total_vehicles, max_wait

def run_camaf_logic():
    step = 0
    tls_id = "Intersection_A"
    
    # Base edge IDs (no lane numbers attached)
    north_edge = "edge_north_to_A"
    west_edge = "edge_west_to_A"
    downstream_edge = "edge_A_to_B"
    lanes_per_edge = 3
    
    print("--- Starting Multi-Lane CAMAF Simulation ---")
    
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        
        if step % 5 == 0:
            n_count, n_wait = get_approach_metrics(north_edge, lanes_per_edge)
            w_count, w_wait = get_approach_metrics(west_edge, lanes_per_edge)
            downstream_count, _ = get_approach_metrics(downstream_edge, lanes_per_edge)
            
            # 3 lanes hold more cars. Assume max capacity is ~30 cars (10 per lane).
            downstream_pressure = downstream_count / 30.0 
            print(downstream_pressure)
            if downstream_pressure > 0.01:
                print(f"Step {step} | WARNING: 3-Lane Gridlock risk at B! Forcing North-South Flow.")
                traci.trafficlight.setPhase(tls_id, 0) # N/S Green
                
            else:
                # Dynamic Logic
                north_score = (n_count * 1.0) + (n_wait * 0.5)
                west_score = (w_count * 1.0) + (w_wait * 0.5)
                
                if north_score > west_score:
                    print(f"Step {step} | Flow: North-South (Agg Score: {north_score:.1f}) | N-Cars: {n_count}")
                    traci.trafficlight.setPhase(tls_id, 0) 
                else:
                    print(f"Step {step} | Flow: West-East   (Agg Score: {west_score:.1f}) | W-Cars: {w_count}")
                    traci.trafficlight.setPhase(tls_id, 2) 
        
        step += 1
        
    traci.close()
    print("Simulation Complete.")

if __name__ == "__main__":
    sumo_cmd = ["sumo-gui", "-c", "demo.sumocfg", "--start"]
    traci.start(sumo_cmd)
    run_camaf_logic()