from math import radians, sin, cos, sqrt, atan2

def validate_coordinates(lat: float, lon: float) -> bool:
    """Validate if coordinates are within valid ranges."""
    try:
        return -90 <= float(lat) <= 90 and -180 <= float(lon) <= 180
    except (ValueError, TypeError):
        return False

def calculate_distance(coord1: tuple[float, float], coord2: tuple[float, float]) -> float:
    """
    Calculate the Haversine distance between two points on Earth.
    coord1 and coord2 are tuples of (latitude, longitude)
    Returns distance in meters
    """
    R = 6371000  # Earth's radius in meters

    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Convert coordinates to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Haversine formula
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c 