from Grafo import Grafo
from Estafetas import *
from Entregas import *
import pdb

class Manager:
    def __init__(self):
        self.graph = Grafo()
        self.estafetas = populateEstafetas('Dataset/Estafetas.csv')
        self.entregas = populateEntregas('Dataset/Entregas.csv')
        
    def destinosEntregas (self, ids):
        destinos = []
        for id in ids:
            for entrega in self.entregas:
                if id == entrega.identificador:
                    destinos.append(entrega.destino)
        return destinos
    
    def resolverBFS(self, estafetaID):
        estafeta = self.estafetas[estafetaID-1]
        destinos = self.destinosEntregas(estafeta.Lista_Encomendas)
        a, b, c = self.graph.bfs(estafeta.Ponto_Partida, destinos)
        return a, b, c, destinos
        
                
    
    def estafetaInfo (self, id):
        for estafeta in self.estafetas:
            if id == estafeta.Id:
                return str(estafeta) + ", Destinos: " + str(self.destinosEntregas(estafeta.Lista_Encomendas))

    def __entregaByID (self, entregaID):
        for entrega in self.entregas:
            if entrega.identificador == entregaID:
                return entrega
        raise KeyError (f"Não existe entregas com o ID {entregaID}")
        
    def concluiEstafeta (self, estafeta):
        estafetaObj = self.estafetas[estafeta-1]
        encomendas = estafetaObj.Lista_Encomendas
        ponto_inicio = estafetaObj.Ponto_Partida
        entregas_estafeta = []
        destinos = []
        for encomenda in encomendas:
            entrega = self.__entregaByID(encomenda)
            destinos.append(entrega.destino)
            entregas_estafeta.append(entrega)

        
        fim = self.graph.caminhosParaDestino(ponto_inicio, destinos)
        self.graph.visualize_solution(destinos[0], fim[0])
    
    