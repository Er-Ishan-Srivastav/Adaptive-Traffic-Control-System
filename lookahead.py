import networkx as nx

# Create a city grid graph
city_grid = nx.DiGraph()

# Add intersections
city_grid.add_node("Intersection_A", density=45, wait_time=120)
city_grid.add_node("Intersection_B", density=95, wait_time=300)

# Connect them (Traffic flows A -> B)
city_grid.add_edge("Intersection_A", "Intersection_B")

def calculate_green_time(node):
    local_density = city_grid.nodes[node]['density']
    
    # Check downstream pressure
    downstream_nodes = list(city_grid.successors(node))
    if downstream_nodes:
        downstream_density = city_grid.nodes[downstream_nodes[0]]['density']
        if downstream_density > 80:
            print(f"Downstream full! Restricting green time for {node}.")
            return 15 # Restrict to 15 seconds
            
    # Standard formula if downstream is clear
    return (local_density * 0.5) + 10

tg_A = calculate_green_time("Intersection_A")
print(f"Allocated Green Time for A: {tg_A} seconds")