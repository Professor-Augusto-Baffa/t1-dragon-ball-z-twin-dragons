import auxiliar as aux

# Pedro Gonçalves Mannarino - 2210617
# Luiza Marcondes Paes Leme - 2210275

# Escolhemos representar as coordenadas do mapa como [x][y], x sendo linha e y coluna

mapa = aux.lerMapa()

lugares = aux.lerLugares()

posXY = posI

for i in range(len(lugares)):
    try:
        posI, posE = aux.acharPos(mapa, lugares[i])
    except TypeError:
        print("Mapa contruído incorretamente.")
        quit()

    listaAEstrela = [aux.Coord(posI[0], posI[1], posE, 0, None)]
