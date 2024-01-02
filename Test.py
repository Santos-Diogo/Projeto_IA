import networkx as nx
import heapq

def euclidean_distance(point1, point2):
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) ** 0.5

def minimum_spanning_tree(graph):
    mst_edges = list(nx.minimum_spanning_edges(graph, algorithm='kruskal', data=False))
    return mst_edges

def traveling_salesman_astar(graph, start_node):
    def heuristic(node):
        return 0  # MST heurística admissível

    priority_queue = [(0, start_node, set([start_node]))]  # (f, node, visited_set)
    
    while priority_queue:
        f, current_node, visited_set = heapq.heappop(priority_queue)

        if len(visited_set) == len(graph.nodes):
            return f  # Chegamos ao final, retorna o custo total do caminho

        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited_set:
                new_cost = graph[current_node][neighbor]['weight']
                new_f = f + new_cost + heuristic(neighbor)
                new_visited_set = visited_set.copy()
                new_visited_set.add(neighbor)
                heapq.heappush(priority_queue, (new_f, neighbor, new_visited_set))

    return float('inf')  # Caso algo dê errado ou não seja possível encontrar um caminho

# Exemplo de uso:
points = {'A': (0, 0), 'B': (1, 2), 'C': (3, 1), 'D': (4, 3)}
graph = nx.Graph()

for node1, pos1 in points.items():
    for node2, pos2 in points.items():
        if node1 != node2:
            distance = euclidean_distance(pos1, pos2)
            graph.add_edge(node1, node2, weight=distance)

start_node = 'A'
mst_edges = minimum_spanning_tree(graph)
mst_graph = nx.Graph()
mst_graph.add_edges_from(mst_edges, weight='weight')

total_cost = traveling_salesman_astar(mst_graph, start_node)
print(f"Custo total do caminho usando MST heurística admissível: {total_cost}")
