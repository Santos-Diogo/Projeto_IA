from manager import Manager


class Menu:
    def __init__(self):
        self.manager = Manager()


    def __adicionarHeuristica (self):
        choice = input("Escolha o nó para a heurística se basear: ")
        if choice in self.manager.graph.nx.nodes:
            self.manager.graph.visualize_graph_with_heuristic(choice)
        else:
            print("O nó que escolheu não existe...")


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
            print (f"Custo: {custo}; Expansão: {expansao}")
            self.manager.graph.visualize_solution(caminho, destinos, "BFS")
        elif choice == '2':
            self.__adicionarHeuristica()
        elif choice == '3':
            self.__escolherEstafeta()
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
