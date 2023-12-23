def format_path(path):
    return '-'.join(node for node in path)

def iterative_deepening_search(start, goal, neighbors_func, max_depth=50):
    def depth_limited_search(node, depth, expanded_nodes):
        expanded_nodes.append(node)
        if node == goal:
            return [node]
        if depth == 0:
            return None
        for child in neighbors_func(node):
            path = depth_limited_search(child, depth - 1, expanded_nodes)
            if path is not None:
                return [node] + path
        return None

    for depth in range(max_depth):
        expanded_nodes = []
        result = depth_limited_search(start, depth, expanded_nodes)
        if result is not None:
            formatted_solution = format_path(result)
            formatted_expanded_nodes = format_path(expanded_nodes)
            return (formatted_solution, formatted_expanded_nodes, depth)

    return (None, None, None)

# Define a simple graph
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': ['G', 'H'],
    'E': ['H', 'I'],
    'F': ['J'],
    'G': ['K', 'L'],
    'H': ['M'],
    'I': [],
    'J': ['N', 'O'],
    'K': [],
    'L': [],
    'M': [],
    'N': [],
    'O': []
}

# Define the neighbors function
def neighbors(node):
    return graph[node]

# Define start and goal
start = 'A'
goal = 'M'

# Run the algorithm
solution, expanded_nodes, depth = iterative_deepening_search(start, goal, neighbors)

# Print the final output
print("Solution:", solution)
print("Order of expansion:", expanded_nodes)
print("Depth of the solution:", depth)
