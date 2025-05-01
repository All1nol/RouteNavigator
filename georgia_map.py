import networkx as nx
import math
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path

def create_eurasia_map():
    """
    Create a graph representation of major cities between Paris and Beijing (Pekin),
    with road and rail connections between them.
    
    Returns:
        G: NetworkX graph representing the map
        pos: Dictionary of node positions for visualization
        city_coords: Dictionary of city coordinates
        straight_line_distances: Dictionary of straight-line distances to Beijing
    """
    # Create an undirected graph
    G = nx.Graph()
    
    # Define approximate city coordinates (longitude, latitude scaled for visualization)
    # Roughly accurate for relative positioning
    city_coords = {
        # Western Europe
        'Paris': (2.35, 48.85),
        'Berlin': (13.4, 52.5),
        'Warsaw': (21.0, 52.2),
        'Vienna': (16.4, 48.2),
        'Munich': (11.6, 48.1),
        'Prague': (14.4, 50.1),
        'Budapest': (19.1, 47.5),
        
        # Eastern Europe and Russia
        'Kiev': (30.5, 50.4),
        'Moscow': (37.6, 55.8),
        'Minsk': (27.6, 53.9),
        'St. Petersburg': (30.3, 59.9),
        'Volgograd': (44.5, 48.7),
        'Astana': (71.4, 51.1),
        'Novosibirsk': (82.9, 55.0),
        'Irkutsk': (104.3, 52.3),
        
        # Central Asia
        'Almaty': (76.9, 43.2),
        'Tashkent': (69.2, 41.3),
        'Bishkek': (74.6, 42.9),
        
        # China and East Asia
        'Urumqi': (87.6, 43.8),
        'Lanzhou': (103.8, 36.1),
        'Xi\'an': (108.9, 34.3),
        'Beijing': (116.4, 39.9)
    }
    
    # Define road and rail connections with distances in km
    connections = [
        # Western Europe
        ('Paris', 'Berlin', 1054),
        ('Berlin', 'Warsaw', 574),
        ('Berlin', 'Prague', 350),
        ('Berlin', 'Munich', 585),
        ('Munich', 'Vienna', 355),
        ('Vienna', 'Budapest', 243),
        ('Prague', 'Warsaw', 693),
        ('Prague', 'Vienna', 331),
        ('Warsaw', 'Minsk', 543),
        
        # Eastern Europe
        ('Warsaw', 'Kiev', 785),
        ('Minsk', 'Moscow', 717),
        ('Minsk', 'Kiev', 433),
        ('Moscow', 'St. Petersburg', 705),
        ('Moscow', 'Kiev', 871),
        ('Moscow', 'Volgograd', 981),
        
        # Russia to Central Asia
        ('Moscow', 'Astana', 2700),
        ('Volgograd', 'Astana', 1900),
        ('Astana', 'Almaty', 1300),
        ('Astana', 'Novosibirsk', 1400),
        ('Almaty', 'Bishkek', 237),
        ('Almaty', 'Tashkent', 810),
        ('Bishkek', 'Tashkent', 560),
        
        # Central Asia to China
        ('Almaty', 'Urumqi', 1000),
        ('Tashkent', 'Urumqi', 1500),
        ('Bishkek', 'Urumqi', 990),
        
        # Russia to Siberia
        ('Moscow', 'Novosibirsk', 3200),
        ('Novosibirsk', 'Irkutsk', 1800),
        
        # Through China
        ('Urumqi', 'Lanzhou', 1900),
        ('Irkutsk', 'Beijing', 2200),
        ('Lanzhou', 'Xi\'an', 680),
        ('Xi\'an', 'Beijing', 1100)
    ]
    
    # Add cities as nodes
    for city, coords in city_coords.items():
        # Scale coordinates for better visualization
        scaled_x = (coords[0] - 2) / 30  # Normalize to [0, 1] range approximately
        scaled_y = (coords[1] - 30) / 30
        G.add_node(city, pos=(scaled_x, scaled_y), lon=coords[0], lat=coords[1])
    
    # Add connections as edges
    for city1, city2, distance in connections:
        G.add_edge(city1, city2, weight=distance)
    
    # Get positions for visualization
    pos = {city: (city_coords[city][0]/30, city_coords[city][1]/30) for city in G.nodes()}
    
    # Calculate straight-line distances to Beijing
    beijing_coords = city_coords['Beijing']
    straight_line_distances = {}
    
    # Convert graph to distance matrix for Dijkstra
    cities = list(G.nodes())
    n = len(cities)
    city_to_idx = {city: i for i, city in enumerate(cities)}
    
    # Create distance matrix for Dijkstra algorithm
    dist_matrix = np.zeros((n, n))
    for city1, city2, distance in connections:
        idx1 = city_to_idx[city1]
        idx2 = city_to_idx[city2]
        dist_matrix[idx1, idx2] = distance
        dist_matrix[idx2, idx1] = distance  # Undirected graph
    
    # Convert to sparse matrix for efficiency
    graph = csr_matrix(dist_matrix)
    
    try:
        # Find Beijing's index
        beijing_idx = city_to_idx['Beijing']
        
        # Get distances using Dijkstra's algorithm
        dist_matrix, predecessors = shortest_path(
            csgraph=graph, directed=False, 
            indices=beijing_idx, return_predecessors=True
        )
        
        # Create the straight-line distances dictionary
        for city, idx in city_to_idx.items():
            straight_line_distances[city] = int(dist_matrix[idx])
    except:
        # Fallback to Euclidean distances scaled to kilometers
        for city, coords in city_coords.items():
            # Calculate distance to Beijing (approximate haversine formula)
            lat1, lon1 = coords[1], coords[0]
            lat2, lon2 = beijing_coords[1], beijing_coords[0]
            
            # Convert to radians
            lat1, lon1 = math.radians(lat1), math.radians(lon1)
            lat2, lon2 = math.radians(lat2), math.radians(lon2)
            
            # Haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            
            # Earth radius in kilometers
            r = 6371
            distance = r * c
            
            straight_line_distances[city] = int(distance)
    
    return G, pos, city_coords, straight_line_distances

# Keep the old function name for compatibility with existing code
create_georgia_map = create_eurasia_map
