import random

def tempoTotal(ind, batalhas, herois):
    
    tempo = 0

    for batalha in batalhas:
        
        soma = 0
        for n in range(len(herois)):
            if (batalha in ind[n]):
                soma += herois[n]
        tempo += batalha/soma
    
    return tempo

def fitness(ind, batalhas, herois):
    valor = 1.4 ** (sum(batalhas) - tempoTotal(ind, batalhas, herois))
    if (not verificaAnt(ind, batalhas, herois)):
        return valor
    return valor * 10

def copiaListaDeListas(lista):
    nova = []
    for l in lista:
        nova.append(l.copy())
    return nova

def verificaAnt(ind, batalhas, herois):

    somaant = 0

    for batalha in batalhas:     
        soma = 0
        for n in range(len(herois)):
            if (batalha in ind[n]):
                soma += herois[n]
        if (soma < somaant):
            return False
        somaant = soma

    return True

def simAnnealing(melhor, batalhas, herois):

    melhorAnt = [melhor[0]]
    melhorAnt.append(copiaListaDeListas(melhor[1])) 
    melhorTotal = [melhor[0]]
    melhorTotal.append(copiaListaDeListas(melhor[1])) 

    for n in range(5500):

        mutado = mutacao(copiaListaDeListas(melhor[1]), batalhas)

        if (random.random() < 0.4):
            num = random.randint(1, 7)
            for i in range(num):
                mutado = mutacao(copiaListaDeListas(mutado), batalhas)

        if (n % 25 == 0):
            if (melhor == melhorAnt):
                melhor[1] = copiaListaDeListas(mutado)
                melhor[0] = fitness(melhor[1], batalhas, herois)
                if (melhor[0] > melhorTotal[0]):
                    melhorTotal = [melhor[0]]
                    melhorTotal.append(copiaListaDeListas(melhor[1])) 
                melhorAnt = [melhor[0]]
                melhorAnt.append(copiaListaDeListas(melhor[1]))

        if (fitness(mutado, batalhas, herois) > melhor[0]):
            melhor[1] = copiaListaDeListas(mutado)
            melhor[0] = fitness(melhor[1], batalhas, herois)
    
    if (melhorTotal[0] > melhor[0]):
        return melhorTotal
    return melhor

def randomGen(qtd, batalhas, herois):
    
    geracao = []

    # Geração aleatória
    for n in range(qtd):
        verificacao = batalhas.copy()

        while(verificacao != set()):

            ind = []
            verificacao = batalhas.copy()
            ind.append(random.sample(batalhas, 4))
            verificacao = set(verificacao) - set(ind[0])
            
            for i in range(len(herois) - 1):
                ind.append(random.sample(batalhas, 5))
                verificacao = set(verificacao) - set(ind[i+1])

        geracao.append([fitness(ind, batalhas, herois), ind])
    
    return geracao

def mutacao(ind, batalhas):

    while(True):
        h1 = random.choice(ind)
        b1 = random.choice(h1)
        h2 = random.choice(ind)
        if (b1 not in h2):
            b2 = random.choice(h2)
            if (b2 not in h1):
                h1[h1.index(b1)] = b2
                h2[h2.index(b2)] = b1
                break
    
    return ind

def evolucao(ngens, indsgen, geracao, batalhas, herois):

    sortedgeracao = sorted(geracao, key = lambda x: x[0], reverse = True)
    melhor = sortedgeracao[0].copy()

    for gen in range(ngens):
    
        sortedgeracao = sorted(geracao, key = lambda x: x[0], reverse = True)

        total = 0
        for el in sortedgeracao:
            total += el[0]

        prob = []
        for el in sortedgeracao:
            prob.append(el[0]/total)

        novaGeracao = []

        if (sortedgeracao[0][0] > melhor[0]):
            melhor = sortedgeracao[0].copy()

        if ((gen + 1) % 50 == 0):
            novaGeracao.append(melhor)

        for n in range(int(indsgen*0.92)):
            pai = random.choices(sortedgeracao, prob)[0][1]
            mae = random.choices(sortedgeracao, prob)[0][1]

            verificacao = batalhas.copy()

            while(verificacao != set()):
                filho = []
                
                verificacao = batalhas.copy()
                for i in range(len(pai)):
                    if (random.random() < 0.5):
                        filho.append(pai[i].copy())
                    else:
                        filho.append(mae[i].copy())
                    verificacao = set(verificacao) - set(filho[i])


                if (random.random() < 0.1):
                    filho = mutacao(filho, batalhas)
            
    
        novaGeracao.extend(randomGen(int(indsgen*0.08), batalhas, herois))
        geracao = novaGeracao

    return sorted(geracao, key = lambda x: x[0], reverse = True)
