import auxiliar as aux

# Pedro Gonçalves Mannarino - 2210617
# Luiza Marcondes Paes Leme - 2210275

# Escolhemos representar as coordenadas do mapa como [x][y], x sendo linha e y coluna

mapa = aux.lerMapa()

lugares = aux.lerLugares()

caminhos = []

mapaDinamicoFinal = aux.criarMapaDinamico(mapa)

for i in range(len(lugares) - 1):
    try:
        posI, posE = aux.acharPos(mapa, lugares[i], lugares[i + 1])
    except TypeError:
        print("Mapa contruído incorretamente.")
        quit()
    
    mapaDinamico = aux.criarMapaDinamico(mapa)

    inicio = aux.Coord(posI[0], posI[1], posE, 0, None)
    listaAEstrela = [inicio]

    aux.caminharMapaDinamico(mapaDinamico, inicio.x, inicio.y, mapa)
    aux.caminharMapaDinamico(mapaDinamico, posE[0], posE[1], mapa)

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

            break
        
        aux.avaliaVizinhos(mapa, coordAtual, conhecidos)

        for filho in coordAtual.filhos:
            aux.caminharMapaDinamico(mapaDinamico, filho.x, filho.y, mapa)

        listaAEstrela.extend(coordAtual.filhos)

        listaAEstrela.sort(key = lambda x : x.percorrido + x.heuristica)

somaTempo = 0

for caminho in caminhos:
    char = "\033[1;31m" + caminho[1] +  "\033[0;0m"
    aux.atualizarMapaDinamico(mapaDinamicoFinal, caminho[2:], char)
    somaTempo += caminho[0]

aux.concatenarMapaDinamico(mapaDinamicoFinal)

for linha in mapaDinamicoFinal:
    print(linha)