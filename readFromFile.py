def readProblem(fileNum: int = 1):

    file = open('rcsp%d.txt'%fileNum, 'r')

    numVertices , numArcos , numRecursos = file.readline().split()

    numVertices = int(numVertices)
    numArcos = int(numArcos)
    numRecursos = int(numRecursos)


    lowerBound = file.readline()
    upperBound = file.readline()

    lowerBound = int(lowerBound)
    upperBound = int(upperBound)


    vetResourcesByVertices = []#recursos por vértice

    dictVert = dict() #dicionário que vai ter as informações indexadas por vértice



    for i in range(numVertices):
        vetResourcesByVertices.append(int(file.readline()))
        dictVert[i + 1] = []

    for j in range(numArcos):

        aux = file.readline().split()

        vertexI = int(aux[0])

        # if(vertexI not in dictVert):
        #     dictVert[vertexI] = []

        aux2 = []
        for k in range(1, len(aux)):
            aux2.append(int(aux[k]) )
        dictVert[vertexI].append(aux2)
  #  print(dictVert[1])


    file.close()
    #print(dictVert)
    return numVertices,numArcos, numRecursos,lowerBound, upperBound,vetResourcesByVertices, dictVert

if __name__ == '__main__':
    readProblem(3)
