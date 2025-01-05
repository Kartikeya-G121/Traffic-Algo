import osmnx as ox
import networkx as nx
import folium
from typing import Tuple, List, Optional, Dict
from utils import validate_coordinates, calculate_distance

class MapHandler:
    def __init__(self):
        self.graph = None
        self.nodes = []
        self.edges = []
        self.node_to_idx = {}  # Cache for node index lookup

    def load_map_area(self, lat: float, lon: float, radius: float = 5000):
        """Load map data for a specific area"""
        try:
            if not validate_coordinates(lat, lon):
                return False

            # Get only drivable roads
            self.graph = ox.graph_from_point(
                (lat, lon), 
                dist=radius, 
                network_type='drive',
                simplify=True,
                retain_all=False
            )
            
            # Convert node coordinates to list format and store node mapping
            self.nodes = []
            self.node_to_idx = {}
            for i, (node, data) in enumerate(self.graph.nodes(data=True)):
                self.nodes.append((data['y'], data['x']))
                self.node_to_idx[node] = i
            
            # Create edges list with indices
            self.edges = [(self.node_to_idx[u], self.node_to_idx[v]) 
                         for u, v in self.graph.edges()]
            
            return True
        except Exception as e:
            print(f"Error loading map: {str(e)}")
            return False

    def get_nearest_node(self, lat: float, lon: float) -> Optional[int]:
        """Find the nearest node to given coordinates"""
        if not self.graph or not validate_coordinates(lat, lon):
            return None
        
        try:
            # Find the nearest node in the graph
            nearest_node = ox.distance.nearest_nodes(self.graph, lon, lat)
            return self.node_to_idx.get(nearest_node)
        except Exception as e:
            print(f"Error finding nearest node: {str(e)}")
            return None

    def get_graph_for_pathfinding(self) -> nx.Graph:
        """Prepare graph for pathfinding algorithms"""
        if not self.graph:
            return nx.Graph()

        # Create a new graph with sequential indices
        G = nx.Graph()
        
        # Add nodes with positions
        for i, coord in enumerate(self.nodes):
            G.add_node(i, pos=coord)
        
        # Add edges with weights based on Haversine distance
        for u_idx, v_idx in self.edges:
            u_coord = self.nodes[u_idx]
            v_coord = self.nodes[v_idx]
            weight = calculate_distance(u_coord, v_coord)
            G.add_edge(u_idx, v_idx, weight=weight)
        
        return G

    def create_folium_map(self, center: Tuple[float, float], zoom: int = 13) -> folium.Map:
        """Create a Folium map centered at the specified location."""
        return folium.Map(
            location=center,
            zoom_start=zoom,
            tiles='OpenStreetMap'
        )

    def add_route_to_map(self, folium_map: folium.Map, 
                        path: List[int], color: str = 'red') -> folium.Map:
        """Add a route to the Folium map."""
        if not path:
            return folium_map

        route_coords = []
        for node_id in path:
            if node_id < len(self.nodes):
                route_coords.append(self.nodes[node_id])

        if len(route_coords) > 1:
            folium.PolyLine(
                locations=route_coords,
                weight=2,
                color=color,
                opacity=0.8
            ).add_to(folium_map)

        return folium_map