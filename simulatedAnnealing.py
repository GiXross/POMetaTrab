from math import exp
from readFromFile import readProblem
from randomFunction import randomSolution
from random import randint


def temperaturaInicial(beta, gama, SAmax, to, s,dictVert,upperBound):
    t = to
    continua = True
    while continua:
        aceitos = 0
        for i in range(SAmax):
            sLinha = generateRandomNeighbor(s, dictVert, upperBound)
            delta = funcCusto(sLinha, dictVert) - funcCusto(s, dictVert)
            if delta<0:
                aceitos += 1
            else:
                x = 0.5
                if x < exp((-delta / t)):
                    aceitos +=1
        if aceitos >= gama*SAmax:
            continua = False
        else:
            t = beta * t

    return t



def embaralha(vO,dictVert, upperBound):
    tamVO = len(vO)
    #print(vO)
    voltar = randint(1,tamVO-1) #o quão atrás nas escolhas vai querer voltar atrás

    currVert = vO[voltar-1] #pega o valor na posição ''voltar''
    vA = vO[:voltar] #pega os ''voltar'' primeiros valores

    #
    goal = vO[-1] #último elemento da vizinhança original

    notFailed = True

    goalNotAchieved = True

    tries = 0

    recursosAcumulados = funcRecurso(vA, dictVert)
    custoAcumulado = funcCusto(vA, dictVert)
    # while goalNotAchieved:
    while (goalNotAchieved and notFailed and tries<1000):
        tempVertsAtEnd = []
        tempCosts = []
        tempRecursosGastos = []

        for i in dictVert[currVert]:  # pegar os vértices possíveis de caminhar
            #print(currVert)
            vertEnd = i[0]
            cost = i[1]
            recursoGasto = i[2]
            if (vertEnd not in vA):
                tempVertsAtEnd.append(vertEnd)
                tempCosts.append(cost)
                tempRecursosGastos.append(recursoGasto)

        indexOfLowestCost = 0

        for i in range(len(tempVertsAtEnd)):
            if ((tempRecursosGastos[i] + recursosAcumulados) < upperBound) and (
                    tempVertsAtEnd[i] == goal) and (randint(0, 10) < 2):  # achou o último vértice pega na maioria dos casos, mas as vezes tenta outra coisa
                indexOfLowestCost = i
                break
            elif ((tempCosts[i] + tempRecursosGastos[i]) / 2 < (
                    tempCosts[indexOfLowestCost] + tempRecursosGastos[indexOfLowestCost]) / 2 and (
                          (tempRecursosGastos[i] + recursosAcumulados) < upperBound)):
                indexOfLowestCost = i
            elif ((tempCosts[i] + tempRecursosGastos[i]) / 2 >= (
                    tempCosts[indexOfLowestCost] + tempRecursosGastos[indexOfLowestCost]) / 2 and (
                          (tempRecursosGastos[i] + recursosAcumulados) < upperBound)):
                if randint(0, 10) < 2:  # Faz com que ele tente outros caminhos
                    indexOfLowestCost = i
                    break  # Se não fizer isso, a probabilidade fica tão baixa que sempre o próximo sobrescreve
            else:
                tries += 1
                notFailed = False
                break

        if len(tempVertsAtEnd)>0:
            vA.append(tempVertsAtEnd[indexOfLowestCost])
            recursosAcumulados += tempRecursosGastos[indexOfLowestCost]
            custoAcumulado += tempCosts[indexOfLowestCost]
            currVert = tempVertsAtEnd[indexOfLowestCost]
        else:
            notFailed = False

        if notFailed == False:
            currVert = vO[voltar-1]
            vA = vO[:voltar]
            #print(vA)
            recursosAcumulados = funcRecurso(vA, dictVert)
            custoAcumulado = funcCusto(vA, dictVert)
            notFailed = True
         #   print('aqui')
        elif currVert == goal:
            # if 100 not in vA:
            #     print(vO)
            #     print(vA)
            goalNotAchieved = False  # alcancei o vértice alvo
        # print('Failed:',notFailed)
        # print('Goal Not Achieved',goalNotAchieved)
        # print('Tries:', tries)

    #

    if tries >= 1000:
        #print('tries')
        vA = vO
    if vO[-1] not in vA:
        print(vO)
        print(vA)
        print('Algo deu errado na execução do código')
        exit(1)
    #print(vA)
    return vA

def generateRandomNeighbor(s,dictVert,upperBound):
    vizinhancaOriginal = s

    vizinhancaAleatoria = embaralha(vizinhancaOriginal,dictVert,upperBound)

    return vizinhancaAleatoria


def funcRecurso(solu, dictVert): #preciso do dictVert para obter meu custo
    #print(solu)
    recurso = 0
    for i in range(len(solu)):
        vert = solu[i]
        for j in range(len(dictVert[vert])):
            if vert != solu[-1]:

                # print(dictVert[vert][j][0])
                #
                # print(solu[i])
                # print(solu[i +1])

                if dictVert[vert][j][0] == solu[i +1]:
                    recurso += dictVert[vert][j][2]

#    print('custo:',custo)

    return recurso

def funcCusto(solu, dictVert): #preciso do dictVert para obter meu custo
    #print(solu)
    custo = 0
    for i in range(len(solu)):
        vert = solu[i]
        for j in range(len(dictVert[vert])):
            if vert != solu[-1]:

                # print(dictVert[vert][j][0])
                #
                # print(solu[i])
                # print(solu[i +1])

                if dictVert[vert][j][0] == solu[i +1]:
                    custo += dictVert[vert][j][1]

#    print('custo:',custo)

    return custo

def simulAnnealing(s, to, SAmax, dictVert,upperBound, alfa):
    solOtima = s
    iterT = 0
    t = to
    while t >0.001:
        while iterT< SAmax:
            iterT += 1
            #TODO gerar um vizinho aleatório s' pertence a Vizinhança de s

            sLinha = generateRandomNeighbor(s,dictVert,upperBound)
            #print('s', sLinha)
            delta = funcCusto(sLinha, dictVert) - funcCusto(s, dictVert)
            if (delta <0):
                s = sLinha
                if(funcCusto(sLinha, dictVert) < funcCusto(solOtima, dictVert)): #Se o novo s for menor do que a atual solução ótima
                    solOtima = sLinha
            else:
                x = 0.5
                if x < exp((-delta/t)):
                    s = sLinha
        t = alfa * t
        iterT = 0
    s = solOtima
    return s


def main(SAmax, alfa, beta, gama,pE):
    numVertices,numArcos, numRecursos,lowerBound, upperBound,vetResourcesByVertices, dictVert = readProblem(pE)
    visited, custoAcumulado, recursosAcumulados = randomSolution(numVertices, numArcos, numRecursos, lowerBound, upperBound, vetResourcesByVertices, dictVert)
    to = temperaturaInicial(beta, gama,SAmax, 1,visited, dictVert, upperBound)
    print('Temperatura Inicial: ',to)
    melhorSolEncontrada = simulAnnealing(visited, to, SAmax, dictVert,upperBound, alfa)
    print('Melhor Solução Encontrada pelo Simulated Annealing:',melhorSolEncontrada)
    print('Custo Melhor Solucao Encontrada:', funcCusto(melhorSolEncontrada, dictVert))
    print('Recursos Gastos Melhor Solucao Encontrada:', funcRecurso(melhorSolEncontrada, dictVert))

if __name__ == '__main__':
    problemaEscolhido = 1
    main(SAmax=1000,alfa=0.9, beta=2,gama=0.95, pE=problemaEscolhido)