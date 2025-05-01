import networkx as nx
import math

def create_georgia_map():
    """
    Create a graph representation of cities in Georgia with roads connecting them.
    
    Returns:
        G: NetworkX graph representing the map
        pos: Dictionary of node positions for visualization
        city_coords: Dictionary of city coordinates
        straight_line_distances: Dictionary of straight-line distances to Sokhumi
    """
    # Create an undirected graph
    G = nx.Graph()
    
    # Define city coordinates (approximate lat/long as x,y for simplicity)
    # These are approximate coordinates for visualization purposes
    city_coords = {
        "Telavi": (0.8, 0.5),
        "Tbilisi": (0.6, 0.3),
        "Rustavi": (0.7, 0.2),
        "Gori": (0.4, 0.4),
        "Kutaisi": (0.3, 0.6),
        "Zugdidi": (0.2, 0.8),
        "Batumi": (0.1, 0.3),
        "Sokhumi": (0.1, 0.9),
        "Poti": (0.1, 0.7),
        "Akhaltsikhe": (0.3, 0.2),
        "Gagra": (0.05, 1.0),
        "Tskhinvali": (0.35, 0.5),
        "Mestia": (0.25, 0.9),
        "Ambrolauri": (0.4, 0.7),
        "Akhmeta": (0.7, 0.6)
    }
    
    # Add cities as nodes with positions
    for city, coords in city_coords.items():
        G.add_node(city, pos=coords)
    
    # Add roads as edges with distances (in km)
    roads = [
        ("Telavi", "Tbilisi", 70),
        ("Telavi", "Akhmeta", 30),
        ("Tbilisi", "Rustavi", 35),
        ("Tbilisi", "Gori", 85),
        ("Gori", "Kutaisi", 125),
        ("Kutaisi", "Zugdidi", 110),
        ("Zugdidi", "Sokhumi", 90),
        ("Batumi", "Poti", 70),
        ("Poti", "Zugdidi", 60),
        ("Kutaisi", "Poti", 100),
        ("Batumi", "Kutaisi", 150),
        ("Tbilisi", "Akhaltsikhe", 210),
        ("Akhaltsikhe", "Batumi", 190),
        ("Sokhumi", "Gagra", 80),
        ("Gori", "Tskhinvali", 30),
        ("Zugdidi", "Mestia", 130),
        ("Kutaisi", "Ambrolauri", 90),
        ("Ambrolauri", "Mestia", 120),
        ("Akhmeta", "Ambrolauri", 170),
        ("Gori", "Akhmeta", 130),
        ("Tbilisi", "Akhmeta", 110)
    ]
    
    # Add the roads to the graph
    for city1, city2, distance in roads:
        G.add_edge(city1, city2, weight=distance)
    
    # Calculate straight-line distances to Sokhumi for heuristic
    sokhumi_coords = city_coords["Sokhumi"]
    straight_line_distances = {}
    
    for city, coords in city_coords.items():
        # Calculate Euclidean distance and scale it to approximate kilometers
        dx = coords[0] - sokhumi_coords[0]
        dy = coords[1] - sokhumi_coords[1]
        euclidean_distance = math.sqrt(dx**2 + dy**2)
        
        # Scale to make it comparable to the road distances (approximate)
        scaled_distance = euclidean_distance * 250
        
        straight_line_distances[city] = int(scaled_distance)
    
    # Get positions for visualization
    pos = nx.get_node_attributes(G, 'pos')
    
    return G, pos, city_coords, straight_line_distances
