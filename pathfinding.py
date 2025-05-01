from collections import deque
import heapq

class IterativeDeepeningBidirectionalSearch:
    """
    Implementation of Iterative Deepening Bidirectional Search algorithm.
    This is an uninformed search that combines iterative deepening with 
    bidirectional search to find the optimal path.
    """
    
    def __init__(self, graph):
        """Initialize with the graph representing cities and roads."""
        self.graph = graph
        self.nodes_expanded = 0
    
    def search(self, start, goal):
        """
        Find the optimal path from start to goal using Iterative Deepening Bidirectional Search.
        
        Args:
            start: Starting city
            goal: Destination city
            
        Returns:
            list: Path from start to goal if found, empty list otherwise
        """
        # Reset counter for nodes expanded
        self.nodes_expanded = 0
        
        # Check if start or goal is not in the graph
        if start not in self.graph or goal not in self.graph:
            return []
        
        # If start is the goal, return it
        if start == goal:
            return [start]
        
        # Iterative Deepening
        max_depth = 1
        while True:
            # Run bidirectional search with current depth limit
            path = self._bidirectional_search(start, goal, max_depth)
            
            # If a path is found or maximum depth (size of graph) is reached, return the result
            if path or max_depth >= len(self.graph):
                return path
            
            # Increase depth limit
            max_depth += 1
    
    def _bidirectional_search(self, start, goal, max_depth):
        """
        Perform bidirectional search with a depth limit.
        
        Args:
            start: Starting city
            goal: Destination city
            max_depth: Maximum depth to search
            
        Returns:
            list: Path from start to goal if found, empty list otherwise
        """
        # Forward search
        forward_visited = {start: None}  # node -> parent
        forward_frontier = deque([(start, 0)])  # (node, depth)
        
        # Backward search
        backward_visited = {goal: None}  # node -> parent
        backward_frontier = deque([(goal, 0)])  # (node, depth)
        
        # Run search from both directions
        while forward_frontier and backward_frontier:
            # Forward search step
            intersection = self._search_step(forward_frontier, forward_visited, backward_visited, max_depth, True)
            if intersection:
                return self._reconstruct_path(intersection, forward_visited, backward_visited)
            
            # Backward search step
            intersection = self._search_step(backward_frontier, backward_visited, forward_visited, max_depth, False)
            if intersection:
                return self._reconstruct_path(intersection, forward_visited, backward_visited)
        
        # No path found within the depth limit
        return []
    
    def _search_step(self, frontier, visited, other_visited, max_depth, is_forward):
        """
        Perform one step of the search.
        
        Args:
            frontier: Queue of nodes to explore
            visited: Dictionary of visited nodes and their parents
            other_visited: Dictionary of visited nodes from the other direction
            max_depth: Maximum depth to search
            is_forward: Whether this is the forward search
            
        Returns:
            str: Intersection node if found, None otherwise
        """
        if not frontier:
            return None
        
        # Get the next node to explore
        current, depth = frontier.popleft()
        
        # Skip if we've already reached the max depth
        if depth > max_depth:
            return None
        
        # Increment nodes expanded counter
        self.nodes_expanded += 1
        
        # Check neighbors
        for neighbor in self.graph.neighbors(current):
            # Skip if already visited from this direction
            if neighbor in visited:
                continue
            
            # Record the parent
            visited[neighbor] = current
            
            # Check if this node has been visited from the other direction
            if neighbor in other_visited:
                return neighbor  # Intersection found
            
            # Add to frontier for next iteration if not at max depth
            if depth < max_depth:
                frontier.append((neighbor, depth + 1))
        
        return None
    
    def _reconstruct_path(self, intersection, forward_visited, backward_visited):
        """
        Reconstruct the path from the intersection node.
        
        Args:
            intersection: Node where the two searches meet
            forward_visited: Dictionary of nodes visited from the start
            backward_visited: Dictionary of nodes visited from the goal
            
        Returns:
            list: Complete path from start to goal
        """
        # Build the path from start to intersection
        forward_path = []
        current = intersection
        while current is not None:
            forward_path.append(current)
            current = forward_visited[current]
        forward_path.reverse()
        
        # Build the path from intersection to goal
        backward_path = []
        current = backward_visited[intersection]
        while current is not None:
            backward_path.append(current)
            current = backward_visited[current]
        
        # Combine the paths
        return forward_path + backward_path


class AStarSearch:
    """
    Implementation of A* Search algorithm.
    This is an informed search that uses a heuristic to guide the search.
    """
    
    def __init__(self, graph, heuristic):
        """
        Initialize with the graph and heuristic function.
        
        Args:
            graph: NetworkX graph representing cities and roads
            heuristic: Dictionary mapping city names to straight-line distances to the goal
        """
        self.graph = graph
        self.heuristic = heuristic
        self.nodes_expanded = 0
    
    def search(self, start, goal):
        """
        Find the optimal path from start to goal using A* Search.
        
        Args:
            start: Starting city
            goal: Destination city
            
        Returns:
            list: Path from start to goal if found, empty list otherwise
        """
        # Reset counter for nodes expanded
        self.nodes_expanded = 0
        
        # Check if start or goal is not in the graph
        if start not in self.graph or goal not in self.graph:
            return []
        
        # If start is the goal, return it
        if start == goal:
            return [start]
        
        # Priority queue: (f_score, node)
        # f_score = g_score + heuristic, where g_score is the cost from start to node
        frontier = [(self.heuristic[start], start)]
        
        # Dictionary to store the cost from start to each node
        g_score = {start: 0}
        
        # Dictionary to store the parent of each node
        came_from = {start: None}
        
        while frontier:
            # Get the node with the lowest f_score
            _, current = heapq.heappop(frontier)
            
            # If we've reached the goal, reconstruct and return the path
            if current == goal:
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path
            
            # Increment nodes expanded counter
            self.nodes_expanded += 1
            
            # Check all neighbors
            for neighbor in self.graph.neighbors(current):
                # Calculate tentative g_score
                tentative_g_score = g_score[current] + self.graph[current][neighbor]['weight']
                
                # If we found a better path to the neighbor, update
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # Record this better path
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic[neighbor]
                    
                    # Add to frontier
                    heapq.heappush(frontier, (f_score, neighbor))
        
        # No path found
        return []
