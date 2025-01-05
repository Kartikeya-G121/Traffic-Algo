// Initialize map centered on Manhattan
const map = L.map('map').setView([40.7831, -73.9712], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// State variables
let startMarker = null;
let endMarker = null;
let routeLine = null;

// DOM elements
const calculateBtn = document.getElementById('calculateBtn');
const clearBtn = document.getElementById('clearBtn');
const distanceElement = document.getElementById('distance');
const statusElement = document.getElementById('status');

// Custom icons
const startIcon = L.icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34]
});

const endIcon = L.icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34]
});

// Event handlers
map.on('click', (e) => {
    const latlng = e.latlng;
    
    if (!startMarker) {
        startMarker = L.marker(latlng, {icon: startIcon, draggable: true})
            .addTo(map)
            .bindPopup('Start Point');
        statusElement.textContent = 'Start point set. Click to set end point.';
    } else if (!endMarker) {
        endMarker = L.marker(latlng, {icon: endIcon, draggable: true})
            .addTo(map)
            .bindPopup('End Point');
        statusElement.textContent = 'End point set. Click Calculate Route to find path.';
    }
});

calculateBtn.addEventListener('click', async () => {
    if (!startMarker || !endMarker) {
        statusElement.textContent = 'Please set both start and end points first.';
        return;
    }

    statusElement.textContent = 'Calculating shortest path...';
    
    try {
        const response = await fetch('/api/calculate_route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                start_lat: startMarker.getLatLng().lat,
                start_lng: startMarker.getLatLng().lng,
                end_lat: endMarker.getLatLng().lat,
                end_lng: endMarker.getLatLng().lng,
                algorithm: 'dijkstra'
            }),
        });

        const data = await response.json();
        
        if (data.success) {
            // Clear previous route
            if (routeLine) {
                map.removeLayer(routeLine);
            }
            
            // Draw new route
            routeLine = L.polyline(data.route, {color: 'blue', weight: 3}).addTo(map);
            
            // Update status
            distanceElement.textContent = `Distance: ${(data.distance/1000).toFixed(2)} km`;
            statusElement.textContent = 'Route calculated successfully!';
            
            // Fit map to show entire route
            map.fitBounds(routeLine.getBounds(), {padding: [50, 50]});
        } else {
            statusElement.textContent = data.error || 'Could not calculate route.';
        }
    } catch (error) {
        console.error('Error:', error);
        statusElement.textContent = 'Error calculating route.';
    }
});

clearBtn.addEventListener('click', () => {
    // Clear markers
    if (startMarker) {
        map.removeLayer(startMarker);
        startMarker = null;
    }
    if (endMarker) {
        map.removeLayer(endMarker);
        endMarker = null;
    }
    
    // Clear route
    if (routeLine) {
        map.removeLayer(routeLine);
        routeLine = null;
    }
    
    // Reset status
    distanceElement.textContent = '';
    statusElement.textContent = 'Click on map to set start point.';
}); 