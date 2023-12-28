import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue
import math
import heapq
import pdb
from collections import OrderedDict

def format_path(path):          #Pega numa lista de nodes, em formato tuplo e separa por -
    return ' -> '.join(node for node in path)

class Grafo:
    def __init__(self, graph_dict):
        self.nx = nx.Graph()
        self.g = graph_dict
        
        for node, connections in graph_dict.items():
            if len(node) == 1:  # Caso a posição não seja fornecida, definimos como (0, 0)
                node_name, node_pos = node[0], (0, 0)
            elif len(node) == 2:
                node_name, node_pos = node
            else:
                raise ValueError("Cada entrada do dicionário deve ter 1 ou 2 elementos.")

            self.nx.add_node(node_name, pos=node_pos)
            for connection, cost in connections:
                self.nx.add_edge(node_name, connection, weight=cost)
            
                
    def iterative_deepening_dfs(self, start, target):
        path = []  # Caminho para a solução
        order_of_expansion = []  # Ordem de expansão
        pdb.set_trace()
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
    
    def procura_BFS(self, start, end):
        # definir nodos visitados para evitar ciclos
        visited = set()
        fila = Queue()
        expansao = []
        # adicionar o nodo inicial à fila e aos visitados
        fila.put(start)
        visited.add(start)
        # garantir que o start node não tem pais...
        parent = dict()
        parent[start] = None

        path_found = False
        while not fila.empty() and not path_found:
            nodo_atual = fila.get()
            expansao.append(nodo_atual)
            if nodo_atual == end:
                path_found = True
            else:
                for (adjacente, peso) in self.g[nodo_atual]:
                    if (adjacente,) not in visited:
                        fila.put((adjacente,))
                        parent[(adjacente,)] = nodo_atual
                        visited.add((adjacente,))

        # Reconstruir o caminho
        path = []
        custo = 0
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            # função calcula custo caminho
            custo = self.calcula_custo(path)
        return (path, custo, expansao)
    
    
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
        ('Mouquim', ): [],
        ('Seide', ): [],
        ('Vale', ): [],
        ('Louro', ): [],
        ('Vilarinho', ): []
    }


graph = Grafo(graph_dict)
#print(format_path(solution) + "\n" + format_path(expanded_nodes))
print("DFS: ", graph.procura_DFS(('Vila Nova de F', ), ('Seide', )))
print("BFS: ", graph.procura_BFS(('Vila Nova de F', ), ('Seide', )))
print("UCS: ", graph.custoUniforme(('Vila Nova de F', ), ('Seide', )))
print("IDDFS: ", graph.iterative_deepening_dfs(('Vila Nova de F', ), ('Seide', )))
visualize_graph(graph.nx)
