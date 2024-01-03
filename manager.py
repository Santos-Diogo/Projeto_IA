from Grafo import Grafo
from Estafetas import *
from Entregas import *
import pdb

class Manager:
    def __init__(self):
        self.graph = Grafo()
        self.estafetas = populateEstafetas('Dataset/Estafetas.csv')
        self.entregas = populateEntregas('Dataset/Entregas.csv')
        self.trained = False
        
    def destinosEntregas (self, ids):
        destinos = []
        for id in ids:
            for entrega in self.entregas:
                if id == entrega.identificador:
                    destinos.append(entrega.destino)
        return destinos
    
    def entregasEstafeta(self, ids):
        res = []
        for id in ids:
            for entrega in self.entregas:
                if id == entrega.identificador:
                    res.append(entrega)
        return res
    
    def rotaBicicleta(kms, peso):
        vel = 10 - (peso * 0.6)
        return (kms * 60) / vel
    
    def rotaMota(kms, peso):
        vel = 35 - (peso * 0.5)
        return (kms * 60) / vel
    
    def rotaCarro(kms, peso):
        vel = 50 - (peso * 0.1)
        return (kms * 60) / vel
    
    def resolverBFS(self, estafetaID):
        estafeta = self.estafetas[estafetaID-1]
        destinos = self.destinosEntregas(estafeta.Lista_Encomendas)
        a, b, c = self.graph.bfs(estafeta.Ponto_Partida, destinos)
        return a, b, c, destinos
        
    def resolverDFS(self, estafetaID):
        estafeta = self.estafetas[estafetaID-1]
        destinos = self.destinosEntregas(estafeta.Lista_Encomendas)
        a, b, c = self.graph.dfs_search_tsp(estafeta.Ponto_Partida, destinos)
        return a, b, c, destinos
    
    def resolverIDDFS(self, estafetaID):
        estafeta = self.estafetas[estafetaID-1]
        destinos = self.destinosEntregas(estafeta.Lista_Encomendas)
        a, b, c = self.graph.iddfs_tsp(estafeta.Ponto_Partida, destinos)
        return a, b, c, destinos

    def resolverCustoUniforme(self, estafetaID):
        estafeta = self.estafetas[estafetaID-1]
        destinos = self.destinosEntregas(estafeta.Lista_Encomendas)
        a, b, c = self.graph.custoUniforme(estafeta.Ponto_Partida, destinos)
        return a, b, c, destinos
    
    def resolverGreedy(self, estafetaID):
        estafeta = self.estafetas[estafetaID-1]
        destinos = self.destinosEntregas(estafeta.Lista_Encomendas)
        if self.trained:
            a, b, c, dest= self.graph.busca_gulosa(estafeta.Ponto_Partida, destinos, self.graph.trainedHeuristicFunction)
        else:
            a, b, c, dest= self.graph.busca_gulosa(estafeta.Ponto_Partida, destinos, self.graph.heuristicFunction)
        return a, b, c, dest
    
    def resolverA_Star(self, estafetaID):
        estafeta = self.estafetas[estafetaID-1]
        destinos = self.destinosEntregas(estafeta.Lista_Encomendas)
        if self.trained:
            a, b, c, dest= self.graph.a_estrela(estafeta.Ponto_Partida, destinos, self.graph.trainedHeuristicFunction)
        else:
            a, b, c, dest= self.graph.a_estrela(estafeta.Ponto_Partida, destinos, self.graph.heuristicFunction)
        return a, b, c, dest
    
    def resolver(self, estafetaID):
        estafeta = self.estafetas[estafetaID-1]
        destinos = self.destinosEntregas(estafeta.Lista_Encomendas)
        pathBFS, custoBFS, expansaoBFS, destinosBFS = self.resolverBFS(estafetaID)
        pathDFS, custoDFS, expansaoDFS, destinosDFS = self.resolverDFS(estafetaID)
        pathIDDFS, custoIDDFS, expansaoIDDFS, destinosIDDFS = self.resolverIDDFS(estafetaID)
        pathCUn, custoCUn, expansaoCUn, destinosCUn = self.resolverCustoUniforme(estafetaID)
        pathGreedy, custoGreedy, expansaoGreedy, destinosGreedy = self.resolverGreedy(estafetaID)
        patha_star, custoa_star, expansaoa_star, destinosa_star = self.resolverA_Star(estafetaID)
        minCusto = min([custoBFS, custoa_star, custoCUn, custoDFS, custoGreedy, custoIDDFS])
        
        
    def pesos(self, entregas):
        sum = 0
        for entrega in entregas:
            sum = sum + entrega.peso
        return sum
        
    def train(self):
        self.graph.trainHeuristic()
        self.trained = True
    
    def estafetaInfo (self, id):
        for estafeta in self.estafetas:
            if id == estafeta.Id:
                return str(estafeta) + ", Destinos: " + str(self.destinosEntregas(estafeta.Lista_Encomendas))
        
    """ def concluiEstafeta (self, estafetaID):
        estafeta = self.estafetas[estafetaID-1]
        entregas = self.entregasEstafeta[estafeta.Lista_Encomendas]
        sorted_objects = sorted(entregas, key=lambda obj: obj.tempo)
        custo_otimo = self.resolver(estafetaID)
        pesos = self.pesos(sorted_objects)
        if pesos <= 5:
            tempo = self.rotaBicicleta(custo_otimo, pesos)
            if tempo < sorted_objects[-1].tempo:
                return something
            else:
                tempo = self.rotaMota(custo_otimo, pesos)
                return somethingelse
        elif pesos <= 20:
            tempo = self.rotaMota(custo_otimo, pesos)
            if tempo < sorted_objects[-1].tempo:
                return something
            else:
                tempo = self.rotaCarro(custo_otimo, pesos)
                return somethingelse
        elif pesos <= 100: """
            
        