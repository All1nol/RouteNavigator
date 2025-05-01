import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import time
import pandas as pd
import tracemalloc
from pathfinding import IterativeDeepeningBidirectionalSearch, AStarSearch
from georgia_map import create_georgia_map
from complexity_analysis import measure_performance

# Set page configuration
st.set_page_config(
    page_title="Pathfinding Algorithms Comparison",
    page_icon="🗺️",
    layout="wide"
)

# Title and introduction
st.title("Pathfinding Algorithm Comparison")
st.markdown("""
This application compares two search algorithms for finding the optimal path from Telavi to Sokhumi in Georgia:
- **Iterative Deepening Bidirectional Search** (Uninformed Search)
- **A* Search Algorithm** (Informed Search)

The comparison includes time complexity (execution time) and space complexity (memory usage).
""")

# Create the map of Georgia
G, pos, city_coords, straight_line_distances = create_georgia_map()

# Display the original map
st.header("Map of Georgia")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Cities and Roads")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', 
            font_size=10, font_weight='bold', ax=ax)
    
    # Draw edge labels (distances)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    
    st.pyplot(fig)

with col2:
    st.subheader("Straight-Line Distances to Sokhumi")
    
    # Create a DataFrame to display the heuristic values
    heuristic_df = pd.DataFrame(
        list(straight_line_distances.items()),
        columns=['City', 'Straight-Line Distance to Sokhumi (km)']
    )
    st.table(heuristic_df)

# Run the search algorithms
if st.button("Run Pathfinding Algorithms"):
    st.header("Pathfinding Results")
    
    # Initialize the algorithms
    idbs = IterativeDeepeningBidirectionalSearch(G)
    astar = AStarSearch(G, straight_line_distances)
    
    # Measure performance of Iterative Deepening Bidirectional Search
    st.subheader("Iterative Deepening Bidirectional Search (Uninformed)")
    idbs_results = measure_performance(
        idbs.search, 
        "Telavi", 
        "Sokhumi"
    )
    
    # Display IDBS results
    idbs_path = idbs_results["path"]
    if idbs_path:
        st.success(f"Path found: {' → '.join(idbs_path)}")
        
        # Calculate total distance
        total_distance = 0
        for i in range(len(idbs_path) - 1):
            total_distance += G[idbs_path[i]][idbs_path[i+1]]['weight']
        
        st.info(f"Total distance: {total_distance} km")
        
        # Visualize the path
        fig1, ax1 = plt.subplots(figsize=(10, 8))
        
        # Draw the graph
        nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightgray', 
                font_size=10, font_weight='bold', ax=ax1)
        
        # Highlight the path
        path_edges = [(idbs_path[i], idbs_path[i+1]) for i in range(len(idbs_path)-1)]
        nx.draw_networkx_nodes(G, pos, nodelist=idbs_path, node_color='green', node_size=700, ax=ax1)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='green', width=3, ax=ax1)
        
        st.pyplot(fig1)
    else:
        st.error("No path found using Iterative Deepening Bidirectional Search.")
    
    # Measure performance of A* Search
    st.subheader("A* Search Algorithm (Informed)")
    astar_results = measure_performance(
        astar.search, 
        "Telavi", 
        "Sokhumi"
    )
    
    # Display A* results
    astar_path = astar_results["path"]
    if astar_path:
        st.success(f"Path found: {' → '.join(astar_path)}")
        
        # Calculate total distance
        total_distance = 0
        for i in range(len(astar_path) - 1):
            total_distance += G[astar_path[i]][astar_path[i+1]]['weight']
        
        st.info(f"Total distance: {total_distance} km")
        
        # Visualize the path
        fig2, ax2 = plt.subplots(figsize=(10, 8))
        
        # Draw the graph
        nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightgray', 
                font_size=10, font_weight='bold', ax=ax2)
        
        # Highlight the path
        path_edges = [(astar_path[i], astar_path[i+1]) for i in range(len(astar_path)-1)]
        nx.draw_networkx_nodes(G, pos, nodelist=astar_path, node_color='blue', node_size=700, ax=ax2)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=3, ax=ax2)
        
        st.pyplot(fig2)
    else:
        st.error("No path found using A* Search.")
    
    # Compare the algorithms
    st.header("Algorithm Comparison")
    
    # Create comparison table
    comparison_data = {
        "Algorithm": ["Iterative Deepening Bidirectional Search", "A* Search"],
        "Execution Time (s)": [idbs_results["execution_time"], astar_results["execution_time"]],
        "Memory Usage (KB)": [idbs_results["memory_usage"] / 1024, astar_results["memory_usage"] / 1024],
        "Nodes Expanded": [idbs_results["nodes_expanded"], astar_results["nodes_expanded"]],
        "Path Length": [len(idbs_path) - 1 if idbs_path else "N/A", len(astar_path) - 1 if astar_path else "N/A"],
        "Total Distance (km)": [
            sum(G[idbs_path[i]][idbs_path[i+1]]['weight'] for i in range(len(idbs_path)-1)) if idbs_path else "N/A",
            sum(G[astar_path[i]][astar_path[i+1]]['weight'] for i in range(len(astar_path)-1)) if astar_path else "N/A"
        ]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.table(comparison_df)
    
    # Create bar charts for visual comparison
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Execution Time Comparison")
        fig3, ax3 = plt.subplots(figsize=(8, 5))
        bars = ax3.bar(
            ["IDBS", "A*"], 
            [idbs_results["execution_time"], astar_results["execution_time"]],
            color=['green', 'blue']
        )
        ax3.set_ylabel("Time (seconds)")
        ax3.set_title("Execution Time")
        
        # Add values on top of bars
        for bar in bars:
            height = bar.get_height()
            ax3.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{height:.6f}',
                ha='center', va='bottom', rotation=0
            )
        
        st.pyplot(fig3)
        
    with col4:
        st.subheader("Memory Usage Comparison")
        fig4, ax4 = plt.subplots(figsize=(8, 5))
        bars = ax4.bar(
            ["IDBS", "A*"], 
            [idbs_results["memory_usage"]/1024, astar_results["memory_usage"]/1024],
            color=['green', 'blue']
        )
        ax4.set_ylabel("Memory (KB)")
        ax4.set_title("Memory Usage")
        
        # Add values on top of bars
        for bar in bars:
            height = bar.get_height()
            ax4.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{height:.2f}',
                ha='center', va='bottom', rotation=0
            )
        
        st.pyplot(fig4)
    
    # Nodes expanded comparison
    st.subheader("Nodes Expanded Comparison")
    fig5, ax5 = plt.subplots(figsize=(10, 5))
    bars = ax5.bar(
        ["IDBS", "A*"], 
        [idbs_results["nodes_expanded"], astar_results["nodes_expanded"]],
        color=['green', 'blue']
    )
    ax5.set_ylabel("Number of Nodes")
    ax5.set_title("Nodes Expanded During Search")
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax5.text(
            bar.get_x() + bar.get_width()/2.,
            height,
            f'{int(height)}',
            ha='center', va='bottom', rotation=0
        )
    
    st.pyplot(fig5)
    
    # Conclusion
    st.header("Conclusion")
    st.markdown("""
    ### Time Complexity
    - **Iterative Deepening Bidirectional Search**: This uninformed search explores nodes systematically without knowledge of the goal.
    - **A* Search**: This informed search uses heuristic information to guide the search toward the goal.
    
    ### Space Complexity
    - **Iterative Deepening Bidirectional Search**: Uses less memory as it doesn't store all explored nodes at once.
    - **A* Search**: Maintains a priority queue of nodes to explore, which can consume more memory.
    
    ### Key Observations
    - A* typically finds the solution faster but may use more memory.
    - Iterative Deepening Bidirectional Search is more memory-efficient but may take longer to find the optimal path.
    - Both algorithms are guaranteed to find the optimal path if one exists.
    """)
