import auxiliar as aux

# Pedro Gonçalves Mannarino - 2210617
# Luiza Marcondes Paes Leme - 2210275

# Escolhemos representar as coordenadas do mapa como [x][y], x sendo linha e y coluna

mapa = aux.lerMapa()

lugares = aux.lerLugares()

caminhos = []

contFoi = 0
for i in range(len(lugares) - 1):
    try:
        posI, posE = aux.acharPos(mapa, lugares[i], lugares[i + 1])
    except TypeError:
        print("Mapa contruído incorretamente.")
        quit()
    
    listaAEstrela = [aux.Coord(posI[0], posI[1], posE, 0, None)]

    conhecidos = []

    while(True):
        coordAtual = listaAEstrela[0]
        del listaAEstrela[0]
        
        conhecidos.append((coordAtual.x, coordAtual.y))
        
        if (coordAtual.heuristica == 0):
            caminhos.append(aux.acharCaminho(coordAtual, lugares[i]))
            break
        
        aux.avaliaVizinhos(mapa, coordAtual, conhecidos)
       
        listaAEstrela.extend(coordAtual.filhos)

        listaAEstrela.sort(key = lambda x : x.percorrido + x.heuristica)

mapaDinamico = aux.criarMapaDinamico(mapa)

for caminho in caminhos:
    aux.atualizarMapaDinamico(mapaDinamico, caminho[1:], caminho[0])

aux.concatenarMapaDinamico(mapaDinamico)

print(mapaDinamico)