from manager import Manager
import pdb

class Menu:
    def __init__(self):
        self.manager = Manager()


    def __adicionarHeuristica (self):
        choice = input("Escolha o nó para a heurística se basear: ")
        ch_list = [item.strip() for item in choice.split(',')]
        present = True
        for element in ch_list:
            if element not in self.manager.graph.nx.nodes:
                print("Um dos nós que escolheu não existe...")
                return
        self.manager.graph.visualize_graph_with_heuristic(ch_list)


    def __menuEstafeta (self, estafeta):
        print("Menu do " + self.manager.estafetaInfo(estafeta.Id))
        print("1. Aplicar BFS")
        print("2. Aplicar DFS")
        print("3. Aplicar IDDFS")
        print("4. Aplicar Custo Uniforme")
        print("5. Aplicar Greedy")
        print("6. Aplicar A*")
        print("7. Resolver Estafeta")
        print("8. Sair")
        choice = input("Opção (1-8): ")
        
        if choice == '1':
            caminho, custo, expansao, destinos= self.manager.resolverBFS(estafeta.Id)
            print (f"Caminho: {caminho}; Custo: {custo}; Expansão: {expansao}")
            self.manager.graph.visualize_solution(caminho, destinos, "BFS")
        elif choice == '2':
            caminho, custo, expansao, destinos= self.manager.resolverDFS(estafeta.Id)
            print (f"Caminho: {caminho}; Custo: {custo}; Expansão: {expansao}")
            self.manager.graph.visualize_solution(caminho, destinos, "DFS")
        elif choice == '3':
            caminho, custo, expansao, destinos= self.manager.resolverIDDFS(estafeta.Id)
            print (f"Caminho: {caminho}; Custo: {custo}; Expansão: {expansao}")
            self.manager.graph.visualize_solution(caminho, destinos, "IDDFS")
        elif choice == '4':
            caminho, custo, expansao, destinos= self.manager.resolverCustoUniforme(estafeta.Id)
            print (f"Caminho: {caminho}; Custo: {custo}; Expansão: {expansao}")
            self.manager.graph.visualize_solution(caminho, destinos, "Custo Uniforme")
        elif choice == '5':
            caminho, custo, expansao, destinos= self.manager.resolverGreedy(estafeta.Id)
            print (f"Caminho: {caminho}; Custo: {custo}; Expansão: {expansao}")
            self.manager.graph.visualize_solution(caminho, destinos, "Greedy", True)
        elif choice == '6':
            caminho, custo, expansao, destinos= self.manager.resolverA_Star(estafeta.Id)
            print (f"Caminho: {caminho}; Custo: {custo}; Expansão: {expansao}")
            self.manager.graph.visualize_solution(caminho, destinos, "A*", True)
        elif choice == '8':
            return
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

    def __escolherEstafeta(self):
        i = 0
        while(i < len(self.manager.estafetas)):
            print(self.manager.estafetaInfo(i+1))
            i = i + 1
        choice = input(f"Escholha o estafeta (1 - {i}): ")
        estafeta = self.manager.estafetas[int(choice) - 1]
        self.__menuEstafeta(estafeta)
        
        
        
    def iniciar(self):
        while True:
            print("1. Mostrar Grafo")
            print("2. Adicionar Heuristica")
            print("3. Escolher estafeta para correr o programa")
            print("4. Exit")

            choice = input("Insira a sua escolha (1-4): ")

            if choice == '1':
                self.manager.graph.visualize_graph()
            elif choice == '2':
                self.__adicionarHeuristica()
            elif choice == '3':
                self.__escolherEstafeta()
            elif choice == '4':
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    visualizer = Menu()
    visualizer.iniciar()
