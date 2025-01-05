# Manhattan Traffic Management System

## Overview
A web-based traffic management system that provides optimal route calculation in Manhattan using Dijkstra's algorithm. The system uses real street data from OpenStreetMap and provides an interactive interface for route visualization.

## Features
- Interactive map interface centered on Manhattan
- Dijkstra's algorithm for shortest path finding
- Real-time route calculation
- Distance calculation in meters
- Visual route display on map
- Error handling for invalid inputs
- Responsive web interface

## Technical Architecture

### Backend Components
1. **app.py**
   - Flask web server
   - API endpoints for map data and route calculation
   - Request validation and error handling

2. **map_handler.py**
   - OpenStreetMap data management
   - Graph construction and maintenance
   - Node and edge management
   - Map visualization using Folium

3. **pathfinding.py**
   - Implementation of Dijkstra's algorithm
   - Distance calculations
   - Path optimization

4. **utils.py**
   - Coordinate validation
   - Haversine distance calculation
   - Utility functions

### Frontend Components
1. **index.html**
   - Main user interface
   - Map display
   - Control elements

2. **main.js**
   - User interaction handling
   - API communication
   - Route visualization

3. **style.css**
   - UI styling
   - Responsive design

## Dependencies
- Flask 3.0.0: Web framework
- OSMnx 2.0.0: OpenStreetMap network analysis
- Folium 0.19.2: Map visualization
- NetworkX 3.4.2: Graph operations
- GeoPy 2.4.1: Geographic calculations

## Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Access the interface at `http://localhost:5000`

## Usage
1. Open the web interface
2. Click on the map to set start point (green marker)
3. Click again to set end point (red marker)
4. Click "Calculate Route" to find optimal path
5. View the route and distance information

## Algorithm Details

### Dijkstra's Algorithm
- Guarantees the shortest path between any two points
- Efficient for urban road networks
- Uses edge weights based on real-world distances
- Ideal for city navigation where shortest path is priority
- Time complexity: O(E log V) where E is number of edges and V is number of vertices

## Performance Considerations
- Caches node indices for faster lookups
- Uses Haversine distance for accurate measurements
- Optimized graph creation
- Efficient data structures for route calculations

## Error Handling
- Input validation for coordinates
- Route availability checking
- Graceful error reporting

## Future Improvements
1. Traffic condition integration
2. Time-based routing
3. Multiple waypoint support
4. Route alternatives
5. Real-time traffic updates

## Technical Limitations
1. Limited to Manhattan area
2. Fixed radius of 5000 meters
3. No real-time traffic data
4. Single route calculation at a time

## Security Considerations
- Input validation for all API endpoints
- Error message sanitization
- Rate limiting considerations
- Coordinate range validation 