from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import osmnx as ox
import os

class ShortestPathInput(BaseModel):
    """Input schema for ShortestPathTool."""
    longitude_origin: float = Field(..., description="X coordinate from the origin location.")
    latitude_origin: float = Field(..., description="Y coordinate from the origin location.")
    longitude_destination: float = Field(..., description="X coordinate from the destination location.")
    latitude_destination: float = Field(..., description="Y coordinate from the destination location.")

class ShortestPathTool(BaseTool):
    name: str = "OSMnx Shortest Path Tool"
    description: str = (
        "Computes the shortest distance and path between two locations in a city using an OSMnx graph. "
        "Returns the distance in meters and the path as a list of nodes."
    )
    args_schema: Type[BaseModel] = ShortestPathInput

    def _run(self, longitude_origin: float, latitude_origin: float,
             longitude_destination: float, latitude_destination: float) -> dict:
        try:
            file_path = os.path.join('..', 'inputs', 'valencia.graphml')
            graph = ox.load_graphml(filepath=file_path)
            graph = ox.routing.add_edge_speeds(graph)
            graph = ox.routing.add_edge_travel_times(graph)

            origin_node = ox.distance.nearest_nodes(graph, X=longitude_origin, Y=latitude_origin)
            destination_node = ox.distance.nearest_nodes(graph, X=longitude_destination, Y=latitude_destination)
            route = ox.shortest_path(graph, origin_node, destination_node, weight='travel_time')
            edge_lengths = ox.routing.route_to_gdf(graph, route)['length']

            return {"distance_meters": round(sum(edge_lengths))}
        except Exception as e:
            return {"error": str(e)}
        
    