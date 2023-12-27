import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue
from collections import OrderedDict

def iterative_deepening_dfs(start, target):
    visited = set()  # Conjunto para rastrear nós visitados
    path = []  # Caminho para a solução
    order_of_expansion = []  # Ordem de expansão

    def dfs(node, depth):
        if node["value"] in visited:
            return False
        visited.add(node["value"])
        order_of_expansion.append(node["value"])
        if node["value"] == target:
            path.append(node["value"])
            return True
        if depth > 0:
            for child in node["children"]:
                if dfs(child, depth - 1):
                    path.append(node["value"])
                    return True
        return False

    depth = 0
    while not dfs(start, depth):
        visited.clear()  # Limpar nós visitados para a próxima iteração
        depth += 1
    unique_list = list(OrderedDict.fromkeys(order_of_expansion))

    return path[::-1], unique_list, depth

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

def convert_graph(graph):
    new_graph = {}
    for node, children in graph.items():
        # Criando a estrutura de nó esperada pela função iterative_deepening_dfs
        new_graph[node] = {"value": node, "children": []}
        for child in children:
            new_graph[node]["children"].append({"value": child, "children": []})

    # Conectando os nós filhos aos pais
    for node, node_info in new_graph.items():
        for child in node_info["children"]:
            child.update(new_graph[child["value"]])

    return new_graph

converted_graph = convert_graph(graph)

result = iterative_deepening_dfs(converted_graph[('A',)], ('M',))

converted_graph = convert_graph(graph)
solution, order_of_expansion, depth = iterative_deepening_dfs(converted_graph[('A',)], ('M',))

print(solution, order_of_expansion, depth)