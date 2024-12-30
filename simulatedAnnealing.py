from math import exp


def func(solu):
    return 1

def simulAnnealing(s, to, SAmax):
    solOtima = s
    iterT = 0
    t = to
    alfa = 0.9
    while t >0.00001:
        while iterT< SAmax:
            iterT += 1
            #TODO gerar um vizinho aleatório s' pertence a Vizinhança de s
            sLinha = None
            delta = func(sLinha) - func(s)
            if (delta <0):
                s = sLinha
                if(func(s) < func(solOtima)): #Se o novo s for menor do que a atual solução ótima
                    solOtima = sLinha
            else:
                x = 0.5
                if 0.5 < exp((-delta/t)):
                    s = sLinha
        t = alfa * t
        iterT = 0
    s = solOtima
    return s
