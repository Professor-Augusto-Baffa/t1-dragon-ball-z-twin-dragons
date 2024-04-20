import math

class Coord():
    def __init__(self, x, y, posE, percorrido, pai):
        self.x = x
        self.y = y
        self.posE = posE
        self.percorrido = percorrido
        self.heuristica = heuristica(x, y, posE)
        self.pai = pai
        self.filhos = []


def lerMapa():
    with open("mapa.txt", "r") as arq:
        mapa = [x.strip() for x in arq.readlines()]

    return mapa

def lerLugares():
    with open("lugares.txt", "r") as arq:
        lugares = [x for x in arq.readline()]

    return lugares

def acharPos(mapa, c):
    I = None
    E = None

    x = 0
    for linha in mapa:
        y = 0
        for coluna in linha:
            
            if (mapa[x][y] == 'I'):
                I = (x, y)
                if (E != None):
                    return I, E
                
            if (mapa[x][y] == c):
                E = (x, y)
                if (I != None):
                    return I, E
                
            y += 1
        x += 1
        
    return None


def heuristica(x, y, posE):
    return abs(x - posE[0]) + abs(y - posE[1])


def validaCelula(mapa, x, y):
    if (x < 0 or x >= len(mapa) or y < 0 or y >= len(mapa[0])):
        return False
    
    return True


def avaliaCelula(mapa, x, y):
    c = mapa[x][y]

    if (c == 'M'):
        return 200
    
    if (c == 'A'):
        return 30

    if (c == 'F'):
        return 15

    if (c == 'R'):
        return 5

    return 1


def avaliaVizinhos(mapa, x, y, pai):
    vizinhos = []

    if (validaCelula(mapa, x + 1, y)):
        vizinhos.append(Coord(x + 1, y, pai.posE, pai.percorrido + avaliaCelula(mapa, x + 1, y), pai))

    if (validaCelula(mapa, x - 1, y)):
        vizinhos.append(Coord(x - 1, y, pai.posE, pai.percorrido + avaliaCelula(mapa, x - 1, y), pai))

    if (validaCelula(mapa, x, y + 1)):
        vizinhos.append(Coord(x, y + 1, pai.posE, pai.percorrido + avaliaCelula(mapa, x, y + 1), pai))

    if (validaCelula(mapa, x, y - 1)):
        vizinhos.append(Coord(x, y + 1, pai.posE, pai.percorrido + avaliaCelula(mapa, x, y - 1), pai))

    pai.filhos = vizinhos
    
    return vizinhos
