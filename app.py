from flask import Flask, jsonify, request, render_template
from map_handler import MapHandler
from pathfinding import PathFinder
from utils import validate_coordinates

app = Flask(__name__)

# Initialize map handler with Manhattan data
map_handler = MapHandler()
map_handler.load_map_area(40.7831, -73.9712, radius=5000)

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/map_data', methods=['GET'])
def get_map_data():
    """Get map nodes and edges"""
    if not map_handler.nodes or not map_handler.edges:
        return jsonify({
            'success': False,
            'error': 'Map data not loaded'
        })
    return jsonify({
        'success': True,
        'nodes': map_handler.nodes,
        'edges': map_handler.edges
    })

@app.route('/api/calculate_route', methods=['POST'])
def calculate_route():
    """Calculate route between two points"""
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            })

        # Validate input data
        required_fields = ['start_lat', 'start_lng', 'end_lat', 'end_lng', 'algorithm']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            })

        # Validate coordinates
        start_coords = (data['start_lat'], data['start_lng'])
        end_coords = (data['end_lat'], data['end_lng'])
        
        if not (validate_coordinates(*start_coords) and validate_coordinates(*end_coords)):
            return jsonify({
                'success': False,
                'error': 'Invalid coordinates'
            })

        algorithm = data['algorithm'].lower()
        if algorithm not in ['dijkstra', 'a_star', 'bellman_ford']:
            return jsonify({
                'success': False,
                'error': 'Invalid algorithm'
            })

        # Get nearest nodes
        start_node = map_handler.get_nearest_node(*start_coords)
        end_node = map_handler.get_nearest_node(*end_coords)

        if start_node is None or end_node is None:
            return jsonify({
                'success': False,
                'error': 'Could not find nearest nodes'
            })

        # Calculate route
        graph = map_handler.get_graph_for_pathfinding()
        pathfinder = PathFinder(graph)
        path_func = pathfinder.get_algorithm(algorithm)

        if not path_func:
            return jsonify({
                'success': False,
                'error': f'Algorithm {algorithm} not implemented'
            })

        path, distance = path_func(start_node, end_node)
        
        if not path or distance == float('inf'):
            return jsonify({
                'success': False,
                'error': 'No route found between points'
            })

        # Convert path indices to coordinates
        route_coords = [map_handler.nodes[idx] for idx in path]
        return jsonify({
            'success': True,
            'route': route_coords,
            'distance': distance
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True) 