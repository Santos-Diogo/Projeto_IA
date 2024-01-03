import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue
import math
import heapq
import pdb
from collections import OrderedDict, deque


default = {
    ('Vila Nova de Famalicão',): [('Gavião', 27), ('Antas', 22), ('Calendário', 27), ('Mouquim', 34), ('Louro', 40), ('Brufe', 30)],
    ('Antas',): [('Calendário', 39), ('Esmeriz', 26), ('Vale', 52)],
    ('Calendário',): [('Brufe', 16)],
    ('Gavião', ): [('Vale', 35), ('Mouquim', 30), ('Antas', 50)],
    ('Brufe', ): [('Louro', 34), ('Outiz', 25)],
    ('Outiz', ): [('Vilarinho', 52), ('Louro', 27)],
    ('Mouquim', ): [('Louro', 16)],
    ('Esmeriz', ): [],
    ('Vale', ): [],
    ('Louro', ): [],
    ('Vilarinho', ): []
}

default_pos = {
    'Vila Nova de Famalicão': {'pos': (0, 0), 'connections': [('Gavião', 27), ('Antas', 22), ('Calendário', 27), ('Mouquim', 34), ('Louro', 40), ('Brufe', 30)]},
    'Antas': {'pos' : (0.9, -1.2), 'connections' : [('Calendário', 39), ('Esmeriz', 26), ('Vale', 52)]},
    'Calendário': {'pos' : (-1, -1.466), 'connections' : [('Brufe', 16)]},
    'Gavião': {'pos' : (1.052, 1.736), 'connections' : [('Vila Nova de Famalicão', 27), ('Vale', 35), ('Mouquim', 30), ('Antas', 50)]},
    'Brufe': {'pos' : (-1.396, -0.1), 'connections' : [('Louro', 34), ('Outiz', 25)]},
    'Outiz': {'pos' : (-2.92, 0.954), 'connections' : [('Vilarinho', 52), ('Louro', 27)]},
    'Mouquim': {'pos' : (-0.447, 2.46), 'connections' : [('Louro', 16)]},
    'Esmeriz': {'pos' : (0.469, -3.559), 'connections' : []},
    'Vale': {'pos' : (3.322, 1.123), 'connections' : []},
    'Louro': {'pos' : (-1.383, 2.4), 'connections' : []},
    'Vilarinho': {'pos' : (-2.839, -2.616), 'connections' : []}
}

default_pos_bi = {
    'Vila Nova de Famalicão': {'pos': (0, 0), 'connections': [('Gavião', 27), ('Antas', 22), ('Calendário', 27), ('Mouquim', 34), ('Louro', 40), ('Brufe', 30)]},
    'Antas': {'pos' : (0.9, -1.2), 'connections' : [('Calendário', 39), ('Esmeriz', 26), ('Vale', 52)]},
    'Calendário': {'pos' : (-1, -1.466), 'connections' : [('Brufe', 16), ('Antas', 39)]},
    'Gavião': {'pos' : (1.052, 1.736), 'connections' : [('Vila Nova de Famalicão', 27), ('Vale', 35), ('Mouquim', 30), ('Antas', 50)]},
    'Brufe': {'pos' : (-1.396, -0.1), 'connections' : [('Louro', 34), ('Outiz', 25), ('Calendário', 16)]},
    'Outiz': {'pos' : (-2.92, 0.954), 'connections' : [('Vilarinho', 52), ('Louro', 27), ('Brufe', 25)]},
    'Mouquim': {'pos' : (-0.447, 2.46), 'connections' : [('Louro', 16), ('Vila Nova de Famalicão', 34)]},
    'Esmeriz': {'pos' : (0.469, -3.559), 'connections' : [('Antas', 26)]},
    'Vale': {'pos' : (3.322, 1.123), 'connections' : [('Gavião', 35), ('Antas', 52)]},
    'Louro': {'pos' : (-1.383, 2.4), 'connections' : [('Brufe', 34), ('Outiz', 27), ('Mouquim', 16)]},
    'Vilarinho': {'pos' : (-2.839, -2.616), 'connections' : [('Outiz', 52)]}
}


class Grafo:
    def __init__(self, graph_dict=default_pos_bi):
        self.nx = nx.Graph()
        self.g = graph_dict
        
        for node, data in graph_dict.items():
            node_name = node
            node_pos = data.get('pos', (0, 0))  # Default position is (0, 0) if not specified
            self.nx.add_node(node_name, pos=node_pos)

            for connection, cost in data.get('connections', []):
                self.nx.add_edge(node_name, connection, weight=cost)

    
    def heuristicFunction(self, initial_node, goal_node):
        if initial_node in self.nx.nodes:
            initial_pos = self.nx.nodes[initial_node]['pos']
        else:
            raise KeyError (f"{initial_node} does not exist in the graph")
        if goal_node in self.nx.nodes:
            goal_pos = self.nx.nodes[goal_node]['pos']
        else:
            raise KeyError (f"{goal_node} does not exist in the graph")
        
        #Usa-se a distância entre dois pontos num plano como heuristica com uma escala
        heuristic = (((goal_pos[0] - initial_pos[0]) **2 + (goal_pos[1] - initial_pos[1]) **2) **0.5) * 10
        return math.floor(heuristic)
    

                
    def iterative_deepening_dfs(self, start, target):
        path = []  # Caminho para a solução
        order_of_expansion = []  # Ordem de expansão
        def dfs(node, depth):
            order_of_expansion.append(node)
            if node == target:
                path.append(node)
                return True
            if depth > 0:
                for child in self.g.get(node, []):
                    if dfs((child[0], ), depth - 1):
                        path.append(node)
                        return True
            return False

        depth = 0
        while not dfs(start, depth):
            depth += 1

        unique_list = list(OrderedDict.fromkeys(order_of_expansion))
        return path[::-1], unique_list, depth
    
    def procura_DFS(self, ponto_inicial, ponto_objetivo):
        visitados = set() #armazenar nós visitados
        ordem_expansao = [] #Lista para armazenar a ordem de expansão dos nós
        
        #função auxiliar para converter tuplos em listas
        def converter_tuplos_para_lista(tuplos):
            return [item[0] for item in tuplos]

        #função para calcular o custo total dos arcos num dado caminho
        def calcular_custo_arcos(caminho):
            custo = 0
            for i in range(len(caminho) - 1):
                no_atual = caminho[i]
                no_seguinte = caminho[i + 1]
                for vizinho, custo_arco in self.g[no_atual]:
                    if vizinho == no_seguinte:
                        custo += custo_arco
                        break
            return custo

        #função principal da procura em profundidade 
        def DFS(atual, caminho, custo):
            visitados.add(atual)
            ordem_expansao.append(atual)
            caminho.append(atual)

            if atual == ponto_objetivo: #verifica se o nó atual é o objetivo
                return caminho, custo

            for vizinho, custo_arco in self.g[atual]:
                if vizinho not in visitados:
                    novo_custo = custo + custo_arco
                    resultado = DFS((vizinho, ), caminho.copy(), novo_custo)
                    if resultado:
                        return resultado
            
            return None

        #inicia a procura DFS
        caminho, custo = DFS(ponto_inicial, [], 0)
        ordem_expansao = converter_tuplos_para_lista(ordem_expansao)
        unique_list = list(OrderedDict.fromkeys(ordem_expansao))
        return caminho, unique_list, custo
    
    def get_arc_cost(self, node1, node2):
        custoT = math.inf
        lis = self.g[node1]  # lista de arestas para aquele nodo
        for (nodo, custo) in lis:
            if nodo == node2[0]:
                custoT = custo
        return custoT
    
    def calcula_custo(self, caminho):
        teste = caminho
        custo = 0
        i = 0
        while i + 1 < len(teste):
            custo = custo + self.get_arc_cost(teste[i], teste[i + 1])
            i = i + 1
        return custo
    
    
    def bfs(self, start, goal):
        if goal == []:
            return [start], 0, [start]
        goals = goal.copy()
        
        queue = deque([(start, [start], 0)])
        expansao = [start]
        
        visited = set([start])

        
        if start == goal:
            return [start]

        #pdb.set_trace()
        while queue:
            
            current, path , totalCost= queue.popleft()
            
            for neighbor, cost in self.g[current]['connections']:
                if neighbor not in visited:
                    
                    if neighbor in goals:
                        goals.remove(neighbor)
                        next_path, next_cost, next_expansao = self.bfs(neighbor, goals)
                        return path + next_path, totalCost + cost + next_cost, expansao + next_expansao
                    
                    expansao = expansao + [neighbor]

                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor], totalCost + cost))

        # If no path is found
        return None
    
    def custoUniforme (self, inicio, fim):
        # Inicialização
        fila_prioridade = [(0, inicio, [])]
        visitados = set()
        expansao = []

        while fila_prioridade:
            (custo, no_atual, caminho) = heapq.heappop(fila_prioridade)
            if no_atual not in visitados:
                visitados.add(no_atual)
                caminho = caminho + [no_atual]
                expansao.append(no_atual)

                if no_atual == fim:
                    return (custo, caminho, expansao)

                for vizinho, custo_aresta in self.g[no_atual]:
                    if (vizinho,) not in visitados:
                        heapq.heappush(fila_prioridade, (custo + custo_aresta, (vizinho, ), caminho))

        return float('inf'), [], []

    def a_estrela(self, inicio, fim):
        # Inicialização
        fila_prioridade = [(0 + self.heuristicFunction(inicio, fim), inicio, [])]
        visitados = set()
        expansao = []

        # Imprimir custos das arestas
        #for node, connections in self.g.items():
        #    for connection, cost in connections:
        #        print(f"Aresta de {node} para {connection} com custo {cost}")

        # Imprimir heurísticas
        #for node, data in self.nx.nodes(data=True):
        #    print(f'Nó: {node}, Heurística: {data["heuristic"]:.2f}')

        while fila_prioridade:
            (custo, no_atual, caminho) = heapq.heappop(fila_prioridade)
            if no_atual not in visitados:
                visitados.add(no_atual)
                caminho = caminho + [no_atual]
                expansao.append(no_atual)

                if no_atual == fim:
                    return round(custo, 2), caminho, expansao

                for vizinho, custo_aresta in self.g[(no_atual, )]:
                    if (vizinho,) not in visitados:
                        # Adiciona custo da aresta e heurística do próximo nó
                        custo_total_vizinho = custo - self.heuristicFunction(no_atual, fim) + custo_aresta + self.heuristicFunction(vizinho, fim)
                        heapq.heappush(fila_prioridade, (custo_total_vizinho, vizinho, caminho))

        return float('inf'), [], []

    def caminhosParaDestino (self, Ponto_Partida, Pontos_Chegada):
        A_star_path = []
        A_star_cost = 0
        A_star_expansao = []
        partida = Ponto_Partida
        for destino in Pontos_Chegada:
            custo, caminho, expansao = self.a_estrela(partida, destino)
            A_star_path = A_star_path + caminho
            A_star_cost = A_star_cost + custo
            A_star_expansao = A_star_expansao + expansao
            partida = destino
            
        return A_star_path, A_star_cost, A_star_expansao
            
    def visualize_graph_with_heuristic(self, goal_node):
        plt.clf()
        plt.ion()
        pos = nx.get_node_attributes(self.nx, 'pos')
        edge_labels = {(node1, node2): f'{cost}' for (node1, node2, cost) in self.nx.edges.data('weight')}
        
        # Calculate heuristic values and position them slightly below the nodes
        heuristic_labels = {node: (pos[node][0], pos[node][1] - 0.2, f'H = {self.heuristicFunction(node, goal_node)}') for node in self.nx.nodes}

        nx.draw(self.nx, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8, font_color='black', edge_color='black', linewidths=1, alpha=0.7)
        nx.draw_networkx_edge_labels(self.nx, pos, edge_labels=edge_labels, font_color='red', font_size=8)
        
        # Draw heuristic values with custom formatting
        for node, (x, y, label) in heuristic_labels.items():
            plt.text(x, y, label, color='red', fontweight='bold', fontsize=8, ha='center', va='center')

        plt.show()
        plt.ioff()
    
    """ def visualize_solution(self, goal_node, path):
        plt.clf()
        plt.ion()
        pos = nx.get_node_attributes(self.nx, 'pos')
        edge_labels = {(node1, node2): f'{cost}' for (node1, node2, cost) in self.nx.edges.data('weight')}
        
        # Calculate heuristic values and position them slightly below the nodes
        heuristic_labels = {node: (pos[node][0], pos[node][1] - 0.2, f'H = {self.heuristicFunction(node, goal_node)}') for node in self.nx.nodes}

        nx.draw(self.nx, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8, font_color='black', edge_color='black', linewidths=1, alpha=0.7)
        nx.draw_networkx_edge_labels(self.nx, pos, edge_labels=edge_labels, font_color='red', font_size=8)
        
        # Draw heuristic values with custom formatting
        for node, (x, y, label) in heuristic_labels.items():
            plt.text(x, y, label, color='red', fontweight='bold', fontsize=8, ha='center', va='center')
            
        a_star_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(self.nx, pos, edgelist=a_star_edges, edge_color='green', width=2)
        
        plt.title("Graph with Heuristic Values")
        plt.show()
        plt.ioff() """
    
    def visualize_solution(self, path, goals, algorithm, heuristic=False):
        plt.clf()
        plt.ion()
        plt.title(algorithm + ": " + path[0] + " -> " + str(goals))
        pos = nx.get_node_attributes(self.nx, 'pos')
        edge_labels = {(node1, node2): f'{cost}' for (node1, node2, cost) in self.nx.edges.data('weight')}

        edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(self.nx, pos, edgelist=edges, edge_color='blue', width=4)
            
        nx.draw(self.nx, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8, font_color='black', edge_color='black', linewidths=1, alpha=0.7)
        nx.draw_networkx_edge_labels(self.nx, pos, edge_labels=edge_labels, font_color='red', font_size=8)
        
        if not heuristic == False:
            heuristic_labels = {node: (pos[node][0], pos[node][1] - 0.2, f'H = {self.heuristicFunction(node, goal_node)}') for node in self.nx.nodes}
            for node, (x, y, label) in heuristic_labels.items():
                plt.text(x, y, label, color='red', fontweight='bold', fontsize=8, ha='center', va='center')
        
        plt.show()
        plt.ioff()

    def visualize_graph(self):
        plt.clf()
        plt.ion()
        plt.title("Grafo Inicial")
        pos = nx.get_node_attributes(self.nx, 'pos')
        edge_labels = {(node1, node2): f'{cost}' for (node1, node2, cost) in self.nx.edges.data('weight')}

        nx.draw(self.nx, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8, font_color='black', edge_color='black', linewidths=1, alpha=0.7)
        nx.draw_networkx_edge_labels(self.nx, pos, edge_labels=edge_labels, font_color='red', font_size=8)

        plt.show()
        plt.ioff()


if __name__ == '__main__':
    graph = Grafo()
    print(graph.bfs('Vila Nova de Famalicão', ['Vale', 'Outiz']))

""" graph = Grafo()
#print(format_path(solution) + "\n" + format_path(expanded_nodes))
print("DFS: ", graph.procura_DFS(('Vila Nova de Famalicão', ), ('Esmeriz', )))
print("BFS: ", graph.procura_BFS(('Vila Nova de Famalicão', ), ('Esmeriz', )))
print("UCS: ", graph.custoUniforme(('Vila Nova de Famalicão', ), ('Esmeriz', )))
print("IDDFS: ", graph.iterative_deepening_dfs(('Vila Nova de Famalicão', ), ('Esmeriz', )))
print(graph.caminhosParaDestino('Gavião', ['Louro']))
graph.visualize_solution('Louro', ['Gavião', 'Mouquim', 'Louro']) """

