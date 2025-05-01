import time
import tracemalloc

def measure_performance(search_function, start, goal):
    """
    Measure the performance metrics of a search algorithm.
    
    Args:
        search_function: The search algorithm function to measure
        start: The starting node
        goal: The goal node
        
    Returns:
        dict: Dictionary containing performance metrics
    """
    # Start tracking memory
    tracemalloc.start()
    
    # Record the starting time
    start_time = time.time()
    
    # Run the search algorithm
    path = search_function(start, goal)
    
    # Record the ending time
    end_time = time.time()
    
    # Get memory stats
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Get the number of nodes expanded from the search function instance
    # This assumes the search function is a method of a class that tracks nodes_expanded
    nodes_expanded = search_function.__self__.nodes_expanded
    
    # Calculate metrics
    execution_time = end_time - start_time
    memory_usage = peak  # in bytes
    
    # Return the performance metrics
    return {
        "path": path,
        "execution_time": execution_time,
        "memory_usage": memory_usage,
        "nodes_expanded": nodes_expanded
    }
