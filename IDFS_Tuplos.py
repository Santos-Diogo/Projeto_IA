def format_path(path):          #Pega numa lista de nodes, em formato tuplo e separa por -
    return ' -> '.join(node[0] for node in path)

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
            return result, expanded_nodes, depth

    return None, [], None

# Example graph with tuple nodes
graph = {
    ('A',): [('B',), ('C',)],
    ('B',): [('D',), ('E',)],
    ('C',): [('F',)],
    ('D',): [('G',), ('H',)],
    ('E',): [('H',), ('I',)],
    ('F',): [('J',)],
    ('G',): [('K',), ('L',)],
    ('H',): [('M',)],
    ('I',): [],
    ('J',): [('N',), ('O',)],
    ('K',): [],
    ('L',): [],
    ('M',): [],
    ('N',): [],
    ('O',): []
}

# Neighbors function for tuple-based graph
def neighbors(node):
    return graph[node]

# Run the algorithm
start = ('A',)
goal = ('M',)
solution, expanded_nodes, depth = iterative_deepening_search(start, goal, neighbors)

# Format the solution and expanded nodes
formatted_solution = format_path(solution)
formatted_expanded_nodes = format_path(expanded_nodes)

# Create the final tuple output
final_output = (formatted_solution, formatted_expanded_nodes, depth)
print(final_output)

