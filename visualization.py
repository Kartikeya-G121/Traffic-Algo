import pygame
import numpy as np
from typing import List, Tuple, Optional

class Visualizer:
    def __init__(self, width: int = 800, height: int = 600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Traffic Management System - Route Visualization")
        self.background_color = (255, 255, 255)
        self.node_color = (100, 100, 100)
        self.edge_color = (200, 200, 200)
        self.route_color = (255, 0, 0)
        self.node_radius = 5
        self.running = False

    def normalize_coordinates(self, nodes: List[Tuple[float, float]]) -> List[Tuple[int, int]]:
        """Convert geographic coordinates to screen coordinates."""
        if not nodes:
            return []

        lats, lons = zip(*nodes)
        min_lat, max_lat = min(lats), max(lats)
        min_lon, max_lon = min(lons), max(lons)

        lat_range = max_lat - min_lat
        lon_range = max_lon - min_lon

        padding = 50
        screen_width = self.width - 2 * padding
        screen_height = self.height - 2 * padding

        normalized = []
        for lat, lon in nodes:
            x = int(padding + (lon - min_lon) * screen_width / lon_range)
            y = int(padding + (lat - min_lat) * screen_height / lat_range)
            normalized.append((x, y))

        return normalized

    def draw_graph(self, nodes: List[Tuple[float, float]], 
                  edges: List[Tuple[int, int]], 
                  path: Optional[List[int]] = None):
        """Draw the graph with nodes, edges, and highlighted path."""
        self.screen.fill(self.background_color)
        
        # Normalize coordinates to screen space
        screen_nodes = self.normalize_coordinates(nodes)

        # Draw edges
        for start, end in edges:
            if start < len(screen_nodes) and end < len(screen_nodes):
                pygame.draw.line(self.screen, self.edge_color,
                               screen_nodes[start], screen_nodes[end], 2)

        # Draw path if provided
        if path and len(path) > 1:
            for i in range(len(path) - 1):
                start, end = path[i], path[i + 1]
                if start < len(screen_nodes) and end < len(screen_nodes):
                    pygame.draw.line(self.screen, self.route_color,
                                   screen_nodes[start], screen_nodes[end], 3)

        # Draw nodes
        for x, y in screen_nodes:
            pygame.draw.circle(self.screen, self.node_color, (x, y), self.node_radius)

        pygame.display.flip()

    def run(self, nodes: List[Tuple[float, float]], 
            edges: List[Tuple[int, int]], 
            path: Optional[List[int]] = None):
        """Run the visualization loop."""
        self.running = True
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.draw_graph(nodes, edges, path)
            clock.tick(30)

        pygame.quit()

    def stop(self):
        """Stop the visualization."""
        self.running = False 