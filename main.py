import uniformCostSearch
import aStarSearch
import aStarSearchManhattan

print("\nDigite o tabuleiro inicial (usando None no lugar do bloco vazio):")
print("Ex: 1, 2, None, 4, 5, 3, 7, 8, 6 \n")

initialPuzzle = (input('Tabuleiro: ')).replace(" ", "").split(",")

for i in initialPuzzle:
    if i.isdigit():
        initialPuzzle[initialPuzzle.index(i)] = int(i)
    elif i.lower() == 'none':
        initialPuzzle[initialPuzzle.index(i)] = None

print("\nQual algoritmo você deseja?:")
print("1 - Custo uniforme")
print("2 - A* simples")
print("3 - A* com melhor implementação (Manhattan)\n")

userResponse = input('Opção: ')

if userResponse == "1":
    uniformCostSearch.uniform_cost_search(initialPuzzle)
elif userResponse == "2":
    aStarSearch.aStarSearch(initialPuzzle)
elif userResponse == "3":
    aStarSearchManhattan.a_star_manhattan_search(initialPuzzle)
else:
    print("Opção não encontrada, use 1, 2 ou 3.")
