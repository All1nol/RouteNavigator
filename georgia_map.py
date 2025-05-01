import networkx as nx
import math
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path

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
    
    # Define the graph of Georgia's cities with road distances
    georgia_graph = {
        'Telavi': {'Tbilisi': 90, 'Gurjaani': 38, 'Lagodekhi': 80},
        'Tbilisi': {'Telavi': 90, 'Gori': 68, 'Rustavi': 21, 'Mtskheta': 25},
        'Gurjaani': {'Telavi': 38, 'Sagarejo': 30, 'Kvareli': 45},
        'Sagarejo': {'Gurjaani': 30, 'Tbilisi': 50},
        'Rustavi': {'Tbilisi': 21, 'Marneuli': 40},
        'Marneuli': {'Rustavi': 40, 'Bolnisi': 25, 'Tbilisi': 50},
        'Gori': {'Tbilisi': 68, 'Khashuri': 25, 'Kaspi': 30},
        'Khashuri': {'Gori': 25, 'Kareli': 15, 'Zestaponi': 70},
        'Kutaisi': {'Zestaponi': 33, 'Samtredia': 30, 'Tskaltubo': 15},
        'Zugdidi': {'Samtredia': 100, 'Sokhumi': 102},
        'Sokhumi': {'Zugdidi': 102},
        'Batumi': {'Kobuleti': 25, 'Poti': 80},
        'Poti': {'Samtredia': 60, 'Batumi': 80},
        'Kobuleti': {'Batumi': 25, 'Ozurgeti': 45},
        'Ozurgeti': {'Kobuleti': 45, 'Lanchkhuti': 30},
        'Lanchkhuti': {'Ozurgeti': 30, 'Samtredia': 40},
        'Samtredia': {'Kutaisi': 30, 'Lanchkhuti': 40, 'Poti': 60},
        'Zestaponi': {'Khashuri': 70, 'Kutaisi': 33},
        'Tskaltubo': {'Kutaisi': 15, 'Tsageri': 60},
        'Tsageri': {'Tskaltubo': 60, 'Ambrolauri': 40},
        'Ambrolauri': {'Tsageri': 40, 'Oni': 30},
        'Oni': {'Ambrolauri': 30},
        'Chiatura': {'Zestaponi': 40, 'Sachkhere': 20},
        'Sachkhere': {'Chiatura': 20, 'Tkibuli': 35},
        'Tkibuli': {'Sachkhere': 35, 'Kutaisi': 40},
        'Khoni': {'Kutaisi': 30},
        'Baghdati': {'Kutaisi': 25},
        'Vani': {'Baghdati': 20},
        'Borjomi': {'Khashuri': 30, 'Akhaltsikhe': 50},
        'Akhaltsikhe': {'Borjomi': 50, 'Aspindza': 30},
        'Aspindza': {'Akhaltsikhe': 30},
        'Mtskheta': {'Tbilisi': 25},
        'Kaspi': {'Gori': 30},
        'Kareli': {'Khashuri': 15},
        'Bolnisi': {'Marneuli': 25},
        'Kvareli': {'Gurjaani': 45},
        'Lagodekhi': {'Telavi': 80}
    }
    
    # Convert city names to indices for calculating layout
    cities = list(georgia_graph.keys())
    city_to_idx = {city: i for i, city in enumerate(cities)}
    
    # Create a sparse matrix representation for force-directed layout
    n = len(cities)
    adjacency_matrix = np.zeros((n, n))
    
    for city, neighbors in georgia_graph.items():
        city_idx = city_to_idx[city]
        for neighbor, distance in neighbors.items():
            neighbor_idx = city_to_idx[neighbor]
            adjacency_matrix[city_idx, neighbor_idx] = 1
            adjacency_matrix[neighbor_idx, city_idx] = 1
    
    # Create the graph
    for city, neighbors in georgia_graph.items():
        if city not in G:
            G.add_node(city)
        for neighbor, distance in neighbors.items():
            if neighbor not in G:
                G.add_node(neighbor)
            G.add_edge(city, neighbor, weight=distance)
    
    # Use a force-directed layout for node positions
    pos = nx.spring_layout(G, seed=42)
    
    # Store the positions as city coordinates
    city_coords = {city: pos[city] for city in G.nodes()}
    
    # Calculate the shortest path distances to Sokhumi
    # Calculate straight-line distances to Sokhumi for heuristic
    # Use the Dijkstra algorithm to get actual shortest path distances as a better heuristic
    dist_matrix = adjacency_matrix.copy()
    for i in range(n):
        for j in range(n):
            if i != j and dist_matrix[i, j] == 1:
                city_i = cities[i]
                city_j = cities[j]
                if city_j in georgia_graph[city_i]:
                    dist_matrix[i, j] = georgia_graph[city_i][city_j]
                else:
                    dist_matrix[i, j] = georgia_graph[city_j][city_i]
    
    graph = csr_matrix(dist_matrix)
    
    try:
        # Find Sokhumi's index
        sokhumi_idx = city_to_idx['Sokhumi']
        
        # Get distances from Dijkstra
        dist_matrix, predecessors = shortest_path(csgraph=graph, directed=False, 
                                                 indices=sokhumi_idx, return_predecessors=True)
        
        # Create the straight-line distances dictionary
        straight_line_distances = {}
        for city, idx in city_to_idx.items():
            # Use the actual shortest path distance as the heuristic
            # This is admissible since it's the actual shortest distance
            straight_line_distances[city] = int(dist_matrix[idx])
    except:
        # Fallback to use Euclidean distances if Sokhumi is not in the graph or other error occurs
        sokhumi_coords = city_coords.get('Sokhumi', (0, 0))
        straight_line_distances = {}
        
        for city, coords in city_coords.items():
            # Calculate Euclidean distance and scale it to approximate kilometers
            dx = coords[0] - sokhumi_coords[0]
            dy = coords[1] - sokhumi_coords[1]
            euclidean_distance = math.sqrt(dx**2 + dy**2)
            
            # Scale to make it comparable to the road distances
            scaled_distance = euclidean_distance * 200
            
            straight_line_distances[city] = int(scaled_distance)
    
    return G, pos, city_coords, straight_line_distances
