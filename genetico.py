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

    return 1.2 ** (sum(batalhas) - tempoTotal(ind, batalhas, herois))

def randomGen(qtd, batalhas, herois):
    
    geracao = []

    # Geração aleatória
    for n in range(qtd):

        verificacao = batalhas.copy()
        while(verificacao != set()):
            
            ind = []
            verificacao = batalhas.copy()
            h = random.sample(batalhas, 4)
            h.sort()
            ind.append(h)
            verificacao = set(verificacao) - set(ind[0])
            
            for i in range(len(herois) - 1):
                h = random.sample(batalhas, 5)
                h.sort()
                ind.append(h)
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
    
    for gen in range(ngens):
    
        sortedgeracao = sorted(geracao, key = lambda x: x[0], reverse = True)

        total = 0
        for el in sortedgeracao:
            total += el[0]

        prob = []
        for el in sortedgeracao:
            prob.append(el[0]/total)

        novaGeracao = []

        novaGeracao.extend(sortedgeracao[:int(indsgen*0.06)])


        for n in range(int(indsgen*0.86)):
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

batalhas = [35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
herois = [1.1, 1.2, 1.3, 1.4, 1.5]
ngens = 1500
indsgen = 400
batalhas.sort()
herois.sort()

melhores = []
#melhores.append([fitness([[45, 60, 75, 50], [55, 65, 85, 70, 60], [50, 90, 80, 95, 45], [85, 35, 90, 55, 95], [70, 75, 65, 80, 40]], batalhas, herois), [[45, 60, 75, 50], [55, 65, 85, 70, 60], [50, 90, 80, 95, 45], [85, 35, 90, 55, 95], [70, 75, 65, 80, 40]]])
#melhores.append([fitness([[50, 70, 85, 55], [80, 75, 50, 45, 95], [90, 45, 65, 60, 55], [35, 75, 60, 40, 65], [70, 80, 90, 95, 85]], batalhas, herois), [[50, 70, 85, 55], [80, 75, 50, 45, 95], [90, 45, 65, 60, 55], [35, 75, 60, 40, 65], [70, 80, 90, 95, 85]]])
#melhores.append([fitness([[55, 50, 45, 90], [45, 60, 75, 70, 55], [65, 85, 60, 50, 90], [85, 70, 95, 80, 35], [95, 75, 40, 65, 80]], batalhas, herois), [[55, 50, 45, 90], [45, 60, 75, 70, 55], [65, 85, 60, 50, 90], [85, 70, 95, 80, 35], [95, 75, 40, 65, 80]]])
#melhores.append([fitness([[50, 70, 65, 75], [50, 55, 45, 85, 60], [45, 55, 80, 95, 75], [40, 60, 80, 90, 95], [90, 35, 65, 85, 70]], batalhas, herois), [[50, 70, 65, 75], [50, 55, 45, 85, 60], [45, 55, 80, 95, 75], [40, 60, 80, 90, 95], [90, 35, 65, 85, 70]]])
#melhores.append([fitness([[80, 60, 50, 45], [65, 85, 70, 55, 75], [45, 65, 50, 80, 90], [95, 90, 35, 60, 70], [55, 95, 75, 40, 85]], batalhas, herois), [[80, 60, 50, 45], [65, 85, 70, 55, 75], [45, 65, 50, 80, 90], [95, 90, 35, 60, 70], [55, 95, 75, 40, 85]]])
#melhores.append([fitness([[65, 75, 45, 85], [55, 45, 95, 90, 60], [55, 80, 65, 50, 70], [90, 50, 75, 95, 70], [80, 35, 60, 40, 85]], batalhas, herois), [[65, 75, 45, 85], [55, 45, 95, 90, 60], [55, 80, 65, 50, 70], [90, 50, 75, 95, 70], [80, 35, 60, 40, 85]]])
#melhores.append([fitness([[65, 45, 60, 50], [50, 90, 75, 45, 60], [80, 55, 70, 85, 40], [80, 55, 95, 70, 90], [75, 65, 85, 95, 35]], batalhas, herois), [[65, 45, 60, 50], [50, 90, 75, 45, 60], [80, 55, 70, 85, 40], [80, 55, 95, 70, 90], [75, 65, 85, 95, 35]]])
#melhores.append([fitness([[65, 70, 40, 55], [60, 40, 55, 75, 95], [50, 70, 90, 60, 80], [50, 65, 90, 85, 80], [95, 45, 85, 35, 75]], batalhas, herois), [[65, 70, 40, 55], [60, 40, 55, 75, 95], [50, 70, 90, 60, 80], [50, 65, 90, 85, 80], [95, 45, 85, 35, 75]]])
#melhores.append([fitness([[90, 55, 60, 45], [75, 55, 50, 85, 65], [65, 80, 95, 90, 45], [95, 50, 85, 80, 70], [70, 40, 60, 35, 75]], batalhas, herois), [[90, 55, 60, 45], [75, 55, 50, 85, 65], [65, 80, 95, 90, 45], [95, 50, 85, 80, 70], [70, 40, 60, 35, 75]]])
#melhores.append([fitness([[55, 50, 45, 60], [75, 45, 70, 60, 50], [65, 90, 80, 95, 85], [80, 85, 90, 70, 55], [40, 35, 65, 95, 75]], batalhas, herois), [[55, 50, 45, 60], [75, 45, 70, 60, 50], [65, 90, 80, 95, 85], [80, 85, 90, 70, 55], [40, 35, 65, 95, 75]]])
#melhores.append([fitness([[50, 80, 55, 75], [65, 60, 40, 85, 55], [65, 40, 90, 70, 50], [95, 75, 85, 90, 70], [45, 80, 35, 95, 60]], batalhas, herois), [[50, 80, 55, 75], [65, 60, 40, 85, 55], [65, 40, 90, 70, 50], [95, 75, 85, 90, 70], [45, 80, 35, 95, 60]]])
#melhores.append([fitness([[45, 65, 55, 50], [75, 45, 70, 60, 50], [80, 90, 70, 85, 60], [55, 85, 90, 80, 95], [40, 35, 65, 95, 75]], batalhas, herois), [[45, 65, 55, 50], [75, 45, 70, 60, 50], [80, 90, 70, 85, 60], [55, 85, 90, 80, 95], [40, 35, 65, 95, 75]]])
#melhores.append([fitness([[45, 65, 55, 50], [75, 45, 70, 60, 50], [70, 85, 55, 90, 80], [60, 80, 95, 85, 90], [40, 35, 65, 95, 75]], batalhas, herois), [[45, 65, 55, 50], [75, 45, 70, 60, 50], [70, 85, 55, 90, 80], [60, 80, 95, 85, 90], [40, 35, 65, 95, 75]]])
#melhores.append([fitness([[55, 50, 45, 60], [65, 50, 75, 45, 70], [70, 85, 55, 90, 80], [60, 80, 95, 85, 90], [40, 35, 65, 95, 75]], batalhas, herois), [[55, 50, 45, 60], [65, 50, 75, 45, 70], [70, 85, 55, 90, 80], [60, 80, 95, 85, 90], [40, 35, 65, 95, 75]]])
#melhores.append([fitness([[55, 50, 45, 60], [65, 50, 75, 45, 70], [65, 80, 70, 55, 85], [60, 80, 95, 85, 90], [90, 95, 35, 75, 40]], batalhas, herois), [[55, 50, 45, 60], [65, 50, 75, 45, 70], [65, 80, 70, 55, 85], [60, 80, 95, 85, 90], [90, 95, 35, 75, 40]]])
#melhores.append([fitness(, batalhas, herois), ])
#melhores.append([fitness(, batalhas, herois), ])
#melhores.append([fitness(, batalhas, herois), ])
#melhores.append([fitness(, batalhas, herois), ])



geracao = randomGen(indsgen, batalhas, herois)
geracao.extend(melhores)
geracao1 = evolucao(ngens, indsgen, geracao, batalhas, herois)
print(geracao1[0][0])
geracao = randomGen(indsgen, batalhas, herois)
geracao.extend(melhores)
geracao2 = evolucao(ngens, indsgen, geracao, batalhas, herois)
print(geracao2[0][0])
geracao = randomGen(indsgen, batalhas, herois)
geracao.extend(melhores)
geracao3 = evolucao(ngens, indsgen, geracao, batalhas, herois)
print(geracao3[0][0])
geracao = randomGen(indsgen, batalhas, herois)
geracao.extend(melhores)
geracao4 = evolucao(ngens, indsgen, geracao, batalhas, herois)
print(geracao4[0][0])


geracaofinal = geracao1[:int(indsgen*0.25)]
geracaofinal.extend(geracao2[:int(indsgen*0.25)])
geracaofinal.extend(geracao3[:int(indsgen*0.25)])
geracaofinal.extend(geracao4[:int(indsgen*0.25)])

geracaofinal = evolucao(ngens, indsgen, geracaofinal, batalhas, herois)
print(geracaofinal[0][1])
melhor = geracaofinal[0].copy()

for n in range(1000):
    mutado = mutacao(melhor[1], batalhas)
    if (fitness(mutado, batalhas, herois) > melhor[0]):
        melhor[1] = mutado
        melhor[0] = fitness(mutado, batalhas, herois)
        print(melhor[0])

print(geracaofinal[0][1])
print(geracaofinal[0][0])
print(tempoTotal(geracaofinal[0][1], batalhas, herois))
print(fitness([[55, 50, 45, 60], [65, 50, 75, 45, 70], [65, 80, 70, 55, 85], [60, 80, 95, 85, 90], [90, 95, 35, 75, 40]], batalhas, herois))
print(tempoTotal([[55, 50, 45, 60], [65, 50, 75, 45, 70], [65, 80, 70, 55, 85], [60, 80, 95, 85, 90], [90, 95, 35, 75, 40]], batalhas, herois))