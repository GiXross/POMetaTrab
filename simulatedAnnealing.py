from math import exp
from readFromFile import readProblem
from randomFunction import randomSolution
from random import randint
from random import random
import time

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
                x = random()
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
                x = random()
                if x < exp((-delta/t)):
                    s = sLinha
        t = alfa * t
        iterT = 0
    s = solOtima
    return s


def main(alfa, beta, gama,pE):
    numVertices,numArcos, numRecursos,lowerBound, upperBound,vetResourcesByVertices, dictVert = readProblem(pE)
    SAmax = numVertices
    valTempo = 0
    for i in range(10):
        visited, custoAcumulado, recursosAcumulados = randomSolution(numVertices, numArcos, numRecursos, lowerBound,
                                                                     upperBound, vetResourcesByVertices, dictVert)
        tempo1 = time.time()
        print('Solução %d' % (i + 1))
        to = temperaturaInicial(beta, gama,SAmax, 1,visited, dictVert, upperBound)
        print('Temperatura Inicial: ',to)
        melhorSolEncontrada = simulAnnealing(visited, to, SAmax, dictVert,upperBound, alfa)
        print('Melhor Solução Encontrada pelo Simulated Annealing:',melhorSolEncontrada)
        print('Custo Melhor Solucao Encontrada:', funcCusto(melhorSolEncontrada, dictVert))
        print('Recursos Gastos Melhor Solucao Encontrada:', funcRecurso(melhorSolEncontrada, dictVert))

        tempo2 = time.time()

        difTempo = (tempo2 - tempo1)
        valTempo += difTempo
        print('Tempo da execução: ', difTempo)
    print('Média de tempo das execuções: ', valTempo / 10)

if __name__ == '__main__':
    problemaEscolhido = 2

    main(alfa=0.99, beta=2, gama=0.95, pE=problemaEscolhido)




# Problema 2(com x pertence a [0,1])
# Solução 1
# Temperatura Inicial:  1024
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  27.796696424484253
# Solução 2
# Temperatura Inicial:  1024
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  27.129844665527344
# Solução 3
# Temperatura Inicial:  128
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  24.023000478744507
# Solução 4
# Temperatura Inicial:  256
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  25.352001428604126
# Solução 5
# Temperatura Inicial:  1
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  15.523013353347778
# Solução 6
# Temperatura Inicial:  1
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  15.663985967636108
# Solução 7
# Temperatura Inicial:  128
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  24.417999505996704
# Solução 8
# Temperatura Inicial:  512
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  25.95504856109619
# Solução 9
# Temperatura Inicial:  1
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  14.922965288162231
# Solução 10
# Temperatura Inicial:  512
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  25.012986421585083
# Média de tempo das execuções:  22.579754209518434



# Problema 2(com x podendo ser 0.1, 0.2, 0.3..., 1)
# Solução 1
# Temperatura Inicial:  65536
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  38.72322702407837

# Solução 2
# Temperatura Inicial:  4096
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  32.689213275909424

# Solução 3
# Temperatura Inicial:  8
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  16.430323362350464

# Solução 4
# Temperatura Inicial:  2048
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  29.09767723083496

# Solução 5
# Temperatura Inicial:  2048
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  32.588782787323

# Solução 6
# Temperatura Inicial:  1
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  15.94067645072937

# Solução 7
# Temperatura Inicial:  512
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  28.346956491470337

# Solução 8
# Temperatura Inicial:  512
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  27.609987497329712

# Solução 9
# Temperatura Inicial:  1024
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  28.832045793533325

# Solução 10
# Temperatura Inicial:  32768
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  38.01396441459656
# Média de tempo das execuções:  28.82728543281555




#Old
# Solução 1
# Temperatura Inicial:  256
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  118.05201172828674

# Solução 2
# Temperatura Inicial:  4194304
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  188.81798648834229


# Solução 3
# Temperatura Inicial:  512
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  112.96100068092346

# Solução 4
# Temperatura Inicial:  2048
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  134.82916164398193
# Solução 5
# Temperatura Inicial:  302231454903657293676544
#

#Solução 1 OLD
# Temperatura Inicial:  8192
# Melhor Solução Encontrada pelo Simulated Annealing: [1, 72, 86, 74, 34, 100]
# Custo Melhor Solucao Encontrada: 216
# Recursos Gastos Melhor Solucao Encontrada: 36
# Tempo da execução:  264.42280197143555