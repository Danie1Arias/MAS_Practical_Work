import osmnx as ox
import networkx as nx
from crewai.tools import tool

@tool("OSMnx Shortest Path Tool")
def compute_shortest_path(graph, coord1, coord2):
    """
    Compute the shortest distance between two locations in a city.

    Parameters:
    - graph: OSMnx graph object representing the city.
    - coord1: Tuple (lat, lon) for the first location.
    - coord2: Tuple (lat, lon) for the second location.

    Returns:
    - distance: Shortest distance between the two locations in meters. 
    - path: Shortest path between the two locations in meters. 
    """

    # Find the nearest nodes in the graph to the given coordinates
    node1 = ox.distance.nearest_nodes(graph, X=coord1[1], Y=coord1[0])
    node2 = ox.distance.nearest_nodes(graph, X=coord2[1], Y=coord2[0])

    # Compute the shortest path between the nodes
    # change to weight='travel-time' for calculating a path in minutes
    distance = nx.shortest_path_length(graph, node1, node2, weight='length')
    path = nx.shortest_path(graph, node1, node2, weight='length') 

    return distance, path

"""
# Calculate distance between two points - Example of use

# Read the city graph
file_path = "emergency_flow/src/emergency_flow/inputs/valencia.graphml"
graph = ox.load_graphml(filepath=file_path)

# Coordinates of points (lat, lon)
location_1 = (39.4575, -0.3475)  # location 1: 39.4699, -0.3763, location 2: 39.4575, -0.3475
location_2 = (39.4736, -0.3797)  # location 1: 39.4541, -0.3520, location 2: 39.4736, -0.3797

# Calculate distance
distance, path = compute_shortest_path(graph, location_1, location_2)
if distance:
    print(f"Shortest path between points is {distance:.2f} metres.")
else:
    print("No valid path exists between the two nodes.")

# Draw shortest path on a map
ox.plot_graph_route(graph, path, route_linewidth=4, node_size=0)
"""