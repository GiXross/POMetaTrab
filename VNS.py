from random import randint
from readFromFile import readProblem
from randomFunction import randomSolution

def calcular_custo(grafo, caminho):
    custo = 0
    for i in range(len(caminho) - 1):
        for arco in grafo[caminho[i]]:
            if arco[0] == caminho[i + 1]:
                custo += arco[1]
                break
    return custo

def calcular_recurso(grafo, caminho):
    recurso = 0
    for i in range(len(caminho) - 1):
        for arco in grafo[caminho[i]]:
            if arco[0] == caminho[i + 1]:
                recurso += arco[2]
                break
    return recurso

def gerar_vizinho(s, dictVert, upperBound):
    vizinho = embaralha(s, dictVert, upperBound)
    return vizinho

def embaralha(vO, dictVert, upperBound):
    tamVO = len(vO)
    voltar = randint(1, tamVO - 1)
    currVert = vO[voltar - 1]
    vA = vO[:voltar]
    goal = vO[-1]

    notFailed = True
    goalNotAchieved = True
    tries = 0

    recursosAcumulados = calcular_recurso(dictVert, vA)
    custoAcumulado = calcular_custo(dictVert, vA)

    while (goalNotAchieved and notFailed and tries < 1000):
        tempVertsAtEnd = []
        tempCosts = []
        tempRecursosGastos = []

        for i in dictVert[currVert]:
            vertEnd = i[0]
            cost = i[1]
            recursoGasto = i[2]
            if vertEnd not in vA:
                tempVertsAtEnd.append(vertEnd)
                tempCosts.append(cost)
                tempRecursosGastos.append(recursoGasto)

        indexOfLowestCost = 0
        for i in range(len(tempVertsAtEnd)):
            if (tempRecursosGastos[i] + recursosAcumulados < upperBound and tempVertsAtEnd[i] == goal and randint(0, 10) < 2):
                indexOfLowestCost = i
                break
            elif (tempCosts[i] + tempRecursosGastos[i]) / 2 < (tempCosts[indexOfLowestCost] + tempRecursosGastos[indexOfLowestCost]) / 2 and (tempRecursosGastos[i] + recursosAcumulados) < upperBound:
                indexOfLowestCost = i
            elif (tempCosts[i] + tempRecursosGastos[i]) / 2 >= (tempCosts[indexOfLowestCost] + tempRecursosGastos[indexOfLowestCost]) / 2 and (tempRecursosGastos[i] + recursosAcumulados) < upperBound:
                if randint(0, 10) < 2:
                    indexOfLowestCost = i
                    break
            else:
                tries += 1
                notFailed = False
                break

        if len(tempVertsAtEnd) > 0:
            vA.append(tempVertsAtEnd[indexOfLowestCost])
            recursosAcumulados += tempRecursosGastos[indexOfLowestCost]
            custoAcumulado += tempCosts[indexOfLowestCost]
            currVert = tempVertsAtEnd[indexOfLowestCost]
        else:
            notFailed = False

        if notFailed == False:
            currVert = vO[voltar - 1]
            vA = vO[:voltar]
            recursosAcumulados = calcular_recurso(dictVert, vA)
            custoAcumulado = calcular_custo(dictVert, vA)
            notFailed = True

        elif currVert == goal:
            goalNotAchieved = False

    if tries >= 1000:
        vA = vO
    if vO[-1] not in vA:
        print("Erro na execução do código!")
        exit(1)

    return vA

def vns(s, dictVert, upperBound, maxIter=100):
    melhor_solucao = s
    melhor_custo = calcular_custo(dictVert, s)
    k = 1

    while k <= maxIter:
        vizinho = gerar_vizinho(s, dictVert, upperBound)
        custo_vizinho = calcular_custo(dictVert, vizinho)

        if custo_vizinho < melhor_custo:
            melhor_solucao = vizinho
            melhor_custo = custo_vizinho
            k = 1  # Reinicia a busca se uma melhoria for encontrada
        else:
            k += 1  # Aumenta o nível de vizinhança

    return melhor_solucao, melhor_custo

def main(pE):
    numVertices, numArcos, numRecursos, lowerBound, upperBound, vetResourcesByVertices, dictVert = readProblem(pE)
    print(f"Grafo de {numVertices} vértices e {numArcos} arcos:")
    print(dictVert)

    # Gerar solução inicial aleatória
    sol_inicial, _, _ = randomSolution(numVertices, numArcos, numRecursos, lowerBound, upperBound, vetResourcesByVertices, dictVert)

    # Rodar o VNS para encontrar a melhor solução
    melhor_solucao, melhor_custo = vns(sol_inicial, dictVert, upperBound)

    print(f'Melhor solução encontrada pelo VNS: {melhor_solucao}')
    print(f'Custo da melhor solução encontrada: {melhor_custo}')
    print(f'Recursos gastos na melhor solução: {calcular_recurso(dictVert, melhor_solucao)}')

if __name__ == '__main__':
    problemaEscolhido = 4  # Exemplo de número de problema
    main(problemaEscolhido)
