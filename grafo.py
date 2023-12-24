import networkx as nx
import matplotlib.pyplot as plt

def create_graph(graph_dict):
    G = nx.Graph()

    for node, connections in graph_dict.items():
        if len(node) == 1:  # Caso a posição não seja fornecida, definimos como (0, 0)
            node_name, node_pos = node[0], (0, 0)
        elif len(node) == 2:
            node_name, node_pos = node
        else:
            raise ValueError("Cada entrada do dicionário deve ter 1 ou 2 elementos.")

        G.add_node(node_name, pos=node_pos)
        for connection, cost in connections:
            G.add_edge(node_name, connection, weight=cost)

    return G

# Cálculo da heurística, que para já ainda não usamos 
# def calculate_heuristic(node_start_pos, node_target_pos):
#     if node_start_pos is not None and node_target_pos is not None:
#         return ((node_start_pos[0] - node_target_pos[0]) ** 2 + (node_start_pos[1] - node_target_pos[1]) ** 2) ** 0.5 * 100
#     else:
#         return 0

def visualize_graph(graph):
    pos = nx.get_node_attributes(graph, 'pos') if 'pos' in nx.get_node_attributes(graph, 'pos') else nx.spring_layout(graph, seed=455)
    labels = nx.get_edge_attributes(graph, 'weight')

    nx.draw(graph, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_color='black')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

    plt.title("Grafo Visual com Heurística")
    plt.show()

if __name__ == "__main__":
    graph_dict = {
        ('Vila Nova de F',): [('Gavião', 5), ('Antas', 4), ('Calendário', 7), ('Mouquim', 3)],
        ('Antas',): [('Calendário', 2), ('Requião', 6), ('Seide', 3)],
        ('Calendário',): [('Brufe', 1)],
        ('Gavião', ): [('Vale', 1), ('Mouquim', 4), ('Antas', 5)],
        ('Requião', ): [('Vale', 5), ('Seide', 8)],
        ('Brufe', ): [('Louro', 9), ('Outiz', 4)],
        ('Outiz', ): [('Vilarinho', 8), ('Louro', 4)],
    }

    graph = create_graph(graph_dict)
    visualize_graph(graph)
