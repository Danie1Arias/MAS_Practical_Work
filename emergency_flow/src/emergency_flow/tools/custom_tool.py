from typing import Type, Tuple
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import osmnx as ox
import networkx as nx

class ShortestPathInput(BaseModel):
    """Input schema for ShortestPathTool."""
    graph_path: str = Field(..., description="Path to the OSMnx graph file in .graphml format.")
    coord1: Tuple[float, float] = Field(..., description="Tuple (lat, lon) for the first location.")
    coord2: Tuple[float, float] = Field(..., description="Tuple (lat, lon) for the second location.")

class ShortestPathTool(BaseTool):
    name: str = "OSMnx Shortest Path Tool"
    description: str = (
        "Computes the shortest distance and path between two locations in a city using an OSMnx graph. "
        "Returns the distance in meters and the path as a list of nodes."
    )
    args_schema: Type[BaseModel] = ShortestPathInput

    def _run(self, graph_path: str, coord1: Tuple[float, float], coord2: Tuple[float, float]) -> dict:
        try:
            # Load the graph from the provided path
            graph = ox.load_graphml(filepath=graph_path)

            # Find the nearest nodes in the graph to the given coordinates
            node1 = ox.distance.nearest_nodes(graph, X=coord1[1], Y=coord1[0])
            node2 = ox.distance.nearest_nodes(graph, X=coord2[1], Y=coord2[0])

            # Compute the shortest path between the nodes
            distance = nx.shortest_path_length(graph, node1, node2, weight='length')
            path = nx.shortest_path(graph, node1, node2, weight='length')

            return {"distance_meters": distance, "path_nodes": path}
        except Exception as e:
            return {"error": str(e)}