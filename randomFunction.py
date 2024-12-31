from random import randint
from readFromFile import readProblem

#retorna uma solução aleatória não necessariamente ótima
def randomSolution(numVertices, numArcos, numRecursos, lowerBound, upperBound, vetResourcesByVertices, dictVert):

    visited = [1]

    goal = numVertices

    notFailed = True

    goalNotAchieved = True
    currVert = 1

    tries = 0

    recursosAcumulados = 0
    custoAcumulado = 0
    #while goalNotAchieved:
    while( goalNotAchieved and notFailed):
        tempVertsAtEnd = []
        tempCosts = []
        tempRecursosGastos = []

        for i in dictVert[currVert]: #pegar os vértices possíveis de caminhar
            vertEnd = i[0]
            cost = i[1]
            recursoGasto = i[2]
            if(vertEnd not in visited):
                tempVertsAtEnd.append(vertEnd)
                tempCosts.append(cost)
                tempRecursosGastos.append(recursoGasto)

        indexOfLowestCost = 0


        for i in range(len(tempVertsAtEnd)):
            if((tempRecursosGastos[i] + recursosAcumulados) < upperBound) and (tempVertsAtEnd[i] == numVertices): #achou o último vértice pegou
                indexOfLowestCost = i
                break
            elif((tempCosts[i] + tempRecursosGastos[i])/2 < (tempCosts[indexOfLowestCost] + tempRecursosGastos[indexOfLowestCost])/2 and ((tempRecursosGastos[i] + recursosAcumulados) < upperBound)):
                indexOfLowestCost = i
            elif ((tempCosts[i] + tempRecursosGastos[i])/2 >= (tempCosts[indexOfLowestCost] + tempRecursosGastos[indexOfLowestCost])/2  and ((tempRecursosGastos[i] + recursosAcumulados) < upperBound)):
                if randint(0,10) < 2: #Faz com que ele tente outros caminhos
                    indexOfLowestCost = i
                    break   #Se não fizer isso, a probabilidade fica tão baixa que sempre o próximo sobrescreve
            else:
                tries += 1
                print(tempCosts[i])
                print(tempCosts[indexOfLowestCost])
                print(recursosAcumulados)
                print(upperBound)
                print('Caminho falho, não encontrei seguindo por:', visited)
                notFailed = False
                break

        visited.append(tempVertsAtEnd[indexOfLowestCost])
        recursosAcumulados += tempRecursosGastos[indexOfLowestCost]
        custoAcumulado += tempCosts[indexOfLowestCost]

        currVert = tempVertsAtEnd[indexOfLowestCost]


        if currVert == goal:
            print('Caminho Bem Sucedido:',visited)
            print(tries)
            goalNotAchieved = False #alcancei o vértice alvo

        if notFailed == False:
            currVert = 1
            visited = [1]
            recursosAcumulados = 0
            custoAcumulado = 0
            notFailed = True


    return visited, custoAcumulado, recursosAcumulados

numVertices,numArcos, numRecursos,lowerBound, upperBound,vetResourcesByVertices, dictVert = readProblem(1)
randomSolution(numVertices, numArcos, numRecursos, lowerBound, upperBound, vetResourcesByVertices, dictVert)