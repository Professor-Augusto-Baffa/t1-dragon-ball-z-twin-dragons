import auxiliar as aux
from lutas import randomGen, evolucao, simAnnealing, tempoTotal

# Pedro Gonçalves Mannarino - 2210617
# Luiza Marcondes Paes Leme - 2210275


# Fácil alteração dos valores de batalhas e heróis
batalhas = [35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
herois = [1.1, 1.2, 1.3, 1.4, 1.5]

# Escolhemos representar as coordenadas do mapa como [x][y], x sendo linha e y coluna
mapa = aux.lerMapa()

lugares = aux.lerLugares()

caminhos = []

mapaDinamicoFinal = aux.criarMapaDinamico(mapa)

somaTempo = 0

for i in range(len(lugares) - 1):
    try:
        posI, posE = aux.acharPos(mapa, lugares[i], lugares[i + 1])
    except TypeError:
        print("Mapa contruído incorretamente.")
        quit()
    
    mapaDinamico = aux.criarMapaDinamico(mapa)

    inicio = aux.Coord(posI[0], posI[1], posE, 0, None)
    listaAEstrela = [inicio]

    aux.caminharMapaDinamico(mapaDinamico, inicio.x, inicio.y, mapa, aux.screen)
    aux.caminharMapaDinamico(mapaDinamico, posE[0], posE[1], mapa, aux.screen)

    conhecidos = []

    while(True):
        coordAtual = listaAEstrela[0]
        del listaAEstrela[0]

        if ((coordAtual.x, coordAtual.y) not in conhecidos):
            conhecidos.append((coordAtual.x, coordAtual.y))
        
        if (coordAtual.heuristica == 0):
            caminhos.append(aux.acharCaminho(coordAtual, lugares[i]))
            aux.agregarMapa(mapaDinamicoFinal, mapaDinamico)

            # tempMapa = []
            # for linha in mapaDinamico:
            #     tempMapa.append(linha.copy())

            # aux.concatenarMapaDinamico(tempMapa)

            # print()
            # for linha in tempMapa:
            #     print(linha)
            # print()
            somaTempo += caminhos[i][0]
            print("Tempo da caminhada até " + lugares[i+1] + ": " + str(somaTempo))
            break
        
        aux.avaliaVizinhos(mapa, coordAtual, conhecidos)

        for filho in coordAtual.filhos:
            aux.caminharMapaDinamico(mapaDinamico, filho.x, filho.y, mapa, aux.screen)

        listaAEstrela.extend(coordAtual.filhos)

        listaAEstrela.sort(key = lambda x : x.percorrido + x.heuristica)


flag = 'Z'
for caminho in caminhos:
    aux.atualizarMapaDinamico(mapaDinamicoFinal, caminho[2:], flag, aux.screen)
    flag = 'Y' if flag == 'Z' else 'Z' if flag == 'W' else 'W'

aux.concatenarMapaDinamico(mapaDinamicoFinal)

# Cálculo do tempo da combinação das lutas
ngens = 1600
indsgen = 300
batalhas.sort()
herois.sort()

geracaoFinal = []

for gens in range(4):
    geracao = randomGen(indsgen, batalhas, herois)
    geracao = evolucao(ngens, indsgen, geracao, batalhas, herois)
    print("Melhor fitness da geracao " + str(gens + 1) + " -> " + str(geracao[0][0]))
    geracao[0] = simAnnealing(geracao[0], batalhas, herois)
    print("Melhor fitness da geracao " + str(gens + 1) + " após sim annealing -> " + str(geracao[0][0]))
    geracaoFinal.extend(geracao[:int(indsgen/4)])

geracaoFinal = evolucao(ngens, indsgen, geracaoFinal, batalhas, herois)
print("Melhor fitness da última geracao -> " + str(geracaoFinal[0][0]))
print("Melhor combinação da última geracao -> " + str(geracaoFinal[0][1]))
print("Melhor tempo da última geração -> " + str(tempoTotal(geracaoFinal[0][1], batalhas, herois)))

melhor = simAnnealing(geracaoFinal[0], batalhas, herois)

print("Melhor fitness da última geracao após sim annealing -> " + str(melhor[0]))
print("Melhor combinação da última geracao após sim annealing -> " + str(melhor[1]))
print("Melhor tempo da última geração após sim annealing -> " + str(tempoTotal(melhor[1], batalhas, herois)))

print("Tempo da caminhada:" + str(somaTempo))

print("TEMPO TOTAL: " + str(somaTempo + tempoTotal(melhor[1], batalhas, herois)))