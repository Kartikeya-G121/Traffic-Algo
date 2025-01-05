import networkx as nx
from typing import List, Tuple

class PathFinder:
    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def dijkstra(self, start: int, end: int) -> tuple[List[int], float]:
        """
        Implementation of Dijkstra's algorithm for finding the shortest path.
        
        Args:
            start (int): Starting node index
            end (int): End node index
            
        Returns:
            tuple[List[int], float]: A tuple containing:
                - List of node indices forming the path
                - Total distance of the path in meters
        """
        try:
            path = nx.dijkstra_path(self.graph, start, end, weight='weight')
            path_length = nx.dijkstra_path_length(self.graph, start, end, weight='weight')
            return path, path_length
        except nx.NetworkXNoPath:
            return [], float('inf')

    def get_algorithm(self, name: str):
        """Get pathfinding algorithm by name."""
        if name.lower() != 'dijkstra':
            return None
        return self.dijkstra 