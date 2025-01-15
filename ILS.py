from math import exp
from readFromFile import readProblem
from randomFunction import randomSolution
from random import randint
from simulatedAnnealing import *

def buscaLocal(s, iterMax, dictVert, upperBound):
    solAtual = s
    solOtima = s

    for _ in range(iterMax):
        # Gera um vizinho aleatório
        sLinha = generateRandomNeighbor(solAtual, dictVert, upperBound)

        # Compara os custos e atualiza a solução se o vizinho for melhor
        if funcCusto(sLinha, dictVert) < funcCusto(solAtual, dictVert):
            solAtual = sLinha

        # Atualiza a melhor solução encontrada
        if funcCusto(solAtual, dictVert) < funcCusto(solOtima, dictVert):
            solOtima = solAtual

    return solOtima


def iteratedLocalSearch(s, iterMax, dictVert, upperBound):
    """
    Função para o Iterated Local Search (ILS) usando Hill Climbing.
    """
    solOtima = s

    for iteracao in range(iterMax):
        # Realiza a busca local usando Hill Climbing
        solAtual = buscaLocal(s, 100, dictVert, upperBound)

        # Atualiza a melhor solução se necessário
        if funcCusto(solAtual, dictVert) < funcCusto(solOtima, dictVert):
            solOtima = solAtual

        # Aplica uma perturbação para escapar de ótimos locais
        s = perturbaSolucao(solOtima, dictVert, upperBound)

    return solOtima


def perturbaSolucao(s, dictVert, upperBound):
    """
    Aplica uma perturbação controlada na solução atual.
    Retorna uma solução vizinha aleatória diferente.
    """
    # Aqui usamos a função generateRandomNeighbor para gerar um vizinho aleatório.
    return generateRandomNeighbor(s, dictVert, upperBound)


def mainILS(iterMax, beta, gama, pE):
    """
    Função principal para executar o ILS com Hill Climbing.
    """
    numVertices, numArcos, numRecursos, lowerBound, upperBound, vetResourcesByVertices, dictVert = readProblem(pE)
    visited, custoAcumulado, recursosAcumulados = randomSolution(numVertices, numArcos, numRecursos, lowerBound, upperBound, vetResourcesByVertices, dictVert)
    melhorSolILS = iteratedLocalSearch(visited, iterMax, dictVert, upperBound)
    print('Melhor Solução Encontrada pelo Iterated Local Search:', melhorSolILS)
    print('Custo da Melhor Solução:', funcCusto(melhorSolILS, dictVert))
    print('Recursos Gastos na Melhor Solução:', funcRecurso(melhorSolILS, dictVert))


if __name__ == '__main__':
    problemaEscolhido = 1
    mainILS(iterMax=100, beta=2, gama=0.95, pE=problemaEscolhido)
