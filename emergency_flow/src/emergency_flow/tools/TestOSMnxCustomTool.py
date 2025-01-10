import osmnx as ox
import os

longitude_origin = -0.40776
latitude_origin = 39.46798
longitude_destination = -0.36332447406737145 
latitude_destination = 39.46061969757309

# file_path = os.path.join(os.path.dirname(__file__), 'inputs', 'valencia.graphml')
# graph = ox.load_graphml(filepath="emergency_flow/src/emergency_flow/inputs/valencia.graphml")

mapp = ox.graph_from_place('Valencia, Spain', network_type='drive')
fig, ax = ox.plot_graph(mapp)
ox.save_graphml(mapp, filepath='valencia.graphml')
mapp = ox.load_graphml('valencia.graphml')

graph = ox.routing.add_edge_speeds(mapp)
graph = ox.routing.add_edge_travel_times(mapp)

origin_node = ox.distance.nearest_nodes(mapp, X=longitude_origin, Y=latitude_origin)
destination_node = ox.distance.nearest_nodes(mapp, X=longitude_destination, Y=latitude_destination)
route = ox.shortest_path(mapp, origin_node, destination_node, weight='travel_time')
edge_lengths = ox.routing.route_to_gdf(mapp, route)['length']

print("distance_meters:", round(sum(edge_lengths)))
